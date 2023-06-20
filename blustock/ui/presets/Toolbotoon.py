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
from ui.presets.turnos import nuu,sii
from dal.dal import dal
from db.bdd import bdd

class toolboton(QtWidgets.QToolButton):
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
    def __init__(self, icono: str,nw):
        super().__init__()
        path = f'ui{os.sep}rsc{os.sep}icons{os.sep}{icono}.png'
        self.nw=nw
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
        self.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)
        a=QtWidgets.QMenu(title="sopas")
        b=QtGui.QAction(QtGui.QIcon(f'ui{os.sep}rsc{os.sep}icons{os.sep}salida.png'),"Cerrar sesion",a)
        c=QtGui.QAction(QtGui.QIcon(f'ui{os.sep}rsc{os.sep}icons{os.sep}cerrar.png'),"Terminar turno",a)
        d=QtGui.QAction(QtGui.QIcon(f'ui{os.sep}rsc{os.sep}icons{os.sep}turno.png'),"Iniciar turno",a)
        b.triggered.connect(self.inicio)
        c.triggered.connect(self.anda)
        d.triggered.connect(self.poronga)
        a.addAction(d)
        a.addSeparator()
        a.addAction(c)
        a.addSeparator()
        a.addAction(b)
        self.setMenu(a)
        
        # Define the style for the popup menu using QSS
        menu_style = """
            *{
                font-family: 'Oswald', sans-serif;
                font-weight: 400;
                font-size: 15px;
            }
            Qtoolbutton{
                background-color: #293045;

            }
            QMenu {
                background-color: #293045;
                color:white;
            }
            QMenu::item:selected {
                background-color: #768AC5;
                color:black;
                border-radius: 5px;
            }
        """

        # Apply the style to the popup menu
        self.menu().setStyleSheet(menu_style)


    def inicio(self):
        self.nw.findChild(QtWidgets.QLineEdit, "usuariosLineEdit").clear()
        self.nw.findChild(QtWidgets.QLineEdit, "passwordLineEdit").clear()
        self.nw.menubar.hide()
        self.nw.stackedWidget.setCurrentIndex(0)
    
    def poronga(self):
            popup = nuu(self.nw.usuario)
            popup.exec()

    def anda(self):
            popup=sii(self.nw.usuario)
            popup.exec()
