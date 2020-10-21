import xml.sax
import re
import timeit
from xml.sax import parse
from xml.sax import ContentHandler
import sys
from nltk.stem import PorterStemmer
from collections import defaultdict
import os
from os import walk
import bz2

if(len(sys.argv)!=3):
    print("Argument should be of the form:\n")
    print("bash parse_index.py wiki_file_path inverted_index_file stat_file")
    sys.exit(1)

print("starting process...")
print("Processing...")


article_limit=25000
tokens_Limit=25000
Inverted_Index_File_No=1
port_stemmer = PorterStemmer()
stem_Map = {}
stopwords = set()
total_words = 0
words_inverted_index = 0

with open("stop_words.txt", 'r') as ff:
    for word in ff:
        word = word.strip()
        stopwords.add(word)

dummy, indexfile, statfile = sys.argv
#dummy-------->kuchbhi
#indexfile---->folder to store inverted index file
#statfile----->count of the words before and after processing

#multi-level dictionary to store index__words
#FORMAT::::dictionary ---> word : { articleID_1:{t1:cnt, b1:cnt}, articleID_2:{t1:cnt, b1:cnt} }
invertedIndexdict = defaultdict(lambda: defaultdict(lambda: defaultdict(int))) 


#Regular Expressions
#DOTALL -----> The DOTALL flag allows dot to match newlines as well.
meta__re1 = re.compile(r"[~`!@#$}\\<>%\-^*+{\[\]\|/?,]", re.DOTALL)
cat__re2 = r'\[\[category:(.*?)\]\]'

info = r'{{infobox(.*?)}}'
info__re3 = re.compile(info, re.DOTALL)

ref = r'== ?references ?==(.*?)=='
ref__re4 = re.compile(ref, re.DOTALL)

mixx__re5 = re.compile(r"[~`!@#$%\-^*+{\[}\]\|\\<>/?,]", re.DOTALL)

# RegEx to remove Numbers!!!
num = re.compile(r"\b[0-9]+[0-9]*[a-z]+[a-z0-9][a-z0-9]*\b", re.DOTALL)

less_than_four = re.compile(r"\b[0-9]{1,3}\b", re.DOTALL)
more_than_four = re.compile(r"\b[0-9]{5,}\b", re.DOTALL)
mixx = re.compile(r"\b[0-9][0-9][0-9][0-9]+[a-z]*\b\|\b[0-9][0-9][0-9][a-z]\b\|\b[0-9][0-9][a-z]\b||\b[0-9]*[a-z]\b", re.DOTALL)


def inverted_Index_File_Append(wordList, articleID, t):
    global words_inverted_index
    for word in wordList:
        word = word.strip()
        word = re.sub(r'[\ \.\-\:\&\$\!\*\+\%\,\@]+',"",word)
        if len(word) >= 3 and len(word) <= 200:
            if word not in stopwords:
                if word not in stem_Map.keys():
                    stem_Map[word]=port_stemmer.stem(word)
                word=stem_Map[word]

                if word in invertedIndexdict:
                    if articleID in invertedIndexdict[word]:
                        if t in invertedIndexdict[word][articleID]:
                            invertedIndexdict[word][articleID][t]=invertedIndexdict[word][articleID][t]+1
                        else:
                            invertedIndexdict[word][articleID][t]=1
                    else:
                        invertedIndexdict[word][articleID]={t: 1}
                else:
                    words_inverted_index=words_inverted_index+1
                    invertedIndexdict[word]=dict({articleID: {t: 1}})

#<<<<---- Cleaning the text ---->>>>
def cleanLine(text):
    # RegEx to remove <..> tags from text!!!
    a_r=r'<(.*?)>'
    angular_removal=re.compile(a_r, re.DOTALL)
    text=angular_removal.sub('', text)

    # RegEx to remove Punctuation!!!
    p_r=r'[.,;_()/\"\'\=]'
    punct=re.compile(p_r, re.DOTALL)
    text=punct.sub(' ', text)

    # RegEx to remove {{cite **}} or {{vcite **}}!!!
    c_r=r'{{v?cite(.*?)}}'
    cite_removal=re.compile(c_r, re.DOTALL)
    text=cite_removal.sub('', text)
    
    # RegEx to remove [[file:]]
    f_r=r'\[\[file:(.*?)\]\]'
    file_removal=re.compile(f_r, re.DOTALL)
    text = file_removal.sub('', text)
    
    # RegEx to remove Non ASCII characters!!!
    n_a_r=r'[^\x00-\x7F]+'
    non_ascii_removal=re.compile(n_a_r, re.DOTALL)
    text=non_ascii_removal.sub(' ', text)
    return text


#<<<<---- Processing the title ---->>>>
def processTitle(text, articleID):
    global path_to_index, total_words
    text = text.lower()
    total_words=total_words+len(text.split())
    
    text = cleanLine(text)

    meta__re1.sub(' ', text)
    words=text.split()
    token=[]
    for word in words:
        if word not in stopwords:
            # total_words=total_words+1
            token.append(word.strip())
    inverted_Index_File_Append(token, articleID, "t")

#<<<<---- Processing the text ---->>>>
def processText(text, articleID):
    global path_to_index, total_words, Inverted_Index_File_No

    info__box = []
    categories = []
    external = []
    references = []

    text = text.lower()
    total_words=total_words+len(text.split())
    
    text = cleanLine(text)

    external_link_Ind = 0
    category_Ind = len(text)

    categories = re.findall(cat__re2, text, flags=re.MULTILINE)

    lines = text.split('\n')
    flag = 1

    #<<<<---- Infobox calculation ---->>>>
    lines_no=len(lines)
    for i in range(lines_no):
        if '{{infobox' in lines[i]:
            flag=0
            temp=lines[i].split('{{infobox')[1:]
            info__box.extend(temp)
            while True:
                if(i >= len(lines)):
                    break
                
                if '{{' in lines[i]:
                    count = lines[i].count('{{')
                    flag=flag+count
                
                if '}}' in lines[i]:
                    count = lines[i].count('}}')
                    flag=flag-count
                
                if flag <= 0:
                    break
                i=i+1
                
                if(i < len(lines)):
                    info__box.append(lines[i])
        if flag <= 0:
            text='\n'.join(lines[i+1:])
            break
    


    #<<<<---- External Link Index calculation ---->>>>            
    try:
        external_link_Ind = text.index('==external links==')
        external_link_Ind=external_link_Ind+20
    except:
        pass

    if external_link_Ind == 0:
        try:
            external_link_Ind = text.index('== external links ==')
            external_link_Ind=external_link_Ind+22
        except:
            pass
    
    #<<<<---- Categories Index calculation ---->>>>                        
    try:
        category_Ind = text.index('[[category:')
    except:
        pass


    #<<<<---- External link and References calculation ---->>>>                        
    if external_link_Ind != 0:
        external = text[external_link_Ind:category_Ind]
        external = re.findall(r'\[(.*?)\]', external, flags=re.MULTILINE)

    references = re.findall(ref, text, flags=re.DOTALL)

    if external_link_Ind != 0:
        text = text[0:external_link_Ind-20]


    #<<<<---- Body text processing ---->>>>                        
    text=ref__re4.sub('', text)
    text=mixx__re5.sub(' ', text)
    text=num.sub('', text)
    text=less_than_four.sub('', text)
    text=more_than_four.sub('', text)
    text=mixx.sub('', text)
    # print(text)
    # print()
    words=text.split()


    #<<<<---- Infobox text processing ---->>>>                        
    token__List=[]
    for info__List in info__box:
        # token__List=[]
        token__List=re.findall(r'\d+|[\w]+', info__List, re.DOTALL)
        token__List=' '.join(token__List)
        token__List=mixx__re5.sub(' ', token__List)
        token__List=num.sub('', token__List)
        token__List=less_than_four.sub('', token__List)
        token__List=more_than_four.sub('', token__List)
        token__List=mixx.sub('', token__List)
        token__List=token__List.split()


    #<<<<---- External links text processing ---->>>>                        
    external=' '.join(external)
    external=mixx__re5.sub(' ', external)
    external=num.sub('', external)
    external=less_than_four.sub('', external)
    external=more_than_four.sub('', external)
    external=mixx.sub('', external)
    external=external.split()


    #<<<<---- Category text processing ---->>>>                        
    categories=' '.join(categories)
    categories=mixx__re5.sub(' ', categories)
    categories=num.sub('', categories)
    categories=less_than_four.sub('', categories)
    categories=more_than_four.sub('', categories)
    categories=mixx.sub('', categories)
    categories=categories.split()


    #<<<<---- References text processing ---->>>>                        
    references=' '.join(references)
    references= mixx__re5.sub(' ', references)
    references=num.sub('', references)
    references=less_than_four.sub('', references)
    references=more_than_four.sub('', references)
    references=mixx.sub('', references)
    references=references.split()


    #<<<<---- Storing to Inverted Index File ---->>>>                        
    inverted_Index_File_Append(words, articleID, "b")
    inverted_Index_File_Append(token__List, articleID, "i")
    inverted_Index_File_Append(external, articleID, "e")
    inverted_Index_File_Append(categories, articleID, "c")
    inverted_Index_File_Append(references, articleID, "r")

    # print(articleID)
    if articleID % tokens_Limit == 0:
        f = open(indexfile +'/'+str(Inverted_Index_File_No)+'.txt', "w")
        for key, val in sorted(invertedIndexdict.items()):
            s = str(key)+"="
            for k, v in sorted(val.items()):
                s += str(k) + ":"
                for k1, v1 in v.items():
                    s = s + str(k1) + str(v1) + "#"
                s = s[:-1]+","
            f.write(s[:-1]+"\n")
        f.close()
        invertedIndexdict.clear()
        stem_Map.clear()
        Inverted_Index_File_No += 1


##<<<<---- Article names into a file ---->>>>                        
# article_to_title = open("./articleno_with_name.txt", "w")
article_to_title=[]

##<<<<---- Total words::: 1) before processing and  2) InvertedIndex File ---->>>>                        
stat = open(statfile, "w")


def write(article_to_title,Article_File_No):
    f = open(indexfile+'/'+"articleno_with_name"+str(Article_File_No)+'.txt', "w")
    for i in article_to_title:
        f.write(i)

titleID=0
articleID=0
flag=False
Article_File_No=1
title=""
buffe=""

class WikiHandler(ContentHandler):
    
    def startElement(self,element,attributes):
        global article_to_title, Article_File_No, titleID, articleID, flag, title, buffe 
        if element == "id" and flag:
            buffe = ""

        if element == "title":
            buffe=""
            flag=True

        if element == "page":
            articleID+=1

        if element == "text":
            buffe=""
    
    def endElement(self,element):
        global article_to_title, Article_File_No, titleID, articleID, flag, title, buffe 
        if element == "title":
            processTitle(buffe, articleID)
            title=buffe
            if(titleID%500==0):
                print(titleID)
            if(titleID%article_limit==0 and titleID!=0):
                print(chr(27) + "[2J")
                write(article_to_title,Article_File_No)
                article_to_title.clear()
                Article_File_No+=1
            titleID+=1
            buffe=""
        elif element == "text":
            processText(buffe, articleID)
            buffe = ""
        elif element == "id" and flag:
            try:
                # article_to_title.write(str(self.articleID)+"#"+self.title+"\n")
                article_to_title.append(str(articleID)+"#"+title+"\n")
            except:
                # article_to_title.write(str(self.articleID)+"#"+self.title.encode('utf-8')+"\n")
                article_to_title.append(str(articleID)+"#"+title.encode('utf-8')+"\n")
            flag=False
            buffe=""
            
    def characters(self,content):
        global buffe 
        buffe=buffe+content

time=open("timetaken.txt","w")

if __name__ == '__main__':
    # start_time = timeit.default_timer()
    mypath="/media/viviek/2650746350743B9D/IRE_PROJECT/Files/"
    f = []

    for (dirpath, dirnames, filenames) in walk(mypath):
        f.extend(filenames)
        break
    cnt=0
    for i in f:
        start_time = timeit.default_timer()
        i=i.replace(" ", "")
        cnt=cnt+1
        wikifile=mypath+i
        parse(wikifile,WikiHandler())
        stop_time = timeit.default_timer()
        ttt=str(stop_time-start_time)
        time.write(ttt+"\n")
        print("\nA file completed!!!\n")

    time.close()
    if not os.path.exists(indexfile):
        os.makedirs(indexfile)
    if(len(invertedIndexdict)!=0):
        f = open(indexfile +'/'+str(Inverted_Index_File_No)+'.txt', "w")
        for key, val in sorted(invertedIndexdict.items()):
            s = str(key)+"="
            for k, v in sorted(val.items()):
                s += str(k) + ":"
                for k1, v1 in v.items():
                    s = s + str(k1) + str(v1) + "#"
                s = s[:-1]+","
            f.write(s[:-1]+"\n")

        f.close()
        invertedIndexdict.clear()
        stem_Map.clear()

    f = open(indexfile+'/'+"articleno_with_name"+str(Article_File_No)+'.txt', "w")
    for i in article_to_title:
        f.write(i)

    # print(total_words)
    # print(words_inverted_index)
    stat.write("Words before processing: "+str(total_words)+"\n")
    stat.write("Words in inverted index file: "+str(words_inverted_index))