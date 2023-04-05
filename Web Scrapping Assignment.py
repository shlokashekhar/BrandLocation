#!/usr/bin/env python
# coding: utf-8

import requests
import json
import csv
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns

import warnings
warnings.filterwarnings("ignore")


url = "https://api.pantaloons.com/store/getCurrentStore"


payload = json.dumps({
  "brand": "pantaloons",
  "validateHash": False,
  "hash": "b991e1b3d3352b7d89ce3df3cccec3e9",
  "utmSource": -1,
  "version": 3.4,
  "geoLocation": {
    "latitude": 0
  },
  "deviceType": "desktop",
  "fcmToken": "111",
  "deviceId": "bdec426-1a64-dfaa-de61-ad64daa2aa0c",
  "deviceToken": "d2a2bb1bd314801ec4aed24f978727e6.1680524955",
  "sessionId": "d2a2bb1bd314801ec4aed24f978727e6",
  "searchWord": " ",
  "cartId": 0,
  "customerId": 0,
  "sliderSource": -1,
  "cartOperation": "add"
})
headers = {
  'authority': 'api.pantaloons.com',
  'accept': 'application/json',
  'accept-language': 'en-US,en;q=0.9',
  'content-type': 'application/json',
  'env': 'prod',
  'origin': 'https://www.pantaloons.com',
  'referer': 'https://www.pantaloons.com/',
  'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-site',
  'securekey': '12345',
  'source': 'desktop',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}


data = requests.post(url, headers=headers, data=payload)

print(data.text.encode('utf8'))

data.status_code

stores = json.loads(data.text)

stores['results']

stores.keys()

del stores['success']
del stores['msg']
del stores['cache']
del stores['hash']
del stores['ttl']

with open('Pantaloon_Locations.csv', 'w', encoding = 'utf-8') as pt:
    
    writer = csv.writer(pt, delimiter = ",", quotechar = '"', quoting = csv.QUOTE_MINIMAL)
    
    writer.writerow([
        "Retek_code",
        "store_name",
        "city",
        "pincode",
        "address",
        "latitude",
        "longitude",
        "contact",
        "whatsapp",
        "manager_contact",
        "opening",
        "closing"
        
    ])
    
    for store in stores['results']:
        row = []
        retek_code = store['retek_code']
        store_name = store['store_name']
        city = store['city']
        pincode = store['pincode']
        address = store['address']
        latitude = store['latitude']
        longitude = store['longitude']
        contact = store['phone_number']
        whatsapp = store['whatsapp_number']
        manager_contact = store['store_manager_contact']
        opening = store['open_timings']
        closing = store['closing_time']

        
        row.append(retek_code)
        row.append(store_name)
        row.append(city)
        row.append(pincode)
        row.append(address)
        row.append(latitude)
        row.append(longitude)
        row.append(contact)
        row.append(whatsapp)
        row.append(manager_contact)
        row.append(opening)
        row.append(closing)
        
        writer.writerow(row)

pantaloon = pd.read_csv('Pantaloon_Locations.csv')

pantaloon.head()

print(pantaloon.shape)
print(pantaloon.dtypes)

pantaloon.isna().sum()

pantaloon.city.value_counts().head(10)

plt.figure(figsize = (12,5), dpi = 120)
city_count = pantaloon['city'].value_counts(normalize=True).head(10)
sns.barplot(city_count.index, city_count, order = city_count.index)
plt.xlabel('City')
plt.ylabel('Fraction/Percent')
