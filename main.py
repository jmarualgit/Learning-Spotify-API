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

# various variables that can use
artist_id = result["id"]                        # get the ID of the artist; can look for songs of this artist
artist_full_name = result["name"]               # gets the full name of the searched artist (as listed by spotify)
genres = result["genres"]                       # the genres of the artist
follower_count = result["followers"]["total"]   # total # of followers
popularity_percentage = result["popularity"]    # gets the popularity ranking / 100

# tested print statements 
#print("The artist's offical listed name is " + artist_full_name)
#print("The genres associated with the artist are ")
#print(genres)
#print(artist_full_name + " has " + str(follower_count) + " followers.")
#print("Out of a 100, " + artist_full_name + " has a popularity ranking of " + str(popularity_percentage) + ".")

songs = get_songs_by_artists(token, artist_id)

#print(songs[0]['name'])    # to look for a particular song
#print(songs[0]['id'])      # to get the id of a particular track in the top 10

# making an array for song_genres
song_genres = []

# putting the genres of the top 10 songs in an array
for idx, song in enumerate(songs):
    song_genres.append(song['id'])      # gets the id of every song and adds them into the array

#print(song_genres)          # print the ray

# idx is what "i, j, and k" are in loops in other languages; idx =~ index
#for idx, song in enumerate(songs):
    #print(f"{idx + 1}. {song}")            # prints all the info for every song
    #print(f"{idx + 1}. {song['name']}")     # prints the name of every song

# analyzing a given track
def analyze_track(token, track_id):
    
    url = f"https://api.spotify.com/v1/audio-analysis/{track_id}"
    
    headers = get_auth_header(token)
    
    result = get(url, headers=headers)
    
    
    json_result = json.loads(result.content)
    
    return json_result

track_analysis = analyze_track(token, songs[0]['id'])

# prints the result

# the ["track"] part is taken from spotify documentation: https://developer.spotify.com/documentation/web-api/reference/get-audio-analysis
    # can replace with "meta", "bars", "beats", "sections", "segments", and "tatums"
    # these all have their own separate bunch of items to track
#print(track_analysis["track"])

# printing the song title for reference
print(songs[0]['name'])

# getting more specific
# putting it into variables
song_tempo = track_analysis["track"]["tempo"]           # how fast the song is; measured in bpm
song_loudness = track_analysis["track"]["loudness"]     # how loud the song is; measured in decibels

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

#song_key = track_analysis["track"]["key"]               # "key" gets the key of the track; it's a scale from -1 to 11 where 0 = C, 1 = C#, etc.; -1 = no key detected
# rewritten using the function
song_key = get_key(track_analysis["track"]["key"])

print(song_key)