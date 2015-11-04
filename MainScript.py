from TweetCollector import TweetCollector
from tinydb import TinyDB
import time

agencies = TinyDB('./agencies.json')

access_token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
access_token_secret = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
consumer_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
consumer_secret = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

input('Press enter to start the tweet collector. Afterwards press enter to quit:\n')
dc = TweetCollector(agencies, access_token, access_token_secret, consumer_key, consumer_secret)

input('')
