import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import os

def showPassword(entry, showButton, checked):
    if checked:
        entry.setEchoMode(qtw.QLineEdit.EchoMode.Normal)
        showButton.setIcon(qtg.QIcon(qtg.QPixmap(f"{os.path.abspath(os.getcwd())}/duraam/images/hide.png")))
        showButton.setIconSize(qtc.QSize(25, 25))
    else:
        entry.setEchoMode(qtw.QLineEdit.EchoMode.Password)
        showButton.setIcon(qtg.QIcon(qtg.QPixmap(f"{os.path.abspath(os.getcwd())}/duraam/images/mostrar.png")))
        showButton.setIconSize(qtc.QSize(25, 25))