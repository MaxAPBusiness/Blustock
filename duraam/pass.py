from cryptography.fernet import Fernet

def encriptar(password, key = "PensaEnElColeAntesDeRobar"):
    fernet = Fernet(key)
    return fernet.encrypt(password.encode())

def decriptar(password, key = "PensaEnElColeAntesDeRobar"):
    fernet = Fernet(key)
    return fernet.decrypt(password).decode()

 
