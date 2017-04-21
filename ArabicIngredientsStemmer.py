# -*- coding: utf-8-sig -*-
import pandas as pd 
import numpy as np 
import re
from difflib import SequenceMatcher


class ArabicIngredientsStemmer:


    pattern = re.compile('[\u0627-\u064a]')

    
    def __init__(self, prices):
        self.stop_words = pd.read_csv('stopwordsAR.txt', header=None,encoding="utf-8")[0].tolist()
        self.ItemCorpus = []
        self.ItemCorpusDict = []
        self.extractNamesPrices(prices)
 
    #http://languagelog.ldc.upenn.edu/myl/ldc/morph/buckwalter.html
    def cleanArabicString(self, inp):
        # ، بال وبال ال
        out = " ".join(re.findall(r'[\u0621-\u0652]+', inp))
        out = out.replace(u'،',' ')
        out = out.replace(u'ء',' ')

        out = out.replace(' \u0628 ',' ')#/ و /
        
        out = out.replace('\u0622','\u0627')#آ
        out = out.replace('\u0623','\u0627')#أ
        out = out.replace('\u0625','\u0627')#إ
    
        out = out.replace('\u0629','\u0647')#ة
        out = out.replace('\u0649','\u064A')#ي

        out = out.replace(' \u0628 ',' ')#/ و /
        out = out.replace(' \u0627\u0628 ',' ')#/ او /
        out = out.replace(u'ال',' ')
        out = out.replace(u'لل',' ')
        #out = out.replace('\u0624','')#ؤ
        #out = out.replace('\u0648',' ')#و
        #out = out.replace('\u0628','')#ب
        out = out.replace('\u0647','')#ه
        return out
    
    
    def extractNamesPrices(self, prices): 
        """ extract names from prices and store in shared ItemCorpus """

        for item in prices:
            itemTxt = self.cleanArabicString(item)

            for comp in itemTxt.split():
                if self.pattern.match(comp) != None and len(comp)>2:
                    self.ItemCorpus.append(comp)
                    self.ItemCorpusDict.append({"word":comp,"id":item})
            del itemTxt  
        self.ItemCorpus = (set(self.ItemCorpus))

        return self.ItemCorpus 
    


    def extractNamesIngredients(self, recipes):
        """ extract names from ingredients and return it as a list of words """
        ingrdsCorpus = []
        for ingrds in recipes["ingrd"]:
            for ingrd in ingrds:
                ingrdTxt = self.cleanArabicString(ingrd["n"])
                for comp in ingrdTxt.split():
                    if self.pattern.match(comp) != None and len(comp)>2 and comp not in self.stop_words:
                        ingrdsCorpus.append(comp)
                del ingrdTxt 
        ingrdsCorpus = (set(ingrdsCorpus))
        return ingrdsCorpus
    
    def search(self, word):
        result = []
        for p in self.ItemCorpusDict:
            if p['word'] == word:
                result.append(p["id"])
        return result
    
    def machIngredItmPrice(self, ingrdsCorpus):
        """ mach Ingredients with Item price """

        names = []
        found = []
        for i in ingrdsCorpus:
            if i not in self.ItemCorpus:
                names.append(i) 
            else:
                found.append(i)

    
        names=list(set(names))

        for word in names:
            for item in self.ItemCorpus:
                if SequenceMatcher(None, word, item).ratio()>0.9:
                    found.append(item)
                break
        Items=[]
        for word in set(names+found):
            f=self.search(word)
            if(len(f)>0):
                Items= Items + self.search(word)
       
       
        return list(set(Items))