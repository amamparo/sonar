from dataclasses import dataclass
from random import shuffle
from statistics import mean
from typing import List

from injector import singleton, inject

from src.models import AudioFeatures, Track
from src.spotify import Spotify


@dataclass
class Recommendations:
    input_average_features: AudioFeatures
    recommendations: List[Track]


@singleton
class RecommendationsService:
    @inject
    def __init__(self, spotify: Spotify):
        self.__spotify = spotify

    def get_recommendations(self, track_ids: List[str]) -> Recommendations:
        return Recommendations(
            input_average_features=self.__get_average_features(track_ids),
            recommendations=self.__get_recommendations(track_ids)
        )

    def __get_average_features(self, track_ids: List[str]) -> AudioFeatures:
        features = self.__spotify.get_audio_features(track_ids).values()
        return AudioFeatures(
            acousticness=mean(f.acousticness for f in features),
            danceability=mean(f.danceability for f in features),
            energy=mean(f.energy for f in features),
            instrumentalness=mean(f.instrumentalness for f in features),
            liveness=mean(f.liveness for f in features),
            speechiness=mean(f.speechiness for f in features),
            valence=mean(f.valence for f in features)
        )

    def __get_recommendations(self, track_ids: List[str]) -> List[Track]:
        tracks = self.__get_recommended_tracks(track_ids)
        features = self.__spotify.get_audio_features([t.id for t in tracks])
        for track in tracks:
            track.features = features[track.id]
        return tracks

    def __get_recommended_tracks(self, track_ids: List[str]) -> List[Track]:
        shuffle(track_ids)
        batches = [track_ids[i:i + 5] for i in range(0, len(track_ids), 5)]
        results = set()
        for batch_ids in batches:
            recommended_tracks = self.__spotify.get_recommendations(batch_ids)
            for track in recommended_tracks:
                if track.id in track_ids or not track.preview_url:
                    continue
                results.add(track)
                if len(results) == 100:
                    return list(results)
        return list(results)

