import json
from bs4 import BeautifulSoup
import requests
import re
import sys
from nltk import sent_tokenize
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
import pprint

pp = pprint.PrettyPrinter(indent=4)
DictQuote={}
final_quote=""
final_image=""
def parse(argv):

    found_text=0    
    
    text=""
    r  = requests.get(argv)
    data = r.text
    soup = BeautifulSoup(data,from_encoding='utf8')
    para = soup.find_all('p')
    img= soup.find_all('img')

    #Look for block quotes
    blockQuote= soup.find_all('aside', { "class" : "pullquote" })
    for line in blockQuote:
        if found_text==0:
            final_quote=line.get_text()
            if len(final_quote)>90 and len(final_quote)<350:
                found_text=1
                
            
    for line in para:
        lines=line.get_text()
        text=text+lines
        text.encode('utf-8')
   
    text = text.replace('?"', '? "').replace('!"', '! "').replace('."', '" . ').replace('Advertisement','').replace('ADVERTISEMENT','')
    # REGEX to remove <dot><capital letter> to <dot><space><capital letter> as this was not took care by sentence toeknizer
    text=re.sub(r'(\.)+([A-Z]+)',"".join(r'\1 \2'),text)
    #to add more abbrevations to our sentence tokenizer
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs','ms' ,'prof', 'inc','jr','f.b.i','i.e'])
    sentence_splitter = PunktSentenceTokenizer(punkt_param)
    sentences = sentence_splitter.tokenize(text)
    

    #To print all the individual sentences found in the Paragraph
    # for line in sentences:
    #     # if len(line)>50 and len(line)<500:
    #     print line
    #     print "*************"
    dictionary=[]
    # For no duplicacy of sentences
    unique_sentences=[]
    for line in sentences:
        if line not in unique_sentences:
            unique_sentences.append(line)
    for line in unique_sentences:
        # print(line)
        score=0
        if len(line)>50 and len(line)<400:
            if "I " in line :
                if  line.find("\"")!= -1 or line.find(u"\u201C")!= -1:
                    # print "IN  I AND "" "
                    # print line 
                    if '_' in line:
                        score=score+3
                    if ':' in line:
                        score=score+3
                    if ';' in line:
                        score=score+3
                    if line.count(',')>1:
                        score=score+3  
                    if ',' in line:
                        score=score+3  
                    else:
                        score=score+3

        if len(line)>50 and len(line)<400:
            if "I " in line :
                # print "IN  I :  "
                # print line 
                if '_' in line:
                    score=score+2
                if ':' in line:
                    score=score+2
                if ';' in line:
                    score=score+2
                if line.count(',')>1:
                    score=score+2  
                if ',' in line:
                    score=score+2

        if len(line)>50 and len(line)<400:
            if line.find("\"")!= -1 or line.find(u"\u201C")!= -1:
                # print "IN  quote :  "
                # print line 
                if '_' in line:
                    score=score+2
                if ':' in line:
                    score=score+2    
                if ';' in line:
                    score=score+2  
                if line.count(',')>1:
                    score=score+2   
                if ',' in line:
                    score=score+2

        if ';' in line and len(line)>50 and len(line)<400:
            # print "IN  ; :  "
            # print line 
            score=score+1

        if line.count(',')>1 and len(line)>50 and len(line)<400:
            # print "IN  , many  :  "
            # print line 
            score=score+1

        if ',' in line and len(line)>50 and len(line)<400:
            # print "IN  , one :  "
            # print line 
            score=score+1

        dictionary.append([score,line])
# .encode('ascii', 'xmlcharrefreplace')

    best_quotes=[]
    quotes=[]
    dictionary.sort(key=lambda x:x[0], reverse=True)


#Selecting scored lines which have the best scores
    for score,line in dictionary:
        if score>=10 :
            quotes.append([score,line])

    if len(quotes)>=5:
        # itertools.islice(quotes, 0, 5)
        best_quotes=quotes[0:5]
    else:
        for score,line in dictionary:
            if  score>=5:
                quotes.append([score,line])
        if len(quotes)>=5:
            best_quotes=quotes[0:5]
        else:
            best_quotes=quotes
    

    # pp.pprint(best_quotes)
    my_quotes = [i[1] for i in best_quotes]
    pp.pprint(my_quotes)
    # print "********************"

# GET THE IMAGE
    
    found_img=0
    stri=""
    for i in img:
        stri=i.get('src')
        #print(str)
        if stri is not None:
            images=stri.split(" ")
            if found_img==0:
                for image in images:
                    if found_img==0:
                        if "icon" not in image:
                            if "contributors" not in image:
                                if "jpg" in image or "png" in image:
                                    final_image=image
                                    # print final_image
                                    found_img=1
    
    
    # print final_image
    
    
    return my_quotes,final_image
