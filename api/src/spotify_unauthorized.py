class SpotifyUnauthorized(Exception):
    def __init__(self, status: int, message: str):
        self.__status = status
        self.__message = message

    @property
    def status(self):
        return self.__status

    @property
    def message(self):
        return self.__message

    def __dict__(self):
        return {
            'status': self.__status,
            'message': self.__message
        }
