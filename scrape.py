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
                
    allSen=[]
       
    for para in paras:
        text=para.get_text()
        text.encode('utf-8')

        sentences= []
        quotes= []
        lastBegin=0
        lastSpace=0
        inQuote= False
        quoteStart = 0
        lastCap=0
        spaceQ=0

        hadQ= False
        for i in range(len(text)):
            c=text[i]
            if c== " ":
                lastSpace=i
                if inQuote:
                    spaceQ+=1
            elif c=="." and (text[lastSpace+1:i].lower() in prefixes or i-lastCap<2 or i-lastSpace<2):
                do=0
                #continue
            elif c== "." or c=="!" or c=="?":
                while i<len(text) and text[i] in punctuation:
                    i+=1
                s = text[lastBegin:i]
                sentences.append(s)
                lastBegin= i
            elif c == "\"":
                if inQuote>0:
                    q= text[quoteStart:i+1]
                    #print str(quoteStart)+ " - ascii end"
                    inQuote=False
                    if spaceQ>3:
                        quotes.append(q)
                    spaceQ=0
                else:
                    inQuote=True
                    quoteStart=i

            elif c==u'\u201c':
                inQuote=True
                quoteStart=i
            elif c==u'\u201d':
                q= text[quoteStart:i+1]
                inQuote=False
                #print "uni end"
                if spaceQ>2:
                        quotes.append(q)
                spaceQ=0
            elif ord(c)>64 and ord(c)<91:
                lastCap = i
        #pp.pprint(quotes)
        if len(quotes)>=1:
            allSen+=quotes
        #pp.pprint(sentences)
    pp.pprint(allSen)







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


    return allSen,final_image
#parse('http://www.huffingtonpost.com/entry/david-cameron-dodgy_us_570bf446e4b0885fb50dc004')


parse('http://www.theblaze.com/stories/2016/04/12/trump-blasts-rnc-chairman-reince-priebus-should-be-ashamed-of-himself/')
    
