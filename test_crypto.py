from security.crypto.AesCipher import *
import os

if __name__ == "__main__" :
    cipher = AesCipher()
    encrypted = cipher.encrypt("password")
    print(encrypted)
 
    with open("password_test.txt", "r") as f:
        text = f.read()

    enc = text.split(':')[0].strip()
    print(cipher.decrypt(enc))