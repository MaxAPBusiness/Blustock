"""Este módulo contiene clases relacionadas con crear botones.

Clases
------
    BotonEditar(qtw.QPushButton):
        Genera un botón que se ubicará en las filas de las tablas de la
        UI del programa.
    BotonMostrarContrasena(qtw.QCheckBox):
        Crea un botón checkbox para mostrar o esconder lo ingresado en
        un campo de contraseña.
"""
from PyQt6 import QtWidgets, QtCore, QtGui
import os


class BotonFila(QtWidgets.QPushButton):
    """Esta clase genera un botón que se ubicará en las filas de las
    tablas UI del programa.

    El ícono del botón dependerá del argumento icono.

    Hereda: PyQt6.QtWidgets.QPushButton

    Atributos
    ---------
        icono : str
            El ícono del botón.

    Métodos
    -------
        __init__(self):
            El constructor de la clase BotonEditar.

            Crea el boton y establece su ícono y su tamaño.
    """
    def __init__(self, icono: str, id: int): # Agrego la id de la fila a la que le corresponde (ID en la bbdd, no índice)
        super().__init__()   
        self.id = id
        
        path = f'ui{os.sep}rsc{os.sep}icons{os.sep}{icono}.png'

        # QPixmap: un mapa de pixeles (imagen) de qt. Puede tomar como
        # parámetro el path de la imagen.
        pixmap = QtGui.QPixmap(path)

        # QIcon: un ícono qt para introducir en widgets. Puede tomar
        # como parámetro un pixmap, que representa la imágen que va a 
        # tener el ícono.
        i=QtGui.QIcon(pixmap)

        # Se introduce el ícono en el boton.
        # Método setIcon: establece el ícono de un botón. Toma como
        # parámetro un objeto QIcon.
        self.setIcon(i)
        self.setObjectName(icono)

        # Método setCursor: cambia la forma del cursor cuando pasa por
        # encima del widget.
        self.setCursor(QtGui.QCursor(
            QtCore.Qt.CursorShape.PointingHandCursor))
    
class BotonMostrarContrasena(QtWidgets.QCheckBox):
    """Esta clase crea un botón checkbox para mostrar o esconder lo
    ingresado en un campo de contraseña.
    
    Hereda: PyQt6.QtWidgets.QCheckBox

    Parámetros
    ---------
        entry : QtWidgets.QLineEdit
            El entry de contraseña vinculado al botón.

    Métodos
    -------
        __init__(self):
            El constructor de la clase BotonMostrarContrasena.

            Crea el boton y establece su ícono, su tamaño y su función.

        mostrarContrasena(self):
            Muestra o esconde la contraseña dependiendo del estado de
            activación del botón.
    """
    def __init__(self, entry: QtWidgets.QLineEdit):
        super().__init__()
        # Para entender qué hace el código de abajo, mirar la
        # primera clase (BotonFila)
        path=f'ui{os.sep}rsc{os.sep}icons{os.sep}mostrar.png'
        pixmap = QtGui.QPixmap(path)
        self.setIcon(QtGui.QIcon(QtGui.QIcon(pixmap)))
        self.setIconSize(QtCore.QSize(25, 25))

        # Mirar la documentación de la función.
        self.stateChanged.connect(lambda: self.mostrarContrasena(entry))
        self.mostrarContrasena()
        self.setObjectName("show")
        self.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        
    def mostrarContrasena(self, entry: QtWidgets.QLineEdit):
        """Este método muestra o esconde lo ingresado en el campo de
        contraseña vinculado dependiendo del estado de activación del 
        botón.
        
        Parámetros
        ----------
            entry : QtWidgets.QLineEdit
                El entry de contraseña vinculado al botón.
        """
        # Si el botón está presionado
        if self.isChecked():
            # Muestra lo ingresado en el campo.
            entry.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            # Cambia el ícono.
            path=f'ui{os.sep}rsc{os.sep}icons{os.sep}esconder.png'
            pixmap = QtGui.QPixmap(path)
        else:
            # Cifra lo ingresado en el campo.
            self.entry.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            path=f'ui{os.sep}rsc{os.sep}icons{os.sep}mostrar.png'
            pixmap = QtGui.QPixmap(path)
        self.setIcon(QtGui.QIcon(pixmap))
        self.setIconSize(QtCore.QSize(25, 25))