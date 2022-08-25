from cryptography.fernet import Fernet
import os

def writeKey():
    key = Fernet.generate_key()
    with open(f"{os.path.abspath(os.getcwd())}/duraam/db/key.key", "wb") as keyFile:
        keyFile.write(key)

def loadKey():
    with open(f"{os.path.abspath(os.getcwd())}/duraam/db/key.key", "rb") as file:
        return file.read()

def encriptar(password):
    key=loadKey()
    fernet = Fernet(key)
    return fernet.encrypt(password.encode())

def decriptar(password):
    key=loadKey()
    fernet = Fernet(key)
    return fernet.decrypt(password).decode()
