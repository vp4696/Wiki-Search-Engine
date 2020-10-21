
Tested successfully using:

1)

bash 2019201044/index.sh abc.xml-p1p30303 2019201044/inverted_index 2019201044/invertedindex_stat.txt

where,
abc.xml-p1p30303 ---------------------> wikipedia dump file
2019201044/inverted_index ------------> folder where inverted index file will be stored
2019201044/invertedindex_stat.txt ----> inverted index stat file


2)

bash 2019201044/search.sh 2019201044/inverted_index/ t:World Cup i:2019 c:Cricket
bash 2019201044/search.sh 2019201044/inverted_index/ World Cup 2019 Cricket
