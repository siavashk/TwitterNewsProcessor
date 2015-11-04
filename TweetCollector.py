import tweepy

from tinydb import TinyDB, where

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import string
import re
import time
from datetime import datetime

import threading


class TweetCollector(object):
    def __init__(self, agencies, token, token_secret, consumer, consumer_secret):
        self.agencies = agencies
        self.access_token = token
        self.access_token_secret = token_secret
        self.consumer_key = consumer
        self.consumer_secret = consumer_secret
        self._refresh = 10 * 60
        self._tweets = TinyDB('./tweets.json')
        self._tweets.purge()
        self._auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self._auth.set_access_token(self.access_token, self.access_token_secret)
        self._api = tweepy.API(self._auth)

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def _status(self, handle):
        try:
            user = self._api.get_user(handle)
        except tweepy.TweepError as e:
            print('Tweeter server error ', e.response, ' for handle: ', handle)
            return []

        if hasattr(user, 'status'):
            return user.status
        else:
            return []

    @staticmethod
    def _process(status):
        clean_status = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', status._json['text'],
                               flags=re.MULTILINE)

        clean_status = re.sub('@[\w.]+', '', clean_status, flags=re.MULTILINE)

        tokenized_docs = word_tokenize(clean_status)

        regex = re.compile('[%s]' % re.escape(string.punctuation))

        tokenized_docs_no_punctuation = []

        for token in tokenized_docs:
            new_token = regex.sub(u'', token)
            if not new_token == u'':
                if new_token not in stopwords.words('english') and new_token != 'RT' and new_token != '...':
                    tokenized_docs_no_punctuation.append(new_token)

        status._json['tokens'] = tokenized_docs_no_punctuation

        return status

    def _single_execute(self):
        print(datetime.now().time())
        for agency in self.agencies.search(where('handle')):
            tweeter_handle = agency['handle']
            status = self._status(tweeter_handle)
            if status:
                status_p = self._process(status)
                if not self._tweets.search(where('id') == status_p._json['id']) or not self._tweets.all():
                    self._tweets.insert(status_p._json)
            else:
                continue

    def run(self):
        while True:
            self._single_execute()
            time.sleep(self._refresh)