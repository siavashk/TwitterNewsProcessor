################################
# Twitter News Processor 	   #
################################

###############################################################################

--------------------------------
A. WHAT DOES THE PACKAGE CONTAIN?
--------------------------------

The code contains two classes used for natural language processing of news 
agency twitter feeds. The code is structured as two services that are run 
asynchronously. The first service, TweetCollector, makes a REST call to 
twitter in order to populate a database tweet of news and relevant information. 
The second service, NewsClustering, performs clustering on the tweets data base 
in order to find the most "interesting" news clusters. Both services are started 
using the MainScript.

In summary, this package contains the following files:

1. A list of twitter handles for news agencies: agencies.json
2. A data collector class: TweetCollector.py
3. A news clustering class: NewsClustering.py
4. Example usage script: MainScript.py

###############################################################################

--------------------------------
B. KNOWN DEPENDENCIES
--------------------------------

The code was developed and tested with Python 3.4.3 in Ubuntu 14.0.4 using Pycharm.
The following packages were used:

1. tinydb 2.4
2. nltk 3.0
3. sklrean 0.16
4. pandas 0.17
5. matplotlib 1.5.0

###############################################################################

--------------------------------
C. KNOWN ISSUES
--------------------------------

1. The twitter handle for Bloomberg News, i.e. Bloombergnews, is no longer 
supported. So TweetCollector returns a 404 error when trying to access it. This
is handled with a try/except block.

2. The simple k-means clustering used is not suitable for this problem, given that 
the "interesting" news cluster is inside the noise cluster. Probably a spectral
clustering method would perform better on this dataset.

3. The algorithm does not return the center of the clusters at the moment, which
corresponds to the best tweet. Rather, the clustering class returns the keywords
for each cluster. This is a straight-forward extension, but I did not implement
it in the interest of submitting the test sooner rather than later.
