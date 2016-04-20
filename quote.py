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

punctuation = [".", "!", "?", ")", "]", "\"", "'", "\u201D"]
prefixes = ['dr', 'vs', 'mr', 'mrs','ms' ,'prof', 'inc','jr','f.b.i','i.e']
def parse(argv):

    found_text=0    
    
    text=""
    r  = requests.get(argv)
    data = r.text
    soup = BeautifulSoup(data,from_encoding='utf8')
    paras = soup.find_all('p')
    img= soup.find_all('img')
                
    allQuotes=[]
    allSen = []
    merge=[]  
    for para in paras:
        text=para.get_text()
        text.encode('utf-8')

        sentences= []
        quotes= []
        
        lastBegin=0
        nextBegin=0 
        lastSpace=0
        inQuote= False
        quoteStart = 0
        lastCap=0
        spaceQ=0

        wasQ= False
        hadQ=False
        mightMer=False

        
            
        for i in range(len(text)):
            if i == nextBegin:
                lastBegin=i
            c=text[i]
            if c== " ":
                lastSpace=i
                if inQuote:
                    spaceQ+=1
            elif c=="." and (text[lastSpace+1:i].lower() in prefixes or i-lastCap<2 or i-lastSpace<2):
                do=0
                #continue
            elif c== "." or c=="!" or c=="?" or c==";":
                j=i
                while j<len(text) and text[j] in punctuation:
                    j+=1
                s = text[lastBegin:j]
                sentences.append(s)
                nextBegin= j
                #print str(hadQ)+"-----"
                hadQ=False
                if wasQ:
                    hadQ=True
                wasQ=False
            elif c == "\"":
                if inQuote>0:
                    q= text[quoteStart:i+1]
                    #print str(quoteStart)+ " - ascii end"
                    inQuote=False
                    if spaceQ>3:
                        if mightMer:
                            merge.append(len(quotes)+len(allQuotes))
                        quotes.append(q)
                    spaceQ=0
                    if not (nextBegin>i):
                        wasQ=True
                    mightMer=False
                else:
                    inQuote=True
                    quoteStart=i
                    #print str(quoteStart)+" - " +str(lastBegin)+"  //  "+ str(hadQ)
                    if quoteStart-lastBegin<2 and hadQ:
                        mightMer=True

            elif c==u'\u201c':
                inQuote=True
                quoteStart=i
                #print str(quoteStart)+" - " +str(lastBegin)+"  //  "+ str(hadQ)
                if quoteStart-lastBegin<2 and hadQ:
                    mightMer=True
            elif c==u'\u201d':
                q= text[quoteStart:i+1]
                    #print str(quoteStart)+ " - ascii end"
                inQuote=False
                if spaceQ>3:
                    if mightMer:
                        merge.append(len(quotes)+len(allQuotes))
                    quotes.append(q)
                spaceQ=0
                if not (nextBegin>i):
                    wasQ=True
                mightMer=False
            elif ord(c)>64 and ord(c)<91:
                lastCap = i
        #pp.pprint(quotes)
        if len(quotes)>=1:
            allQuotes+=quotes
        if len(sentences)>=1:
            allSen+=sentences
        #pp.pprint(sentences)
    #print merge

    for i in merge:
        q1=allQuotes[i-1]
        q2=allQuotes[i]
        punc=q1[len(q1)-2]
        q1=q1[:len(q1)-2]
        if punc == ",":
            punc= "."
        qFin= q1 +punc+ " "+ q2[1:]
        allQuotes[i-1]=qFin
    mod=0
    for i in merge:
        allQuotes.pop(i+mod)
        mod-=1

    #for s in allSen:
        #score = 0
        #for e in personal:
            #if



    pp.pprint(allQuotes)







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


    return allQuotes,final_image
#parse('http://www.huffingtonpost.com/entry/david-cameron-dodgy_us_570bf446e4b0885fb50dc004')
#parse('http://www.huffingtonpost.com/entry/ted-cruz-gold-standard-republican_us_571196bfe4b06f35cb6fbac6?cps=gravity_2425_-8385480002285021224')

#parse('http://www.theblaze.com/stories/2016/04/12/trump-blasts-rnc-chairman-reince-priebus-should-be-ashamed-of-himself/')