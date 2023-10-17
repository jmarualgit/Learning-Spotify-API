
# import modules
from auth import get_auth_header
from requests import get
import json

def create_empty_playlist(token, user_id):
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    header = get_auth_header(token)