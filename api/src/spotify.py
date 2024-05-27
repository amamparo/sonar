from dataclasses import dataclass
from urllib import parse
from typing import List

import requests
from flask import g
from injector import singleton

from src.spotify_unauthorized import SpotifyUnauthorized


@dataclass
class Track:
    id: str
    title: str
    artist: str
    album: str
    image_url: str
    preview_url: str


@singleton
class Spotify:
    def search_playlists(self, query: str) -> List[dict]:
        playlists = (self.__get('/v1/search', {'q': query, 'type': 'playlist', 'limit': 50})
                     .get('playlists', {})
                     .get('items', []))
        return [
            {
                'id': x['id'],
                'title': x['name'],
                'author': x['owner']['display_name'],
                'image_url': next((y for y in sorted(x['images'], key=lambda i: i['height'])), {}).get('url')
            }
            for x in playlists
        ]

    def search_tracks(self, query: str) -> List[Track]:
        tracks = (self.__get('/v1/search', {'q': query, 'type': 'track', 'limit': 50})
                     .get('tracks', {})
                     .get('items', []))
        return [
            Track(
                id=x['id'],
                title=x['name'],
                artist=', '.join([a['name'] for a in x['artists']]),
                album=x['album']['name'],
                image_url=sorted(x['album']['images'], key=lambda i: i['height'])[0]['url'],
                preview_url=x['preview_url']
            )
            for x in tracks
        ]

    def playlist_tracks(self, playlist_id) -> List[Track]:
        initial_response = self.__get(f'/v1/playlists/{playlist_id}/tracks', {
            'limit': 100
        })
        items = initial_response.get('items', [])
        next_url = initial_response.get('next')
        while next_url:
            next_response = self.__get_full(next_url)
            items += next_response.get('items', [])
            next_url = next_response.get('next')
        return [
            Track(
                id=x['track']['id'],
                title=x['track']['name'],
                artist=', '.join([a['name'] for a in x['track']['artists']]),
                album=x['track']['album']['name'],
                image_url=sorted(x['track']['album']['images'], key=lambda i: i['height'])[0]['url'],
                preview_url=x['track']['preview_url']
            )
            for x in items
        ]

    def __get(self, path: str, params: dict) -> dict:
        return Spotify.__get_full(f'https://api.spotify.com{path}?{parse.urlencode(params)}')

    @staticmethod
    def __get_full(url: str) -> dict:
        response = requests.get(
            url,
            headers={
                'Authorization': f'Bearer {g.get("token")}'
            }
        )
        if response.status_code == 404:
            return {}
        if 400 <= response.status_code <= 403:
            raise SpotifyUnauthorized(response.status_code, response.json())
        if response.status_code >= 500:
            raise Exception(response.text)
        return response.json()
