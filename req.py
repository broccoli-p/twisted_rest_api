import requests
URL = 'http://127.0.0.1:9990/person'
header = {'Context-Type':'application/json'}
response = requests.post(URL, headers=header) 
print response.status_code 
print response.text
