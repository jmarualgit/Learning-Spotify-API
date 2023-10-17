
# imports
from auth import SpotifyClient
from requests import get
import json

class Track:

    def __init__(self, name, id, artist):
        """
        Constructor for track object

        :param name (str): track name
        :param id (int): Spotify track id
        :param artist (str): Artist who created the track
        """
        self.name = name
        self.id = id
        self.artist = artist

    def __str__(self):
        return f"{self.name} by {self.artist}"

    def create_spotify_uri(self):
        return f"spotify:track:{self.id}"

    def get_songs_by_artists(token, artist_id):
        
        # /artists/ - looking for a specific artist
        # {artist_id} - passing in specific artist id
        # top-tracks - want the top tracks
            # ?country=US - need to pass in a country to use to rank top tracks
        url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
        
        headers = SpotifyClient.get_auth_header(token)
        
        result = get(url, headers=headers)
        
        # parse into json
        json_result = json.loads(result.content)["tracks"]
        
        return json_result

    # analyzing a given track
    def analyze_track(token, track_id):
        
        url = f"https://api.spotify.com/v1/audio-analysis/{track_id}"
        
        headers = SpotifyClient.get_auth_header(token)
        
        result = get(url, headers=headers)
        
        
        json_result = json.loads(result.content)
        
        return json_result

    # generates recommendations from up to 5 artists
    # 1 <= track_limit <= 100
    def get_recommendations_by_artists(token, artist_ids, track_limit):
        url = f"https://api.spotify.com/v1/recommendations?limit={track_limit}&seed_artists="

        # append ids to artist seed
        for idx, id in enumerate(artist_ids):
            if idx != 0:
                url += "%2C"
            url += id

        print(url)
        headers = SpotifyClient.get_auth_header(token)
        result = get(url, headers = headers)
        json_result = json.loads(result.content)["tracks"]

        return json_result


    def get_key(numberOfKey):
        
        # match is similar to "switch" in java
        match numberOfKey:
            case -1:
                print("No key found")
            case 0:
                return "C"
            case 1:
                return "C#/Db"
            case 2:
                return "D"
            case 3:
                return "D#/Eb"
            case 4:
                return "E"
            case 5:
                return "F"
            case 6:
                return "F#/Gb"
            case 7:
                return "G"
            case 8:
                return "G#/Ab"
            case 9:
                return "A"
            case 10:
                return "A#/Bb"
            case 11:
                return "B"

