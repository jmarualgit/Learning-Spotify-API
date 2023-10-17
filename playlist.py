
# import modules
from auth import get_auth_header
from requests import get
import json

class Playlist:

    def __init__(self, name, id):
        """
        Constructor for Playlist object

        :param name (str): Playlist name
        :param id (int): Spotify playlist id
        """

    def __str__(self):
        return f"Playlist: {self.name}"

    def create_empty_playlist(token, user_id):
        url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
        header = get_auth_header(token)