# using client credentials flow works; there is another workflow for user credentials (for users using)
# how it works:
    # send in client_id, client_secret, and grant_type to spotify accounts service
    # returns an access_token
    # can send requests to WEB API using access_token
    # requests to get info about artists, tracks, playlists, etc.

# call the function and load the environment variables
# make sure .env file is in the same directory as this python file
from dotenv import load_dotenv

# importing os module
import os

# a built in module to use for encoding
import base64
import json


# allow to send post requests
from requests import post

load_dotenv()

# load in CLIENT_ID and CLIENT_SECRET
# .getenv gets the value of an environment variable
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# print them out; make sure env variables loaded in
# print(client_id, client_secret)

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


