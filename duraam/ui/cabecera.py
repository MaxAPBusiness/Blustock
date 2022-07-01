# Importamos las librerías
import PyQt6.QtWidgets as qtw
import os
import PyQt6.QtGui as qtg

class Cabecera(qtw.QToolBar):
    def __init__(self):
        super().__init__()

        self.setFloatable(False)
        self.setMovable(False)

        # Se crea un pixmap (algo que guarda una imagen para ponerla en la pantalla), se le da el ícono y se crea el label que tendra la imagen.
        pixmap = qtg.QPixmap(
            f"{os.path.abspath(os.getcwd())}/duraam/images/bitmap.png")
        icono = qtw.QLabel("")
        icono.setPixmap(pixmap)
        # Esto le da un id a los elementos para poder personalizarlos luego con el archivo .qss.
        icono.setObjectName("icono")

        self.headerLabel = qtw.QLabel("DURAAM")
        self.headerLabel.setObjectName("header-label")

        self.addWidget(icono)
        self.addWidget(self.headerLabel)
        
        with open(f"{os.path.abspath(os.getcwd())}/duraam/styles/cabecera.qss", "r") as qss:
            self.setStyleSheet(qss.read())
