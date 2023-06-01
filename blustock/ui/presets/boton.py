from PyQt6 import QtWidgets, QtCore, QtGui, uic
import pathlib
import os
class BotonFila(QtWidgets.QPushButton):

    def __init__(self, icono: str):
        super().__init__()

        # Se introduce el ícono en el boton.
        # Método setIcon: establece el ícono de un botón. Toma como
        # parámetro un objeto QIcon.
        # QIcon: un ícono qt para introducir en widgets. Puede tomar
        # como parámetro un pixmap, que representa la imágen que va a 
        # tener el ícono.
        # Nota: el atributo ícono de la clase es el nombre del icono
        # que se busca en la carpeta images.
        q=QtGui.QIcon()
        path = f'ui{os.sep}rsc{os.sep}{icono}'
        a = QtGui.QPixmap(path)
        q.addPixmap(a)
        self.setIcon(q)
        self.setObjectName(icono.split(".")[0])
        self.setCursor(QtGui.QCursor(
            QtCore.Qt.CursorShape.PointingHandCursor))
    
