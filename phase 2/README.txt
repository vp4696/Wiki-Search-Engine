There are in total 3 files used :

1) parse_index.py -
--> In order to create inverted index file, you need to run this file. 

--> This file takes 2 parameters: a) path where index files need to be stored.
             			  b) stat file, which will contain total # of tokens before processing and after processing.

--> After running this file you will get:
				  a) indexes with posting list (a file contains indexes of 25000 articles).
				  b) id to article title mapping file (a file contains 25000 article titles).



2) index_merger.py -
--> This file will merge indexes from the files and will store the indexes in sorted manner in files, i.e. primary index file(a file contains 500000 indexes).

--> And it will also create secondary index file ( which will contain index to the primary index files).



3) search_query.py - 
--> This file will take input query.txt file and give output query_out.txt.

--> In this file we will load the index from secondary index files and id to title from id-to-title mapping file.



4) stop_words.txt - This file is used to remove stop words from the wikipedia article text.
