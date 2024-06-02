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

    def get_recommendations(self, seed_track_ids: List[str]) -> List[Track]:
        if not seed_track_ids:
            return []
        shuffle(seed_track_ids)
        return self.__spotify.get_recommendations(seed_track_ids[:500])[:100]
