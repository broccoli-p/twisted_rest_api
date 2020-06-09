#-*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function
import requests, codecs
from common.common_func import convertDictToJson, convertJsonToDict

def dictCodecsUnicode(data):
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, dict) or isinstance(v, list):
                data[k] = codecsUnicode(v)
            elif isinstance(v, int) or isinstance(v, float):
                pass
            else:
                data[k] = codecs.decode(v, 'unicode_escape')
    elif isinstance(data, list):
        for i in data:
            if isinstance(v, dict) or isinstance(v, list):
                data[k] = codecsUnicode(v)
            elif isinstance(v, int) or isinstance(v, float):
                pass
            else:
                data[k] = codecs.decode(v, 'unicode_escape')
    return data
    return data
# block InsecureRequestWarning Waring
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
a = '최고관리자'
params = {'personname':a}

URL = 'https://192.168.2.230:9990/api/sync/person'
header = {'Context-Type':'application/json'}
response = requests.get(URL, headers=header, params=convertDictToJson(params), verify=False)

a = dictCodecsUnicode(response.content)
print (a)
def dictPrint(data):
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, dict) or isinstance(v, list):
                dictPrint(v)
            else:
                print(k,':',v)
    elif isinstance(data, list):
        for i in data:
            if isinstance(v, dict) or isinstance(v, list):
                dictPrint(v)
            else:
                print(i)
dictPrint(a)