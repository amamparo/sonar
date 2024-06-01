from concurrent.futures import ThreadPoolExecutor, as_completed
from random import shuffle
from urllib import parse
from typing import List, Dict

import requests
from flask import g
from injector import singleton

from src.models import Track, AudioFeatures, Artist, Playlist
from src.spotify_unauthorized import SpotifyUnauthorized


@singleton
class Spotify:
    def search_playlists(self, query: str) -> List[Playlist]:
        playlists = (self.__get('/v1/search', {'q': query, 'type': 'playlist', 'limit': 50})
                     .get('playlists', {})
                     .get('items', []))
        return [
            Playlist(
                id=x['id'],
                title=x['name'],
                author=x['owner']['display_name'],
                image_url=next((y for y in sorted(x['images'], key=lambda i: i['height'])), {}).get('url')
            )
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
                artists=[Artist(a['id'], a['name']) for a in x['artists']],
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
                artists=[Artist(a['id'], a['name']) for a in x['track']['artists']],
                album=x['track']['album']['name'],
                image_url=sorted(x['track']['album']['images'], key=lambda i: i['height'])[0]['url'],
                preview_url=x['track']['preview_url']
            )
            for x in items
        ]

    def get_audio_features(self, tracks: List[Track]) -> Dict[str, AudioFeatures]:
        batches = [tracks[i:i + 100] for i in range(0, len(tracks), 100)]
        result = {}
        token = self.__get_token()
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.__get_audio_features, batch, token) for batch in batches]
            for future in as_completed(futures):
                result.update(future.result())
        return result

    def __get_audio_features(self, tracks: List[Track], token: str) -> Dict[str, AudioFeatures]:
        return {
            x['id']: AudioFeatures(
                acousticness=x['acousticness'],
                danceability=x['danceability'],
                energy=x['energy'],
                instrumentalness=x['instrumentalness'],
                liveness=x['liveness'],
                loudness=x['loudness'],
                speechiness=x['speechiness'],
                valence=x['valence']
            )
            for x in self.__get(
                '/v1/audio-features',
                {'ids': ','.join([x.id for x in tracks])},
                token
            ).get('audio_features', [])
            if x
        }

    def get_recommendations(self, seed_tracks: List[Track], target_features: AudioFeatures,
                            batch_size: int = 5) -> List[Track]:
        shuffle(seed_tracks)
        batches = [seed_tracks[i:i + batch_size] for i in range(0, len(seed_tracks), batch_size)]
        token = self.__get_token()
        recommendations = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.__get_recommendations, batch, target_features, token) for batch in batches]
            for future in as_completed(futures):
                recommendations.extend(future.result())
        return [x for x in recommendations if x not in seed_tracks and x.preview_url]

    def __get_recommendations(self, seed_tracks: List[Track], target_features: AudioFeatures,
                              token: str) -> List[Track]:
        response = self.__get(
            '/v1/recommendations',
            {
                'seed_tracks': ','.join([x.id for x in seed_tracks]),
                'limit': 100,
                **{f'target_{k}': v for k, v in target_features.__dict__.items() if v}
            },
            token
        )
        return [
            Track(
                id=t['id'],
                title=t['name'],
                artists=[Artist(a['id'], a['name']) for a in t['artists']],
                album=t['album']['name'],
                image_url=next((t for t in sorted(t['album']['images'], key=lambda i: i['height'])), {}).get('url'),
                preview_url=t['preview_url']
            )
            for t in response['tracks']
        ]

    @staticmethod
    def __get(path: str, params: dict, token: str = None) -> dict:
        return Spotify.__get_full(f'https://api.spotify.com{path}?{parse.urlencode(params)}', token)

    @staticmethod
    def __get_full(url: str, token: str = None) -> dict:
        if not token:
            token = Spotify.__get_token()
        response = requests.get(
            url,
            headers={
                'Authorization': f'Bearer {token}'
            }
        )
        if response.status_code == 404:
            return {}
        if 400 <= response.status_code <= 403:
            raise SpotifyUnauthorized(response.status_code, response.json())
        if response.status_code >= 500:
            raise Exception(response.text)
        return response.json()

    @staticmethod
    def __get_token() -> str:
        return g.get("token")
