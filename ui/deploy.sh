#!/bin/zsh

bun install
bun run build
aws s3 sync build "s3://sonar.aaronmamparo.com" --delete
aws cloudfront create-invalidation --distribution-id "E1ORYGIYCSA44Q" --paths "/*"