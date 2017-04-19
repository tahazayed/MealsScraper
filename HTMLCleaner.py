# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 00:23:42 2017

@author: taha.amin
"""
import pandas as pd
from bs4 import BeautifulSoup#, Tag, element
import re
import nltk
import numpy as np



from nltk.corpus import stopwords
#from nltk.stem.porter import PorterStemmer
from nltk.tokenize import wordpunct_tokenize
#nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}',"'", ' ','\t','\n','\r','_','+']) # remove it if you 

"""
MostEnglishWords = EnglishDF[0].tolist()
stop_words.update(MostEnglishWords)
del EnglishDF

TechnicalTagsDF = pd.read_csv('TechnicalTags', header=None)
TechnicalTags = TechnicalTagsDF[0].tolist()
del TechnicalTagsDF
"""
#Most_English_Words = set(stopwords.words('MostEnglishWords'))
#stop_words.update(Most_English_Words)
#stackoverflow tags
#TechnicalTags = set(stopwords.words('TechnicalTags'))


def parse_html(html_doc):
    """returns a string of parsed html with all stop words removed"""
    try:
        if html_doc == np.NaN:
            return np.NaN
        else:
            soup = BeautifulSoup(html_doc, 'html.parser')
            list_of_words = [i for i in wordpunct_tokenize(
            re.sub(r'\d+|[^\w\s]', '', (soup.text.lower()))) if i not in stop_words and i.strip() !=''  ]
            list_of_words = list(set(list_of_words))
            list_of_words.sort()
            return ' '.join(map(lambda x: "%s" % x, list_of_words))
    except TypeError:
        return np.NaN    
       