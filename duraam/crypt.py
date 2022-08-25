from cryptography.fernet import Fernet
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
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

def showPassword(entries, showButtons, checked):
        if checked:
            for i in range(len(entries)):
                entries[i].setEchoMode(qtw.QLineEdit.EchoMode.Normal)
                showButtons[i].setIcon(qtg.QIcon(qtg.QPixmap(f"{os.path.abspath(os.getcwd())}/duraam/images/hide.png")))
                showButtons[i].setIconSize(qtc.QSize(25, 25))
        else:
            for i in range(len(entries)):
                entries[i].setEchoMode(qtw.QLineEdit.EchoMode.Password)
                showButtons[i].setIcon(qtg.QIcon(qtg.QPixmap(f"{os.path.abspath(os.getcwd())}/duraam/images/mostrar.png")))
                showButtons[i].setIconSize(qtc.QSize(25, 25))
