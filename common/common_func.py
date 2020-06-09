
import os, inspect
import json, codecs

def convertJsonToDict(data):
    return json.loads(data)

def convertDictToJson(data):
    return json.dumps(data)
    
def getModuleNm(frame):
    return os.path.split(os.path.abspath(inspect.getfile(frame)))[1]

def getErrorStr(frame, err, lineno = None):
    errortype = 'Exception' if isinstance(err, str) else err.__class__.__name__
    lineno = lineno if lineno is not None else frame.f_lineno
    return '[%s][lineno:%s][%s] >\n%s' %(getModuleNm(frame), lineno, errortype, err)

def ipChk(ip):
    ipList = ip.split('.')
    if len(ipList) != 4:
        return False
    for i in ipList:
        try:
            if int(i) > 255 or int(i) < 0:
                return False
        except:
            return False
    return True

def portChk(port):
    try:
        if int(port) > 65536 or int(port) < 1:
            return False
    except :
        return False
    return True

def convertUnicodeToStr(data, dept=0):
    try:
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, str):
                    data[k] = v.decode('utf-8')
                if isinstance(v, dict) or isinstance(v, list) or isinstance(v, tuple):
                    data[k] = convertUnicodeToStr(v, dept+1)
        elif isinstance(data, list) or isinstance(data, tuple):
            if isinstance(data, tuple):data = list(data)
            for i in range(len(data)):
                if isinstance(data[i], str):
                    try:
                        data[i] = data[i].decode('utf-8')
                    except UnicodeDecodeError:
                        data[i] = data[i].decode('cp949')
                elif isinstance(data[i], dict) or isinstance(data[i], list) or isinstance(data[i], tuple):
                    data[i] = convertUnicodeToStr(data[i], dept+1)
        return data
    except Exception as err:
        lineno = sys.exc_info()[2].tb_lineno
        raise Exception(getErrorStr(sys._getframe(), err, lineno))

def dictCodecsUnicode(data):
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, dict) or isinstance(v, list):
                data[k] = dictCodecsUnicode(v)
            elif isinstance(v, int) or isinstance(v, float):
                pass
            else:
                data[k] = codecs.decode(v, 'unicode_escape')
    elif isinstance(data, list):
        for i in range(len(data)):
            if isinstance(data[i], dict) or isinstance(data[i], list):
                data[i] = dictCodecsUnicode(data[i])
            elif isinstance(data[i], int) or isinstance(data[i], float):
                pass
            else:
                data[i] = codecs.decode(data[i], 'unicode_escape')
    return data

def dictPrint(data):
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, dict) or isinstance(v, list):
                dictPrint(v)
            else:
                print(k,':',v)
    elif isinstance(data, list):
        for i in data:
            if isinstance(i, dict) or isinstance(i, list) or isinstance(i, tuple):
                dictPrint(i)
            else:
                print(i)

