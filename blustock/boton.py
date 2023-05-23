from PyQt6 import QtWidgets, QtCore, QtGui, uic
import pathlib
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
        c = str(pathlib.Path(__file__).parent.absolute())
        path = c +'/rsc/' +str(icono)
        a = QtGui.QPixmap(path)
        q.addPixmap(a)
        self.setIcon(q)
        self.setObjectName(icono.split(".")[0])
        self.setCursor(QtGui.QCursor(
            QtCore.Qt.CursorShape.PointingHandCursor))
    
