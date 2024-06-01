import logging
import traceback

import awsgi
import humps
from flask import Flask, Response, jsonify, request, g
from flask_cors import CORS
from flask_injector import FlaskInjector
from injector import inject

from src.models import Track
from src.recommendations import RecommendationsService
from src.spotify import Spotify
from src.spotify_unauthorized import SpotifyUnauthorized

app = Flask(__name__)
CORS(app)


@app.before_request
def get_token():
    g.token = request.headers.get('token')

@app.after_request
def camelize_response(response):
    if response.is_json:
        response.set_data(jsonify(humps.camelize(response.get_json())).get_data())
    return response

@inject
@app.route('/search/playlists/<path:query>')
def __search_playlists(spotify: Spotify, query: str):
    return jsonify(spotify.search_playlists(query))


@inject
@app.route('/search/tracks/<path:query>')
def __search_tracks(spotify: Spotify, query: str):
    return jsonify(spotify.search_tracks(query))


@inject
@app.route('/playlist/<playlist_id>/tracks')
def __playlist_tracks(spotify: Spotify, playlist_id: str):
    return jsonify(spotify.get_playlist_tracks(playlist_id))


@inject
@app.route('/recommendations', methods=['POST'])
def __recommendations(recommendations: RecommendationsService):
    return jsonify(recommendations.get_recommendations([Track(**humps.decamelize(x)) for x in request.get_json()]))


@inject
@app.errorhandler(500)
def __error(e: Exception):
    logging.error(e)
    return Response(traceback.format_exc(), status=500, mimetype='application/text')


@inject
@app.errorhandler(SpotifyUnauthorized)
def __spotify_unauthorized(e: SpotifyUnauthorized):
    return jsonify(e.message), e.status


def lambda_handler(event, context):
    FlaskInjector(app=app)
    return awsgi.response(app, event, context)


if __name__ == '__main__':
    FlaskInjector(app=app)
    app.run(port=5000, debug=True)
