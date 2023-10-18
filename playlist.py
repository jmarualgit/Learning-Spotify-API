
# import modules
from requests import post
import json

class Playlist:

    def __init__(self, name, id):
        """
        Constructor for Playlist object

        :param name (str): Playlist name
        :param id (int): Spotify playlist id
        """
        self.name = name
        self.id = id

    def __str__(self):
        return f"Playlist: {self.name}"

    def create_playlist(self, token, user_id):
        data = json.dumps({
            "name": self.name,
            "description": "Recommended tracks",
            "public": True
        })

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
        result = post(
            url,
            data = data,
            headers = headers
        )
        json_result = result.json()

        return result