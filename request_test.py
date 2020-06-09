#-*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function
import requests
from common.common_func import convertDictToJson

# block InsecureRequestWarning Waring
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

params = {'personid':'admin1'}
#params = {'hostname':'host'}
print(type('최고관리자'))
URL = 'https://192.168.2.230:9990/api/sync/person'
#URL = 'https://192.168.2.230:9990/api/sync/host'
header = {'Context-Type':'application/json'}
print (convertDictToJson(params))
response = requests.get(URL, headers=header, params=convertDictToJson(params), verify=False)
print (type(response))
print (response.content)
print ("status_code : ", response.status_code)
