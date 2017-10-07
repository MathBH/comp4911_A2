# COMP 4911 Assignment 2: Twitter App
# Tesla Belzile-Ha

import requests
import base64
import json
import sys

# CONSTANTS #

# Console output when user calls the program without arguments
NO_ARGS = 'Missing arguments: please enter a keyword for search'

# Name of file holding credentials
CRED_FILE_NAME = 'cred.txt' # Name of the file containing credentials to read


# MAIN #

# Check if user input args, if not, exit with status 1 and output NO_ARGS prompt
if len(sys.argv) < 2:
   print NO_ARGS
   exit(1)

# Save twitter search argument to string
args = 'q='+ sys.argv[1]

# Check for geocode argument and append to argument string
if len(sys.argv) > 2:
   args = args+'&geocode='+ sys.argv[2]

# Read credentials from file
cred_file = open(CRED_FILE_NAME, 'r')

consumer_key = cred_file.readline().rstrip()
consumer_secret = cred_file.readline().rstrip()

cred_file.close()

# Encode consumer key and secret
credentials = base64.b64encode(consumer_key + ':' + consumer_secret)

# Obtain a bearer token
payload = { 'grant_type': 'client_credentials' }
headers = { 'Authorization': 'Basic ' + credentials, 
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' }

r = requests.post("https://api.twitter.com/oauth2/token", 
                  headers=headers, data=payload)

# Response is JSON data. Decode and display the access token
j = json.loads(r.content)

# With Bearer token, peform searh request
headers = {'Authorization' : 'Bearer '+ j['access_token']}
rr = requests.get("https://api.twitter.com/1.1/search/tweets.json?"+args, headers=headers)
# Decode JSON data
tweets = json.loads(rr.content)

# Display all statuses' screen names and text
for status in tweets['statuses']:
   text = status['text']
   screen_name = status['user']['screen_name']
   print screen_name.upper(), " SAID: ", text.upper(),'\n'
