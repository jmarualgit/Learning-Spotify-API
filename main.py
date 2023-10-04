# things to install:
# pip install python-dotenv OR python -m pip install {} OR python3 -m pip install {}
    # to easily load in environment variables
# pip install requests

# importing dotenv package
from dotenv import load_dotenv

# importing os module
import os

# call the function and load the environment variables
# make sure .env file is in the same directory as this python file
load_dotenv()

# load in CLIENT_ID and CLIENT_SECRET
# .getenv gets the value of an environment variable
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# print them out; make sure env variables loaded in
# print(client_id, client_secret)