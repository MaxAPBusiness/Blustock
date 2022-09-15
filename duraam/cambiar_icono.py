import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import os

def cambiarIcono(boton, checked):
    if checked:
        boton.setIcon(
            qtg.QIcon(
                qtg.QPixmap(f"{os.path.abspath(os.getcwd())}/duraam/images/ascendente.png")
                )
            )
        boton.setIconSize(qtc.QSize(25, 25))
    else:
        boton.setIcon(
            qtg.QIcon(
                qtg.QPixmap(f"{os.path.abspath(os.getcwd())}/duraam/images/descendente.png")
                )
            )
        boton.setIconSize(qtc.QSize(25, 25))