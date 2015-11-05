################################
# Twitter News Processor 	   #
################################

###############################################################################

--------------------------------
1 WHAT DOES THE PACKAGE CONTAIN?
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
2 KNOWN DEPENDENCIES
--------------------------------

The code was developed and tested with Python 3.4.3 in Ubuntu 14.0.4 using Pycharm.
The following packages were used:

1. tinydb 2.4
2. nltk 3.0
3. sklrean 0.16
4. pandas 0.17
5. matplotlib 1.5.0

