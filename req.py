import requests
URL = 'http://localhost:9990/person'
header = {'Context-Type':'application/json'}
response = requests.post(URL, headers=header) 
print (response.status_code)
print (response.content)