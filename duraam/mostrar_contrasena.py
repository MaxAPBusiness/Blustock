import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import os

def mostrarContrasena(entry, boton, checked):
    if checked:
        entry.setEchoMode(qtw.QLineEdit.EchoMode.Normal)
        boton.setIcon(
            qtg.QIcon(
                qtg.QPixmap(f"{os.path.abspath(os.getcwd())}/duraam/images/hide.png")
                )
            )
    else:
        entry.setEchoMode(qtw.QLineEdit.EchoMode.Password)
        boton.setIcon(
            qtg.QIcon(
                qtg.QPixmap(f"{os.path.abspath(os.getcwd())}/duraam/images/mostrar.png")
                )
            )
    boton.setIconSize(qtc.QSize(25, 25))