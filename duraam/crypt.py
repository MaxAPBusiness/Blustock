"""Este módulo crea las funciones relacionadas con la encriptación de
contraseñas.

Funciones
---------
    writeKey(): crea una key y la guarda en un archivo en la carpeta db
    loadKey(): obtiene la key guardada en el archivo de la carpeta db
               y devuelve el texto del archivo (la key como un string).
    encriptar(password): encripta una contraseña.
    decriptar(password): decripta una contraseña.
"""
# Clase Fernet: encripta contraseñas. Viene del módulo
# cryptography.fernet
from cryptography.fernet import Fernet
import os


def writeKey():
    """Esta función crea una key y la guarda en un archivo en la
    carpeta db
    """
    # Método generate_key: crea una key aleatoria.
    # El método pertenece a la clase Fernet.
    key = Fernet.generate_key()
    with open(f"{os.path.abspath(os.getcwd())}/duraam/db/key.key", "wb") as keyFile:
        keyFile.write(key)


def loadKey():
    """Esta función obtiene la key guardada en el archivo de la carpeta
    db y devuelve el texto del archivo (la key como un string).
    """
    with open(f"{os.path.abspath(os.getcwd())}/duraam/db/key.key", "rb") as archivo:
        return archivo.read()


def encriptar(password: str):
    """Esta función encripta una contraseña.

    Parámetros
    ----------
        password : str
            La contraseña a encriptar.

    Devuelve
    --------
        encryptedPassword : bytes
            La contraseña encriptada.
    """
    key = loadKey()
    # Obtenemos un objeto Fernet de la key. Esto lo hacemos para
    # encriptarla, porque Fernet solo puede encriptar objetos, no texto
    fernet = Fernet(key)
    # Obtiene la contraseña encriptada (en bytes) de la contraseña.
    # El encode() lo que hace es transformar el texto de la contraseña
    # en bytes para que fernet lo pueda encriptar.
    encryptedPassword = fernet.encrypt(password.encode())
    return encryptedPassword


def decriptar(password: bytes | str):
    """Esta función decripta una contraseña.

    Parámetros
    ----------
        password : bytes | str
            La contraseña encriptada a decriptar.

    Devuelve
    --------
        decryptedPassword : str
            La contraseña decriptada.
    """
    key = loadKey()
    fernet = Fernet(key)
    # Método decrypt: obtiene la contraseña decriptada.
    # el decode al final transforma los bytes en texto.
    decryptedPassword = fernet.decrypt(password).decode()
    return decryptedPassword

