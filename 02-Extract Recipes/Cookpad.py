
# coding: utf-8

# In[ ]:

import warnings
import sys
import requests
from io import StringIO, BytesIO
import re
from six import u
from bs4 import BeautifulSoup
import json
import pandas as pd
import gc


from datetime import datetime
warnings.filterwarnings("ignore")
today = datetime.utcnow().isoformat()


# In[ ]:

requestSession = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Referer': 'https://cookpad.com/eg/%D9%88%D8%B5%D9%81%D8%A7%D8%AA',
    'Turbolinks-Referrer': 'https://cookpad.com/eg/%D9%88%D8%B5%D9%81%D8%A7%D8%AA',
    'X-Turbolinks-Request': 'true',
    'Accept': 'text/html, application/xhtml+xml',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'en-US,en;q=0.8,ar;q=0.6'
    }
def spider(url):
   
    r = requestSession.get(url=url, headers=headers, verify=False, timeout=(3.05, 27))
    r.raise_for_status()
    
    page = r.text
    soup = BeautifulSoup(page, 'html.parser')
    recipi_name = soup.find('h1',{'class':"recipe-show__title recipe-title strong field-group--no-container-xs"}).text.strip()
    author_name = soup.find('span', attrs={'itemprop':"author"}).text.strip()
    author_url = 'https://cookpad.com' + soup.find('span', attrs={'itemprop':"author"}).parent['href']
    recipi_id = soup.find('div', attrs={'class':'bookmark-button '})['id'].replace('bookmark_recipe_','')
    try:
        recipi_image = [x['src'] for x in soup.findAll('img',{'alt':'Photo'})][0]
    except:
        recipi_image = ''
    
    recipi_likes = soup.find('span', attrs={'class':'field-group__hide subtle'}).text.strip()

    
    #recipi_image = recipi_image_div.find('a',{'data-target':'#modal'})["href"]
    recipi_ingredients = []
    index = 1
    for i in soup.find_all('li',{'class':'ingredient '}):
        if i.text.strip() != '':
            recipi_ingredients.append({'in':index, 'n':i.text.strip()})
            index = index + 1
        
    index = 1
    recipi_instructions = []
    for i in soup.find_all('li',{'class':'step numbered-list__item card-sm'}):
        step = i.find('p').text.strip()
        try:
            imageUrl = [x['src'] for x in i.findAll('img')][0]
        except:
            imageUrl = ''    
        recipi_instructions.append({'in':index,'txt':step,'img':imageUrl})
        del step
        del imageUrl
        index = index + 1 
        
    recipi_tags = []    
    for i in soup.find_all('ul',{"class":'list-inline'}):
        for x in i.find_all('a'):
            recipi_tags.append(x.text.strip())
        break 
    likes=0
    try:
        likes = (0, int(recipi_likes.strip()))[len(recipi_likes.strip())>0]
    except:
        likes = 0
    recipe = {}
    recipe["n"] = recipi_name
    recipe["src"] = url
    recipe["rcpe_id"] = recipi_id
    recipe["ingrd"] = recipi_ingredients
    recipe["instrct"] = recipi_instructions
    recipe["img"] = recipi_image
    recipe["auth"] = {'n':author_name,'src':author_url} 
    recipe["tags"] = recipi_tags
    recipe["likes"] = likes
    recipe["pub"] = today
    recipe["etag"] = r.headers['ETag']
    
    del r, page, soup, recipi_name, author_name, author_url, recipi_id, likes
    del recipi_image, recipi_likes, recipi_ingredients, index
    del recipi_tags, recipi_instructions
    
    return recipe

def saveToFile(data,fileName):
    with open(fileName, 'w', encoding="utf-8") as fo:
        json.dump(data, fo, ensure_ascii=False)
        fo.flush()

    


# In[ ]:

counter = 1
data=[]

with open("links.txt") as f:
    for line in f:
        try:
            #print('{}:{}'.format(counter, line))
            data.append(spider(line))
            counter = counter + 1
            print(counter)
            if(counter % 1000 == 0):
                print(counter)
                saveToFile(data, 'output/test{}.json'.format(counter))
                del data [:]
                print(gc.collect())
        except:
            print ("Unexpected error:", sys.exc_info())
            counter = counter - 1
            continue
    print(counter)
    saveToFile(data, 'output/test{}.json'.format(counter))
    del data [:]
    print(gc.collect())            
        
          


# In[ ]:




# In[ ]:



