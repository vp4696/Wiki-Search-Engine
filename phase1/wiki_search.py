import sys
import re
import timeit
from nltk.stem import PorterStemmer


start_time = timeit.default_timer()

port_stemmer = PorterStemmer()
stopwords = set()

field=['t:','b:','i:','c:','e:']

with open("stop_words.txt", 'r') as ff:
    for word in ff:
        word = word.strip()
        stopwords.add(word)

invertedIndexdict = {}

inverted_file_path=sys.argv[1]
query=sys.argv[2:]

queryy=None
queryy=' '.join(query)

def cleanList_PrintPosting(Qlist, isField):
	if(isField==False):
		text=" "
		txt=text.join(Qlist)
		txt = txt.lower()
		
		# RegEx to remove <..> tags from text!!!
		a_r=r'<(.*?)>'
		angular_removal=re.compile(a_r, re.DOTALL)
		txt=angular_removal.sub('', txt)
		
	    # RegEx to remove Punctuation!!!
		p_r=r'[.,;_()/\"\'\=]'
		punct=re.compile(p_r, re.DOTALL)
		txt=punct.sub(' ', txt)
		
		n_a_r=r'[^\x00-\x7F]+'
		non_ascii_removal=re.compile(n_a_r, re.DOTALL)
		txt=non_ascii_removal.sub(' ', txt)
		
		words=txt.split()
		token=[]
		for word in words:
			if word not in stopwords:
				token.append(word.strip())

		for word in token:
			word=re.sub(r'[\ \.\-\:\&\$\!\*\+\%\,\@]+',"",word)
			word=port_stemmer.stem(word)
			if word in invertedIndexdict:
				print(word,"---->",invertedIndexdict[word])
				print()
				print()
		# print(token)
	if(isField==True):
		for word in Qlist:
			tag=word[:2]
			tag = tag[::-1] 
			word=word[2:]
			txt=list(word.split(' '))
			while("" in txt):
				txt.remove("")

			text=" "
			txt=text.join(txt)
			txt = txt.lower()
			
			# RegEx to remove <..> tags from text!!!
			a_r=r'<(.*?)>'
			angular_removal=re.compile(a_r, re.DOTALL)
			txt=angular_removal.sub('', txt)
			
		    # RegEx to remove Punctuation!!!
			p_r=r'[.,;_()/\"\'\=]'
			punct=re.compile(p_r, re.DOTALL)
			txt=punct.sub(' ', txt)
			
			n_a_r=r'[^\x00-\x7F]+'
			non_ascii_removal=re.compile(n_a_r, re.DOTALL)
			txt=non_ascii_removal.sub(' ', txt)
			
			words=txt.split()

			token=[]
			for word in words:
				if word not in stopwords:
					token.append(word.strip())
			for word in token:
				word=re.sub(r'[\ \.\-\:\&\$\!\*\+\%\,\@]+',"",word)
				word=port_stemmer.stem(word)
				if word in invertedIndexdict:
					st=""
					st=str(invertedIndexdict[word])
					if st.count(str(tag)):
						print(word,"---->",invertedIndexdict[word])
						print()
						print()						

def getPostingList(Qlist, isField):
	global invertedIndexdict, inverted_file_path
	inverted_file_path=inverted_file_path+"/inverted_index.txt"
	with open(inverted_file_path,'r') as ff:
		c=0
		for line in ff:
			lst=line.split('=')
			article=lst[0]
			postings=lst[1]
			postings=postings.split(',')
			postt=[]
			for pp in postings:
				pp=pp.split()
				postt.append(pp)
			postings = [item for p in postt for item in p]
			invertedIndexdict[article]=postings
	# print(len(invertedIndexdict))
	if(isField==False):
		# print(Qlist)
		cleanList_PrintPosting(Qlist,isField)

	if(isField==True):
		# print(Qlist)
		cleanList_PrintPosting(Qlist,isField)

def splitQuery(isField):
	global queryy, inverted_file_path
	Qlist=[]
	if isField==True:
		st=""
		c=0
		for i in reversed((queryy)):
			st=str(st)+str(i)
			if(i==':'):
				c=1
				continue
			if(c==1):
				st = st[::-1] 
				Qlist.append(st)
				c=0
				st=""
		# print(Qlist)
	else:
		Qlist=queryy.split(' ')
		# print(Qlist)	
	getPostingList(Qlist,isField)



if __name__ == '__main__':
	# global queryy, field
	print()
	print("Posting list is of the form:")
	print("no1:b2#c1#i5, no2:t5#b2"," -----> ","where no1=article number, b2=the word appears twice in body of article,c1=the word appears twice in category of article, AND # is the delimeter")
	print()
	isField=False
	for i in field:
		if i in queryy:
			isField=True
			break
	splitQuery(isField)
	stop_time = timeit.default_timer()
	print("Querying time: ", stop_time-start_time)