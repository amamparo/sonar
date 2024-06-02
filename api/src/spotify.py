import base64
import json
import urllib
from concurrent.futures import ThreadPoolExecutor, as_completed
from math import ceil, floor
from random import shuffle
from urllib import parse
from typing import List, Dict

import requests
from flask import g
from injector import singleton

from src.env import Environment
from src.models import Track, AudioFeatures, Artist, Playlist
from src.spotify_unauthorized import SpotifyUnauthorized


@singleton
class Spotify:
    @staticmethod
    def get_refresh_token(code: str, redirect_uri: str) -> dict:
        return Spotify.__token_request({
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': urllib.parse.unquote(redirect_uri)
        })

    @staticmethod
    def refresh_access_token(refresh_token: str) -> dict:
        return Spotify.__token_request({
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        })

    @staticmethod
    def __token_request(data: dict) -> dict:
        authorization = f'Basic {base64.b64encode(
            Environment.spotify_client_id.encode() + b':' + Environment.spotify_client_secret.encode()
        ).decode('utf-8')}'
        return requests.post(
            'https://accounts.spotify.com/api/token',
            data=data,
            headers={
                'Authorization': authorization,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        ).json()

    def export_playlist(self, name: str, track_ids: List[str]) -> None:
        user_id = self.__get('/v1/me')['id']
        playlist_id = self.__post(f'/v1/users/{user_id}/playlists', data={
            'name': name,
            'public': False,
            'description': 'Exported from Discoverify' # TODO: rename this app
        })['id']
        batches = [track_ids[i:i + 100] for i in range(0, len(track_ids), 100)]
        for batch in batches:
            self.__post(f'/v1/playlists/{playlist_id}/tracks', data={
                'uris': [f'spotify:track:{x}' for x in batch]
            })

    def get_tracks(self, track_ids: List[str]) -> List[Track]:
        batch_size = 50
        batches = [track_ids[i:i + batch_size] for i in range(0, len(track_ids), batch_size)]
        track_map = {}
        token = self.__get_access_token()
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.__get_tracks, batch, token) for batch in batches]
            for future in as_completed(futures):
                track_map.update(future.result())
        return [track_map[x] for x in track_ids if x in track_map]

    def __get_tracks(self, track_ids: List[str], token: str) -> Dict[str, Track]:
        as_list = [
            self.__to_track(x) for x in
            self.__get('/v1/tracks', {'ids': ','.join(track_ids)}, token=token).get('tracks', [])
        ]
        return {x.id: x for x in as_list}

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
        return [self.__to_track(x) for x in tracks]

    def get_playlist_tracks(self, playlist_id) -> List[Track]:
        initial_response = self.__get(f'/v1/playlists/{playlist_id}/tracks', {
            'limit': 100
        })
        items = initial_response.get('items', [])
        next_url = initial_response.get('next')
        while next_url:
            next_response = self.__request('GET', next_url)
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
        token = self.__get_access_token()
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.__get_audio_features, batch, token=token) for batch in batches]
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
                tempo=x['tempo'],
                valence=x['valence']
            )
            for x in self.__get(
                '/v1/audio-features',
                {'ids': ','.join([x.id for x in tracks])},
                token
            ).get('audio_features', [])
            if x
        }

    def get_recommendations(self, seed_track_ids: List[str]) -> List[Track]:
        shuffle(seed_track_ids)
        batch_count = ceil(len(seed_track_ids) / 5)
        batch_size = floor(len(seed_track_ids) / batch_count)
        batches = [seed_track_ids[i:i + batch_size] for i in range(0, len(seed_track_ids), batch_size)]
        incomplete_batch = next((x for x in batches if len(x) < batch_size), None)
        if incomplete_batch:
            batches.remove(incomplete_batch)
            for i, x in enumerate(incomplete_batch):
                batches[i].append(x)
        token = self.__get_access_token()
        recommendation_scores: Dict[Track, int] = {}
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.__get_recommendations, batch, token=token) for batch in batches]
            for future in as_completed(futures):
                for i, recommendation in enumerate(future.result()):
                    recommendation_scores[recommendation] = recommendation_scores.get(recommendation, 0) + (100 - i)
        recommendations = [
            x[0] for x in sorted(list(recommendation_scores.items()), key=lambda t: t[1], reverse=True)
            if x[0].id not in seed_track_ids and x[0].preview_url
        ]
        features = self.get_audio_features(recommendations)
        for recommendation in recommendations:
            recommendation.features = features.get(recommendation.id)
        return [x for x in recommendations if x.features]

    def __get_recommendations(self, seed_track_ids: List[str], token: str) -> List[Track]:
        response = self.__get(
            '/v1/recommendations',
            {
                'seed_tracks': ','.join(seed_track_ids),
                'limit': 100
            },
            token
        )
        return [self.__to_track(t) for t in response.get('tracks', [])]

    @staticmethod
    def __to_track(x: dict) -> Track:
        return Track(
            id=x['id'],
            title=x['name'],
            artists=[Artist(a['id'], a['name']) for a in x['artists']],
            album=x['album']['name'],
            image_url=sorted(x['album']['images'], key=lambda i: i['height'])[0]['url'],
            preview_url=x['preview_url']
        )

    @staticmethod
    def __get(path: str, params: dict = None, token: str = None) -> dict:
        return Spotify.__request('GET', f'https://api.spotify.com{path}?{parse.urlencode(params or {})}', token=token)

    @staticmethod
    def __post(path: str, data: dict, token: str = None) -> dict:
        return Spotify.__request('POST', f'https://api.spotify.com{path}', data=data, token=token)

    @staticmethod
    def __request(method: str, url: str, data: dict = None, token: str = None) -> dict:
        if not token:
            token = Spotify.__get_access_token()
        response = requests.request(
            method,
            url,
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            },
            data=json.dumps(data) if data else None
        )
        if response.status_code == 404:
            return {}
        if 401 <= response.status_code <= 403:
            raise SpotifyUnauthorized(response.status_code, response.json())
        if response.status_code >= 500:
            raise Exception(response.text)
        return response.json()

    @staticmethod
    def __get_access_token() -> str:
        return g.get("access_token")
