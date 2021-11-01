# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 10:47:32 2021

@author: XPS
"""

import requests
import json
import time

url = 'https://world-geo-data.p.rapidapi.com/countries/BE/adm-divisions'

headers = {
    'x-rapidapi-host': "world-geo-data.p.rapidapi.com",
    'x-rapidapi-key': "4df3692d45msh4addc1a7e6190f0p1f3544jsn142deaadd4a9"
    }

response = requests.get(url, headers=headers)
response = json.loads(response.content)

for region in response['divisions']:
    if 'Brussels' in region['name']:
        brussels_region_id = region['geonameid']
        
time.sleep(2)

url = 'https://world-geo-data.p.rapidapi.com/adm-divisions/'+str(brussels_region_id)+'/cities'
response = requests.get(url, headers=headers)
response = json.loads(response.content)

for city in response['cities']:
    print(f"{city['name']} - {city['population']} inhabitants")

