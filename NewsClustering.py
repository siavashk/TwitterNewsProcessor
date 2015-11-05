from tinydb import TinyDB
import threading
import time
from datetime import datetime

import nltk
from nltk.stem.snowball import SnowballStemmer

import re
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.externals import joblib

from sklearn.manifold import MDS

import matplotlib.pyplot as plt


class NewsClustering(object):
    def __init__(self, tweets, method, history, delay, refresh):
        self._tweets = TinyDB(tweets)
        self._method = method
        self._nclusters = 5  # TO-DO: remove hard-coded number of clusters
        self._history = history
        self._delay = delay
        self._refresh = refresh
        self._stemmer = SnowballStemmer("english")

        self._vectorizer = []
        self._vocabulary = []
        self._tfidf_matrix = []
        self._distance = []
        self._document = []
        self._frame = []
        self._vocab_frame = []

        self._km = []
        self._clusters = []

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        time.sleep(self._delay)
        thread.start()

    def tokenize_and_stem(self, text):
        # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
        tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
        for token in tokens:
            if re.search('[a-zA-Z]', token):
                filtered_tokens.append(token)
        stems = [self._stemmer.stem(t) for t in filtered_tokens]
        return stems

    @staticmethod
    def tokenize_only(text):
        # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
        tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
        for token in tokens:
            if re.search('[a-zA-Z]', token):
                filtered_tokens.append(token)
        return filtered_tokens

    def _preprocess(self):
        document = []
        for element in range(len(self._tweets) - self._history, len(self._tweets)):
            tw = self._tweets.get(eid=element)
            document.append(' '.join(tw['tokens']))

        # not super pythonic, no, not at all.
        # use extend so it's a big flat list of vocab
        totalvocab_stemmed = []
        totalvocab_tokenized = []
        for i in document:
            allwords_stemmed = self.tokenize_and_stem(i) # for each item in 'synopses', tokenize/stem
            totalvocab_stemmed.extend(allwords_stemmed) # extend the 'totalvocab_stemmed' list

            allwords_tokenized = self.tokenize_only(i)
            totalvocab_tokenized.extend(allwords_tokenized)

        self._vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)
        print('there are ' + str(self._vocab_frame.shape[0]) + ' items in vocab_frame')

        return document

    def _kmeans(self):
        print('entering kmeans')
        # Define vectorizer parameters
        self._vectorizer = TfidfVectorizer(tokenizer=self.tokenize_and_stem)

        # Fit the vectorizer to the news
        self._tfidf_matrix = self._vectorizer.fit_transform(self._document)
        self._vocabulary = self._vectorizer.get_feature_names()
        self._distance = 1 - cosine_similarity(self._tfidf_matrix)

        self._km = KMeans(n_clusters=self._nclusters)

        self._km.fit(self._tfidf_matrix)

        self._clusters = self._km.labels_.tolist()

        joblib.dump(self._km,  'doc_cluster.pkl')

        self._km = joblib.load('doc_cluster.pkl')

        self._clusters = self._km.labels_.tolist()

        news = {'Tweets': self._document, 'cluster': self._clusters}
        self._frame = pd.DataFrame(news, index=[self._clusters], columns=['cluster'])

        print("Top terms per cluster:")
        print()
        # sort cluster centers by proximity to centroid
        order_centroids = self._km.cluster_centers_.argsort()[:, ::-1]

        # TO-DO: Remove hard-coded cluster colors
        cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e'}

        # TO-DO: Remove hard-coded cluster names
        cluster_names = {0: '0',
                         1: '1',
                         2: '3',
                         3: '4',
                         4: '4'}

        for i in range(self._nclusters):
            print("Cluster %d words:" % i, end='')

            cluster_name = []
            for ind in order_centroids[i, :6]: # replace 6 with n words per cluster
                word = str('%s' % self._vocab_frame.ix[self._vocabulary[ind].split(' ')].values.tolist()[0][0])
                cluster_name.append(word)
            print(cluster_name)
            cluster_names[i] = cluster_name
            print()
            print()

        print('Number of tweets per news cluster:', self._frame['cluster'].value_counts())

        MDS()

        # convert two components as we're plotting points in a two-dimensional plane
        # "precomputed" because we provide a distance matrix
        # we will also specify `random_state` so the plot is reproducible.
        mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)

        pos = mds.fit_transform(self._distance)  # shape (n_components, n_samples)

        xs, ys = pos[:, 0], pos[:, 1]
        df = pd.DataFrame(dict(x=xs, y=ys, label=self._clusters))

        # group by cluster
        groups = df.groupby('label')

        # set up plot
        fig, ax = plt.subplots(figsize=(17, 9)) # set size
        ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling

        # iterate through groups to layer the plot
        # note that I use the cluster name and color dicts with the 'name' lookup to return the appropriate color/label

        for name, group in groups:
            ax.plot(group.x, group.y, marker='o', linestyle='', ms=12,
                    label=cluster_names[name], color=cluster_colors[name],
                    mec='none')
            ax.set_aspect('auto')
            ax.tick_params(\
                axis= 'x',          # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom='off',      # ticks along the bottom edge are off
                top='off',         # ticks along the top edge are off
                labelbottom='off')
            ax.tick_params(\
                axis= 'y',         # changes apply to the y-axis
                which='both',      # both major and minor ticks are affected
                left='off',      # ticks along the bottom edge are off
                top='off',         # ticks along the top edge are off
                labelleft='off')

        ax.legend(numpoints=1)  # show legend with only 1 point

        # add label in x,y position with the label as the film title
        for i in range(len(df)):
            ax.text(df.ix[i]['x'], df.ix[i]['y'], '', size=8)

        t = datetime.now().time()
        plt.savefig(str(t) + '_clusters.png', dpi=200)

    def run(self):
        self._document = self._preprocess()
        while True:
            #if self._method == 'kmeans':
            self._kmeans()
            time.sleep(self._refresh)