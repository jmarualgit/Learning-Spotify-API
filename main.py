# things to install:
# pip install python-dotenv OR python -m pip install {} OR python3 -m pip install {}
    # to easily load in environment variables
# pip install requests

# importing dotenv package
from dotenv import load_dotenv

# importing os module
import os

# a built in module to use for encoding
import base64

# allows to send post requests (and to get)
from requests import post, get

# import json module
import json

# call the function and load the environment variables
# make sure .env file is in the same directory as this python file
load_dotenv()

# load in CLIENT_ID and CLIENT_SECRET
# .getenv gets the value of an environment variable
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# print them out; make sure env variables loaded in
# print(client_id, client_secret)

# using client credentials flow works; there is another workflow for user credentials (for users using)
# how it works:
    # send in client_id, client_secret, and grant_type to spotify accounts service
    # returns an access_token
    # can send requests to WEB API using access_token
    # requests to get info about artists, tracks, playlists, etc.

# function to get token
def get_token():
    
    # authorization string (encoded w base 64)
    
    # concatenate client_id to client_secret
    auth_string = client_id + ":" + client_secret
    
    # encode with a base 64 encoding
    auth_bytes = auth_string.encode("utf-8")
    
    # base64.b64encode(auth_bytes) returns a base64 object
    # convert to string to pass with headers to send request to accounts service API
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    # url to send request to
    url = "https://accounts.spotify.com/api/token"
    
    # headers are associated with requests
    headers = {
        
        # sending in authorization data to make sure everything is correct and will send back
        "Authorization": "Basic " + auth_base64,     # make sure to type correctly
        
        # specify type of content (sometimes usually JSON application)
        "Content-Type": "application/x-www-form-urlencoded"
        
    }

    data = {"grant_type": "client_credentials"}     # grant type = client_credentials
    
    result = post(url, headers=headers, data=data)  # data is like the body of the request
    
    # will be returned JSON data in field .content
    # need to convert to python string
    json_result = json.loads(result.content)      # loads() = load from string; loading from result.content
    
    # parse token
    token = json_result["access_token"]
    
    # return token
    return token

# function to instruct header whenever sending a request
# use this whenever making a request
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

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

def get_songs_by_artists(token, artist_id):
    
    # /artists/ - looking for a specific artist
    # {artist_id} - passing in specific artist id
    # top-tracks - want the top tracks
        # ?country=US - need to pass in a country to use to rank top tracks
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    
    headers = get_auth_header(token)
    
    result = get(url, headers=headers)
    
    # parse into json
    json_result = json.loads(result.content)["tracks"]
    
    return json_result

# call the token and store it in a variable
token = get_token()

# print the token
# print(token)

# search for artist then put into result variable
    # if gives {'error': {'status': 404, 'message': 'Service not found'}}
    # then forgot a "?" when making query variable in search_for_artist
result = search_for_artist(token, "Crystal Castles")

# print result
#print(result)
    # this will print everything
    #*****use this to look at possible filters (i think i saw one about genres)*****

# print just the name
#print(result["genres"])
    # prints out "AC/DC" (without the quotations)

# get the ID of the artist
# can look for songs of this artist
artist_id = result["id"]

songs = get_songs_by_artists(token, artist_id)

# idx is what "i, j, and k" are in loops in other languages; idx =~ index
for idx, song in enumerate(songs):
   print(f"{idx + 1}. {song}")

#THIS IS A TEST MATTY PATTY