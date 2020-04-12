import json

def convertJsonToDict(data):
    return json.loads(data)

def convertDictToJson(data):
    return json.dumps(data)