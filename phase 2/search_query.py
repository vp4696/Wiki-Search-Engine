import sys
import re
import timeit
from nltk.stem import PorterStemmer
from bisect import bisect
import glob
from math import log10

output=open("query_out.txt","w")
# field=['t:','b:','i:','c:','e:']


stopwords=set()

with open("stop_words.txt", 'r') as ff:
    for word in ff:
        word = word.strip()
        stopwords.add(word)

port_stemmer=PorterStemmer()
stemwords={}

id_to_article_title={}
article=0
secondary_index_words=[]

def clean(query):
	global port_stemmer
	txt = query.lower()
	
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
		word=re.sub(r'[\ \.\-\:\&\$\!\*\+\%\,\@]+',"",word)
		if len(word) <= 200 and word.isalnum() and word not in stopwords:
			if word in stemwords.keys():
				tp = stemwords[word]
			else:
				tp = port_stemmer.stem(word)
				stemwords[word] = tp
			if len(tp) > 2:
				token.append(tp)
	return token

def FieldQuery(k,query):
	# print("FQ",query.rstrip())
	output.write("Given Query: "+query.rstrip()+"\n")
	index_to_words=dict(list())
	post_list={}
	article_weight={}
	word_tag=dict(list())

	Qlist=[]
	st=""
	c=0
	for i in reversed((query)):
		st=str(st)+str(i)
		if(i==':'):
			c=1
			continue
		if(c==1):
			st = st[::-1] 
			Qlist.append(st)
			c=0
			st=""
	
	for t in Qlist:
		t=t.rstrip();
		tag, word = t.split(":")
		tokens=clean(word)
		# print(tag," ",tokens)
		for q in tokens:
			if q in word_tag:
				word_tag[q].append(tag)
			else:
				word_tag[q]=[tag]

			secondary_loc=bisect(secondary_index_words, q)
			# path_index_f="/media/viviek/2650746350743B9D/IRE_PROJECT/phase_2/index/index"+str(secondary_loc)+".txt"
			path_index_f="/home/viviek/Desktop/Run1/Index/index"+str(secondary_loc)+".txt"

			if path_index_f in index_to_words:
				if q not in index_to_words[path_index_f]:
					index_to_words[path_index_f].append(q)
			else:
				index_to_words[path_index_f]=[q]

	for f_path,word in index_to_words.items():
		with open(f_path,'r') as f:
			for line in f:
				line=line.rstrip("\n")
				w,p_list=line.split("=",1)
				if w in word:
					post_list[w]=p_list


		for w in word:
			if w in post_list:
				p_list=post_list[w].split(',')
				tfidf=log10(article/len(p_list))

				for a_article in p_list:
					a_article_no, val=a_article.split(":")
					article_tag_freq=val.split("#")
					word_freq=0
					for tag in article_tag_freq:
						t=tag[0]
						fq=int(tag[1:])
						if t in word_tag:
							if t=="t":
								word_freq = word_freq + (fq*500)
							elif t=="i":
								word_freq = word_freq + (fq*50)
							elif t=="c":
								word_freq = word_freq + (fq*50)
							elif t=="r":
								word_freq = word_freq + (fq*50)
							elif t=="e":
								word_freq = word_freq + (fq*50)
							elif t=="b":
								word_freq = word_freq + (fq*5)
						else:
							word_freq = word_freq + fq

					if a_article_no in article_weight:
						cal=float(log10(1+word_freq))*float(tfidf)
						article_weight[a_article_no]=article_weight[a_article_no]+cal
					else:
						article_weight[a_article_no]=float(log10(1+word_freq))*float(tfidf)

		post_list.clear()
	index_to_words.clear()

	article_weight = sorted(article_weight.items(), key=lambda xx: xx[1], reverse=True)
	cnt=0
	for p_article in article_weight:
		# print("--->",p_article[0]," ",id_to_article_title[p_article[0]])
		output.write(p_article[0]+","+id_to_article_title[p_article[0]]+"\n")
		cnt=cnt+1
		if(cnt == int(k)):
			break


def NormalQuery(k,query):
	output.write("Query::: "+query.rstrip()+"\n")
	# print("Query:::",query.rstrip())
	query=clean(query)

	index_to_words=dict(list())
	post_list={}
	article_weight={}

	for q in query:
		secondary_loc=bisect(secondary_index_words, q)
		# path_index_f="/media/viviek/2650746350743B9D/IRE_PROJECT/phase_2/index/index"+str(secondary_loc)+".txt"
		path_index_f="/home/viviek/Desktop/Run1/Index/index"+str(secondary_loc)+".txt"

		if path_index_f in index_to_words:
			if q not in index_to_words[path_index_f]:
				index_to_words[path_index_f].append(q)
		else:
			index_to_words[path_index_f]=[q]

	for f_path,word in index_to_words.items():
		with open(f_path,'r') as f:
			for line in f:
				line=line.rstrip("\n")
				w,p_list=line.split("=",1)
				if w in word:
					post_list[w]=p_list
		
		# print(post_list)
		for w in word:
			if w in post_list:
				p_list=post_list[w].split(',')
				tfidf=log10(article/len(p_list))

				for a_article in p_list:
					a_article_no, val=a_article.split(":")
					# print(a_article_no,"     ",val)
					article_tag_freq=val.split("#")
					word_freq=0
					for tag in article_tag_freq:
						t=tag[0]
						fq=int(tag[1:])
						# print(t,"     ",fq)
						if t=="t":
							word_freq = word_freq + (fq*500)
						elif t=="i":
							word_freq = word_freq + (fq*50)
						elif t=="c":
							word_freq = word_freq + (fq*50)
						elif t=="r":
							word_freq = word_freq + (fq*50)
						elif t=="e":
							word_freq = word_freq + (fq*50)
						elif t=="b":
							word_freq = word_freq + (fq*5)

					if a_article_no in article_weight:
						cal=float(log10(1+word_freq))*float(tfidf)
						article_weight[a_article_no]=article_weight[a_article_no]+cal
					else:
						article_weight[a_article_no]=float(log10(1+word_freq))*float(tfidf)

		post_list.clear()
	index_to_words.clear()

	article_weight = sorted(article_weight.items(), key=lambda xx: xx[1], reverse=True)

	cnt=0
	for p_article in article_weight:
		# print("--->",p_article[0]," ",id_to_article_title[p_article[0]])
		output.write(p_article[0]+","+id_to_article_title[p_article[0]]+"\n")
		cnt=cnt+1
		if(cnt == int(k)):
			break

if __name__ == '__main__':

	# path="/media/viviek/2650746350743B9D/IRE_PROJECT/phase_2/"	
	# path="/home/viviek/Desktop/Run1/"	
	print("Storing article_no to title in dict --->")
	article_no_title = glob.glob("/home/viviek/Desktop/Run1/articleno_with_name"+"[0-9]*.txt")
	article_no_title.sort()
	for i in article_no_title:
		try:
			ll=open(i,'r')
			for line in ll:
				line=line.rstrip("\n")
				id_no, title=line.split("#",1)
				id_to_article_title[id_no]=title
				article=article+1
			ll.close()
		except Exception as ex:
			print("Article-Title File not found")
			print(ex)
			sys.exit(1)
	print("<---Storing done")
	# print(len(id_to_article_title))
	print()

	# path_of_index="/media/viviek/2650746350743B9D/IRE_PROJECT/phase_2/index/"
	path_of_index="/home/viviek/Desktop/Run1/Index/"
	print("Storing secondary index --->")
	try:
		with open(path_of_index+"secondaryIndex.txt",'r') as p:
			for line in p:
				line=line.split(' ')
				secondary_index_words.append(line[0])
	except Exception as ex:
		print("Secondary Index File not found")
		sys.exit(1)
	print("<---Storing done")
	print()
	print("<<<< -------- Query processing.... -------- >>>>")	
	with open("query.txt",'r') as q:
			for qr in q:
				start_time=timeit.default_timer()
				k,qr=qr.split(',',1)
				if ':' in qr:
					FieldQuery(k,qr)
				else:
					NormalQuery(k,qr)
				stop_time = timeit.default_timer()
				tt=stop_time-start_time
				# print(tt, tt/int(k))
				sq=tt/int(k)
				tt=str(tt)
				sq=str(sq)
				output.write(tt+","+sq+"\n\n")
	output.close()
	print("<<<< -------- Query Processing Done -------- >>>>")
	print("Check query_out.txt for output!!!")