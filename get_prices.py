# -*- coding: utf-8 -*-
import pandas as pd
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import pickle
import json
from datetime import datetime


vg = 'http://www.agriprice.gov.eg/Search/CategotySearch_Result.aspx?CatId=1'
frt = 'http://www.agriprice.gov.eg/Search/CategotySearch_Result.aspx?CatId=2'
fish = 'http://www.agriprice.gov.eg/Search/CategotySearch_Result.aspx?CatId=3'
basic = 'http://www.agriprice.gov.eg/Search/CategotySearch_Result.aspx?CatId=5'
meat = 'http://www.agriprice.gov.eg/Search/CategotySearch_Result.aspx?CatId=7'
milk = 'http://www.agriprice.gov.eg/Search/CategotySearch_Result.aspx?CatId=8'
seeds = 'http://www.agriprice.gov.eg/Search/CategotySearch_Result.aspx?CatId=11'
suger = 'http://www.agriprice.gov.eg/Search/CategotySearch_Result.aspx?CatId=12'


def make_soup(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers)
    except ConnectionError:
        try:
            r = requests.get(url, headers)
        except ConnectionError:
            return None

    page = r.text
    soup = BeautifulSoup(page, 'html.parser')
    return soup


def parse_data(soup):
    r = []
    t = []
    s = soup.find('tr', attrs={"style": "text-align:center;vertical-align:middle"})
    for i in s.find_next_siblings()[1:]:
        for x in i.find_all('td'):
            r.append(x.text)
        t.append(r)
        r=[]
    return t


def get_href(list_of_roots, names):
    d = defaultdict()
    for i, name in zip(list_of_roots, names):

        s = make_soup(i)
        alist = []
        for i in s.find_all('a', {'style': "text-decoration:none;"}):
            alist.append('http://www.agriprice.gov.eg' + i['href'])
        d[name] = alist
        alist = []
    return d


def make_df(list_of_r):
    # , columns=['item', 'unit', 'min_state', 'min', 'max_state', 'max', 'date'])
    return pd.DataFrame(list_of_r)

def saveToFile(df,fileName):
    data = []
    No_Rows = len(df)
    for i in range(0, No_Rows):
        if(df.iloc[i,5]!='-'):
            ingrd={}
            ingrd["n"]=str.strip(df.iloc[i,1])
            ingrd["gvrnrt"]=str.strip(df.iloc[i,2])
            ingrd["u"]=str.strip(df.iloc[i,3]).replace(" ","")
            if(u'جنيه' in ingrd["u"]):
                ingrd["min_price"]=float(df.iloc[i,5]) * 100
                ingrd["max_price"]=float(df.iloc[i,7]) * 100
                ingrd["u"] = ingrd["u"].replace(u'جنيه',u'قرش')
            else:
                ingrd["min_price"]=float(df.iloc[i,5])
                ingrd["max_price"]=float(df.iloc[i,7])
                
            ingrd["pub"]=datetime.strptime(df.iloc[i,8].replace("\\","").replace(" ",""), '%d/%m/%Y').isoformat()
            ingrd["t"]=df.iloc[i,10]
            ingrd["price"]=(ingrd["min_price"]+ingrd["max_price"])/2.0
            ingrd["price"]=(ingrd["price"]+ingrd["max_price"])/2.0
            data.append(ingrd)
    
    with open(fileName, 'a', encoding="utf-8") as fo:
        json.dump(data, fo, ensure_ascii=False)
        fo.flush()

def main(save=False, max_min_tables=False, save_links=False):
    dfs = []
    alist = [vg, frt, fish, basic, meat, milk, seeds, suger]
    names = ['vegetables', 'fruits', 'fish', 'basic', 'meat', 'milk', 'seeds', 'suger']

    # links for every single item
    dict_of_href = get_href(alist, names)
    if save_links:
        with open('links.pickle', 'wb') as f:
            pickle.dump(f, dict_of_href)
    # for every key in the dict_of_href
    for i in dict_of_href:
        # for link in the value(list) in this key
        print('downloading {}'.format(i))

        for x in dict_of_href[i]:
            # print('X is ', x)
            soup = make_soup(x)
            if soup == None:
                continue
            else:
                parsed = parse_data(soup)
                df = make_df(parsed)
                df['type'] = i
                dfs.append(df)
        print('done {}'.format(i))
        
    print(dfs)
    df = pd.concat(dfs, ignore_index=True)
    df.reset_index(inplace=True)
    print(df[:5])

    saveToFile(df,'prices.json')

if __name__ == '__main__':
    main(save=True)
