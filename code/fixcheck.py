import msgpack_lz4block
import json
import requests
import os

# get spine, background, bgm, card data from episode detail


templist = json.load(open('../_temp/Temp.json', 'rb'))
backgroundlist = templist['background']
bgmlist = templist['bgm']
selist = templist['se']
cardlist = templist['card']
spinelist = templist['spine']

print(templist)
