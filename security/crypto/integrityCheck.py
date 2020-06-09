import hashlib

def encHash(data):
    shaEnc = hashlib.sha256(data.encode()).hexdigest()
    shaDataDict = "{0}:{1}".format(data, shaEnc)

    with open("password_test.txt", "w") as f:
        f.write(shaDataDict)

def integrity(data):
    shaEnc = hashlib.sha256(data.encode()).hexdigest()
    with open("password_test.txt", "r") as f:
        data = f.read()
    preShaEnc = data.split(':')[1].strip()
    if preShaEnc == shaEnc:
        return 0
    else:
        return -1