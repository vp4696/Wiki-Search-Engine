
In order to run:

1)

bash current_folder/index.sh xml_file_name current_folder/inverted_index current_folder/invertedindex_stat.txt

where,
xml_file_name ---------------------> wikipedia dump file
current_folder/inverted_index ------------> folder where inverted index file will be stored
current_folder/invertedindex_stat.txt ----> inverted index stat file


2)

bash current_folder/search.sh current_folder/inverted_index/ t:World Cup i:2019 c:Cricket
bash current_folder/search.sh current_folder/inverted_index/ World Cup 2019 Cricket
