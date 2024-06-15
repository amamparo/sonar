import os
from os import getcwd, path
from typing import cast

from aws_cdk import Duration, App, Stack, RemovalPolicy
from aws_cdk.aws_apigateway import LambdaRestApi, CorsOptions
from aws_cdk.aws_certificatemanager import Certificate
from aws_cdk.aws_cloudfront import OriginAccessIdentity, CloudFrontWebDistribution, SourceConfiguration, \
    S3OriginConfig, Behavior, ViewerCertificate
from aws_cdk.aws_ecr_assets import Platform
from aws_cdk.aws_lambda import DockerImageFunction, DockerImageCode, IFunction
from aws_cdk.aws_route53 import ARecord, HostedZone, RecordTarget
from aws_cdk.aws_route53_targets import CloudFrontTarget
from aws_cdk.aws_s3 import Bucket, BlockPublicAccess, HttpMethods
from constructs import Construct

account = os.environ.get('CDK_DEFAULT_ACCOUNT')
region = os.environ.get('CDK_DEFAULT_REGION')


class Sonar(Stack):
    def __init__(self, scope: Construct):
        super().__init__(scope, 'sonar', env={'account': account, 'region': region})
        api = LambdaRestApi(
            self,
            'sonar-api',
            default_cors_preflight_options=CorsOptions(
                allow_origins=['*'],
                allow_methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
                allow_headers=['Token', 'Content-Type'],
                allow_credentials=True,
                disable_cache=True
            ),
            handler=cast(IFunction, DockerImageFunction(
                self,
                'sonar-api-function',
                function_name='sonar-api-function',
                memory_size=256,
                code=DockerImageCode.from_image_asset(
                    directory=path.join(getcwd(), '..', 'api'),
                    platform=Platform.LINUX_AMD64,
                    cmd=['src.main.lambda_handler'],
                ),
                timeout=Duration.seconds(30),
            ))
        )

        bucket = Bucket(
            self, 'bucket', bucket_name='sonar.aaronmamparo.com',
            website_index_document='index.html',
            website_error_document='index.html',
            public_read_access=True,
            block_public_access=BlockPublicAccess.BLOCK_ACLS,
            cors=[
                {
                    'allowedMethods': [HttpMethods.GET],
                    'allowedOrigins': ['*'],
                    'allowedHeaders': ['*'],
                }
            ],
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        oai = OriginAccessIdentity(self, 'oai')
        bucket.grant_read(oai)

        distribution = CloudFrontWebDistribution(
            self,
            'sonar-distribution',
            error_configurations=[
                {
                    'errorCode': 404,
                    'responseCode': 200,
                    'responsePagePath': '/index.html'
                }
            ],
            origin_configs=[
                SourceConfiguration(
                    s3_origin_source=S3OriginConfig(
                        s3_bucket_source=bucket,
                        origin_access_identity=oai
                    ),
                    behaviors=[
                        Behavior(
                            is_default_behavior=True,
                            max_ttl=Duration.days(365),
                            default_ttl=Duration.days(365),
                            compress=True,
                        )
                    ]
                )
            ],
            viewer_certificate=ViewerCertificate.from_acm_certificate(
                Certificate.from_certificate_arn(
                    self,
                    'certificate',
                    f'arn:aws:acm:{region}:{account}:certificate/d4a83e58-baff-48b1-94e8-13a214184f81'
                ),
                aliases=['sonar.aaronmamparo.com'],
            ),
            default_root_object='index.html'
        )

        ARecord(
            self,
            'a-record',
            zone=HostedZone.from_lookup(self, 'hosted-zone', domain_name='aaronmamparo.com'),
            record_name='sonar.aaronmamparo.com',
            target=RecordTarget.from_alias(CloudFrontTarget(distribution))
        )


if __name__ == '__main__':
    app = App()
    Sonar(app)
    app.synth()
