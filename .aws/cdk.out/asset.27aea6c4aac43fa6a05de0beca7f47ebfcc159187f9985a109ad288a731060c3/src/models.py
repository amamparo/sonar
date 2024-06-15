from dataclasses import dataclass, fields
from math import sqrt
from typing import Optional, List


@dataclass
class AudioFeatures:
    acousticness: Optional[float] = None
    danceability: Optional[float] = None
    energy: Optional[float] = None
    instrumentalness: Optional[float] = None
    liveness: Optional[float] = None
    loudness: Optional[float] = None
    speechiness: Optional[float] = None
    tempo: Optional[float] = None
    valence: Optional[float] = None

    def cosine_similarity(self, that: 'AudioFeatures') -> float:
        this_magnitude = self.__magnitude()
        that_magnitude = that.__magnitude()
        if this_magnitude == 0 or that_magnitude == 0:
            return 0.0
        return self.__dot(that) / (this_magnitude * that_magnitude)

    def __magnitude(self) -> float:
        return sqrt(sum([(getattr(self, field.name) or 0) ** 2 for field in fields(self)]))

    def __dot(self, other: 'AudioFeatures') -> float:
        return sum([(getattr(self, field.name) or 0) * (getattr(other, field.name) or 0) for field in fields(self)])


@dataclass
class Artist:
    id: str
    name: str


@dataclass
class Track:
    id: str
    title: str
    artists: List[Artist]
    album: str
    image_url: str
    preview_url: Optional[str] = None
    features: Optional[AudioFeatures] = None

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


@dataclass
class Playlist:
    id: str
    title: str
    author: str
    image_url: str
