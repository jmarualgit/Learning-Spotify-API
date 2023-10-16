# things to install:
# pip install python-dotenv OR python -m pip install {} OR python3 -m pip install {}
    # to easily load in environment variables
# pip install requests


# import modules
from auth import get_token
from artist import *
from songs import *

# allows to send get requests
from requests import get

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

#song_key = track_analysis["track"]["key"]               
# "key" gets the key of the track; it's a scale from -1 to 11 where 0 = C, 1 = C#, etc.; -1 = no key detected
# rewritten using the function
song_key = get_key(track_analysis["track"]["key"])

print(song_key)
# print(get_artist_genres(token, artist_id))

artist_seeds = [];
artist_seeds.append(artist_id)

recs = get_recommendations_by_artists(token, artist_seeds, 5)
for i in range(5):
    print(f"{i + 1}. {recs[i]['name']} by {recs[i]['artists'][0]['name']}")