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
        shuffle(seed_tracks)
        seed_tracks = seed_tracks[:500]
        seed_features = list(self.__spotify.get_audio_features(seed_tracks).values())
        mean_features = AudioFeatures(**{
            feature.name: sum([getattr(x, feature.name) for x in seed_features]) / len(seed_features)
            for feature in fields(AudioFeatures)
        })
        return self.__spotify.get_recommendations(seed_tracks, mean_features)[:100]
