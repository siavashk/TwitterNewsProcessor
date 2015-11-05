from TweetCollector import TweetCollector
from tinydb import TinyDB
from NewsClustering import NewsClustering

agencies = TinyDB('./agencies.json')

access_token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
access_token_secret = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
consumer_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
consumer_secret = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

input('Press enter to start the tweet collector. Afterwards press enter to quit:\n')
dc = TweetCollector(agencies, access_token, access_token_secret, consumer_key, consumer_secret)

# Surrogate tweets file for demo, since we do not want to wait for tweet database to be populated
# You can change this to ./tweets.json for real application.
tweets_file = './tweets_copy.json'

# Start the clustering after 1 minute to ensure that tweets have been collected, perform clustering every 10 minutes
nc = NewsClustering(tweets=tweets_file, method='kmeans', history=1000, delay=1*60, refresh=10*60)

input('')