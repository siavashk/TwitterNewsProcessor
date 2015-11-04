from TweetCollector import TweetCollector
from tinydb import TinyDB
import time

agencies = TinyDB('./agencies.json')

access_token = "3277141898-WELaKWCU5QBq179cg7skxkOl3ikssi3F52qbdpp"
access_token_secret = "0vDCR1HOuN7jLxJszkr45xndYxDb8HSi1AFvJ7ThOr77a"
consumer_key = "vv6eotv6Rcv5IpKVqShjP6xEx"
consumer_secret = "yyUoxFTQazGFbNo1xxyyiJ9vqlQJGMxiSlqqGvro4xs9GpxEiB"

input('Press enter to start the tweet collector. Afterwards press enter to quit:\n')
dc = TweetCollector(agencies, access_token, access_token_secret, consumer_key, consumer_secret)

input('')