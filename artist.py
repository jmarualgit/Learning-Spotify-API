
# imports
from auth import get_auth_header
from requests import get
import json

# function to search for an artist
def search_for_artist(token, artist_name):
    
    # taken from spotify web api documentation
    url = "https://api.spotify.com/v1/search"
    
    headers = get_auth_header(token)
    
    # construct a query for the search api endpoint 
        # type - list of things looking for
            # can do "artist,track"
        # limit = 1 - gives the first person that pops up
    query = f"?q={artist_name}&type=artist&limit=1"
    
    # combine together
    query_url = url + query
    
    result = get(query_url, headers=headers)
    
    # parse
    # ["artists"]["items"] - what we want
    json_result = json.loads(result.content)["artists"]["items"]
    
    #print(json_result)
    
    # if length of json_result = 0
    if len(json_result) == 0:
        print("No artist with this name exists")
        return None
    
    # otherwise, return the very first result
    return json_result[0]

def get_artist_genres(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)['genres']

    return json_result