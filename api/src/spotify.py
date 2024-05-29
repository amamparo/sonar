from urllib import parse
from typing import List, Dict

import requests
from flask import g
from injector import singleton

from src.models import Track, AudioFeatures
from src.spotify_unauthorized import SpotifyUnauthorized


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

    def get_playlist_tracks(self, playlist_id) -> List[Track]:
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

    def get_audio_features(self, track_ids: List[str]) -> Dict[str, AudioFeatures]:
        batches = [track_ids[i:i + 100] for i in range(0, len(track_ids), 100)]
        result = {}
        for batch_ids in batches:
            result.update({
                x['id']: AudioFeatures(
                    acousticness=x['acousticness'],
                    danceability=x['danceability'],
                    energy=x['energy'],
                    instrumentalness=x['instrumentalness'],
                    liveness=x['liveness'],
                    speechiness=x['speechiness'],
                    valence=x['valence']
                )
                for x in self.__get('/v1/audio-features', {'ids': ','.join(batch_ids)}).get('audio_features', [])
            })
        return result

    def get_recommendations(self, track_ids: List[str]) -> List[Track]:
        tracks = self.__get('/v1/recommendations', {'seed_tracks': ','.join(track_ids), 'limit': 100})['tracks']
        return [
            Track(
                id=t['id'],
                title=t['name'],
                artist=', '.join([a['name'] for a in t['artists']]),
                album=t['album']['name'],
                image_url=next((t for t in sorted(t['album']['images'], key=lambda i: i['height'])), {}).get('url'),
                preview_url=t['preview_url']
            )
            for t in tracks
        ]

    @staticmethod
    def __get(path: str, params: dict) -> dict:
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
