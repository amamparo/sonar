from dataclasses import dataclass
from os import environ

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Environment:
    spotify_client_id: str = environ.get('SPOTIFY_CLIENT_ID')
    spotify_client_secret: str = environ.get('SPOTIFY_CLIENT_SECRET')
