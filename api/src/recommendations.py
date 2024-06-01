from dataclasses import dataclass
from random import shuffle
from typing import List

from injector import singleton, inject

from src.models import Track
from src.spotify import Spotify


@dataclass
class Recommendations:
    recommendations: List[Track]


@singleton
class RecommendationsService:
    @inject
    def __init__(self, spotify: Spotify):
        self.__spotify = spotify

    def get_recommendations(self, track_ids: List[str]) -> List[Track]:
        return self.__get_recommendations(track_ids)

    def __get_recommendations(self, track_ids: List[str]) -> List[Track]:
        tracks = self.__get_recommended_tracks(track_ids)
        features = self.__spotify.get_audio_features([t.id for t in tracks])
        for track in tracks:
            track.features = features.get(track.id)
        return [t for t in tracks if t.features]

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

