#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup as bf
import pickle

headers = {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0"}

base_url = "https://www.fakepersongenerator.com"
url = "https://www.fakepersongenerator.com/Index/generate/gender/male/age/25/state/CO/city/colorado+springs"

# selections = {}
# with open("selections.pkl","rb") as file:
#     selections = pickle.load(file)

# state_abbr = {}
# with open("state_abbr.pkl","rb") as file:
#     state_abbr = pickle.load(file)

try:
    req = requests.get(url=base_url, headers=headers).text
except:
    print("Unable to connect !!")
    exit()

frame  = bf(req, "html5lib").find("div",class_="frame-1")

db = "######## Fake person ########\n\n"
name = frame.find("div",class_="col-md-4 col-sm-6 col-xs-12").text.replace("\xa0"," ")
db += f'Name: {name}\n'
for item in frame.find("div",class_="col-md-8 col-sm-6 col-xs-12").find_all("p"):
    db += f"{item.text.strip()}\n"

base_filename = name.replace(" ","_")
img_url = base_url + frame.find("div",class_="col-md-4 col-sm-6 col-xs-12").find("img")["src"]
with open(f"{base_filename}.jpg","wb") as file:
    file.write(requests.get(url=img_url, headers=headers).content)

headings = []
for h3 in frame.find_all("h3"):
    headings.append(h3.text.strip())
long_infos = frame.find_all("div",class_="row no-margin")
for block in long_infos:
    if block.find("div", class_="info-title"):
        db += f"\n########  {headings.pop(0)} ########\n"
        left = block.find_all("div", class_="info-title")
        right = block.find_all("div", class_="info-detail")
        for l,r in zip(left,right):
            try:
                db += f"\n{l.text}: {r.find('input')['value']}"
            except TypeError:
                try:
                    temp = "\n".join([i.text for i in r.find("p").contents if i.text])
                    db += f"\n{l.text}: {temp}"
                except:
                    continue
        db += "\n"

with open(f"{base_filename}.txt","w") as file:
    file.write(db)

print("Generated Successfully")
