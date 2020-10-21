## Wiki-Search-Engine

The mini project involves building a search engine on the Wikipedia Data Dump without using any external index. For this project, we use the data dump of size ~40 GB. The search results return in real time. Multi-word and multi-field search on Wikipedia Corpus is implemented.

Here we will rank the documents and display the top k relevant documents. Relevance ranking algorithm is implemented using TF-IDF score to rank documents.


### Prerequisites:

1. Python3
2. For preprocessing and Stemming, nltk library is used.
3. To install nltk pip3 install nltk.
4. For parsing wikipedia dump xml file sax parser is used.
5. stop_words.txt file must be present in the same directory to remove stop words.

### Types of Queries

Normal query - Any sequence of simple words is considered a normal query eg: “Sachin Tendulkar”

Field query - Assuming that fields are small letters(b, i, c, t, r, e) followed by colon and the fields are space separated. eg: “b:sachin i:2003 c:sports”
