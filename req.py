from __future__ import absolute_import, division, print_function
import requests
from common.simpleJson import convertDictToJson
params = {'personId':'admin1'}
#URL = 'https://192.168.2.230:9990/person'
URL = 'https://localhost:9990/sync/person'
header = {'Context-Type':'application/json'}
print (convertDictToJson(params))
response = requests.put(URL, headers=header, params=convertDictToJson(params), verify=False)
#response = requests.post(URL, headers=header, params=params) 
print (response.status_code)
print (response.content)