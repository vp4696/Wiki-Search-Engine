import glob
from collections import defaultdict
from heapq import heapify, heappush, heappop
import os
import timeit
import sys

index_files = glob.glob("./[0-9]*.txt")

heap = []
index_word = {}
filePointers = {}
line_no = 0
invertedIndex = defaultdict()
index_files.sort()
current_row = {}

# <---- Where sorted indexes will be stored ---->

folderToStore = "/home/viviek/Desktop/Run1/Index/"

# <---- Total files created after sorting and merging indexes ---->
file_no = 1

# <---- Total indexes in a file ---->
index_in_a_file = 200000

start = timeit.default_timer()

for i in range(len(index_files)):
	try:
		filePointers[i] = open(index_files[i],"r")
	except:
		print ("Could Open Files: ")

	current_row[i] = filePointers[i].readline().strip().split("=")

	while current_row[i][0] and current_row[i][0] in heap:
		index_word[current_row[i][0]] += "," + current_row[i][1]
		current_row[i] = filePointers[i].readline().strip().split("=")

	if current_row[i][0]:
		heappush(heap,current_row[i][0])
		index_word[current_row[i][0]] = current_row[i][1]

fileName = folderToStore + "index" + str(file_no) + ".txt"
file_p = open(fileName,"w")


# <---- Secondary index for the sorted index file ---->
secondary_Index = folderToStore + "/secondaryIndex.txt"
s_i = open(secondary_Index,"w")

while len(heap) > 0:
	line_no += 1
	word = heappop(heap)
	toWrite = word + "=" + index_word[word] + "\n"
	file_p.write(toWrite)			
	index_word.pop(word)

	if(line_no == 1):
		toWrite = word + " " + fileName + "\n"
		s_i.write(toWrite)

	for i in range(len(index_files)):
		if current_row[i][0] == word:

			current_row[i] = filePointers[i].readline().strip().split("=")

			while current_row[i][0] and current_row[i][0] in heap:
				index_word[current_row[i][0]] += "," + current_row[i][1]
				current_row[i] = filePointers[i].readline().strip().split("=")

			if current_row[i][0]:
				heappush(heap,current_row[i][0])
				index_word[current_row[i][0]] = current_row[i][1]

	if line_no == index_in_a_file:
		file_no += 1
		line_no = 0
		file_p.close()
		fileName = folderToStore + "index" + str(file_no) + ".txt"
		print(file_no," created\n")
		file_p = open(fileName,"w")

stop = timeit.default_timer()

print ("Time for Merging:",stop-start,"sec")