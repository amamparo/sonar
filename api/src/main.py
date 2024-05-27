import logging
import traceback

import awsgi
from flask import Flask, Response, jsonify, request, g
from flask_cors import CORS
from flask_injector import FlaskInjector
from injector import inject

from src.spotify import Spotify
from src.spotify_unauthorized import SpotifyUnauthorized

app = Flask(__name__)
CORS(app)


@inject
@app.before_request
def require_token():
    if request.method == 'OPTIONS':
        return jsonify({}, 200)
    token = request.headers.get('token')
    if not token:
        return jsonify({"error": "Missing required token"}), 401
    g.token = token


@inject
@app.route('/search/playlists/<path:query>')
def __playlist_search(spotify: Spotify, query: str):
    return jsonify(spotify.search_playlists(query))


@inject
@app.route('/playlist/<playlist_id>/tracks')
def __playlist_tracks(spotify: Spotify, playlist_id: str):
    return jsonify(spotify.playlist_tracks(playlist_id))


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
