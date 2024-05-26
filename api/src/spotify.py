from typing import List

import requests
from flask import g
from injector import singleton

from src.spotify_unauthorized import SpotifyUnauthorized


@singleton
class Spotify:
    def search(self, query: str) -> List[dict]:
        playlists = self.__get('/v1/search', {'q': query, 'type': 'playlist', 'limit': 50})['playlists']['items']
        return [
            {
                'id': x['id'],
                'name': x['name'],
                'author': x['owner']['display_name'],
                'image': sorted(x['images'], key=lambda i: i['height'])[0]['url']
            }
            for x in playlists
        ]

    def __get(self, path: str, params: dict) -> dict:
        response = requests.get(
            f'https://api.spotify.com{path}',
            params=params,
            headers={
                'Authorization': f'Bearer {g.get("token")}'
            }
        )
        if 400 <= response.status_code <= 499:
            raise SpotifyUnauthorized(response.status_code, response.json())
        if response.status_code >= 500:
            raise Exception(response.text)
        return response.json()

