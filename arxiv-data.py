# -*- coding: utf-8 -*-
"""
Created on Sat May  2 08:00:52 2020

@author: IF
"""

import urllib.request as libreq
import xml.etree.ElementTree as ET
import pandas as pd

# =============================================================================
# arxiv_api = 'http://export.arxiv.org/api/query?search_query=abs:%22climate+change%22+OR+it:%22climate+change%22&max_results=2'
# url = libreq.urlopen(arxiv_api)
# r = url.read()
# #print(r)
# root = ET.fromstring(r)
# url.close()
# 
# =============================================================================

api = 'http://export.arxiv.org/api/query?search_query=abs:%22climate+change%22+OR+it:%22climate+change%22'
def get_arxiv_api(url, start):
    arxiv_api = f'{url}&start={start}&max_results=10'
    return arxiv_api

def get_total_result(arxiv_api):
    url = libreq.urlopen(arxiv_api)
    r = url.read()
    root = ET.fromstring(r)
    for i in root.iter():
        if 'totalResults' in i.tag:
            return int(i.text)
    return 0



arxiv_data = []
total_result = get_total_result(api)
for i in range(total_result//10 + 1):
    arxiv_api = get_arxiv_api(api,i*10)
    #print(arxiv_api)
    url = libreq.urlopen(arxiv_api)
    r = url.read()
    #print(r)
    root = ET.fromstring(r)
    url.close()
    for i in root.iter():
        #print(i.tag)
        if 'summary' in i.tag:
            arxiv_data.append(i.text)
            #print(i.text)

arxiv_data = pd.DataFrame(arxiv_data)
arxiv_data.to_json('arxiv_data.json')

