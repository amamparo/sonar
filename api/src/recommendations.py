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

    def get_recommendations(self, seed_tracks: List[Track]) -> List[Track]:
        recommended_tracks = self.__get_recommended_tracks([x.id for x in seed_tracks])
        features = self.__spotify.get_audio_features([t.id for t in recommended_tracks])
        for track in recommended_tracks:
            track.features = features.get(track.id)
        return [t for t in recommended_tracks if t.features]

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

