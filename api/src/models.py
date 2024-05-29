from dataclasses import dataclass
from typing import Optional


@dataclass
class AudioFeatures:
    acousticness: float
    danceability: float
    energy: float
    instrumentalness: float
    liveness: float
    speechiness: float
    valence: float


@dataclass
class Track:
    id: str
    title: str
    artist: str
    album: str
    image_url: str
    preview_url: str
    features: Optional[AudioFeatures] = None

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id
