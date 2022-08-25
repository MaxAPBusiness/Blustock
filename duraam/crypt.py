from cryptography.fernet import Fernet
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import os

def encriptar(password, key = "xQInlLoNPQK05ytstTGSrc-HmquOy3QM6hg7CRSBAtc="):
    bkey=key.encode('ascii')
    fernet = Fernet(bkey)
    return fernet.encrypt(password.encode())

def decriptar(password, key = "xQInlLoNPQK05ytstTGSrc-HmquOy3QM6hg7CRSBAtc="):
    bkey=key.encode('ascii')
    print(bkey)
    fernet = Fernet(bkey)
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
