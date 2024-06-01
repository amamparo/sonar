from dataclasses import dataclass, fields
from random import shuffle
from typing import List

from injector import singleton, inject

from src.models import Track, AudioFeatures
from src.spotify import Spotify


@dataclass
class Recommendations:
    recommendations: List[Track]


@singleton
class RecommendationsService:
    @inject
    def __init__(self, spotify: Spotify):
        self.__spotify = spotify

    def get_recommendations(self, seed_tracks: List[Track]) -> List[Track]:
        if not seed_tracks:
            return []
        seed_features = list(self.__spotify.get_audio_features(seed_tracks).values())
        mean_features = AudioFeatures(**{
            feature.name: sum([getattr(x, feature.name) for x in seed_features]) / len(seed_features)
            for feature in fields(AudioFeatures)
        })
        recommended_tracks = self.__get_recommended_tracks(seed_tracks, mean_features)
        results = []
        features = self.__spotify.get_audio_features(recommended_tracks)
        for track in recommended_tracks:
            track.features = features.get(track.id)
            if track.features:
                results.append(track)

        return sorted(results, key=lambda x: x.features.cosine_similarity(mean_features), reverse=True)[:250]

    def __get_recommended_tracks(self, seed_tracks: List[Track], target_features: AudioFeatures) -> List[Track]:
        shuffle(seed_tracks)
        recommendations = self.__spotify.get_recommendations(seed_tracks, target_features)
        return recommendations
