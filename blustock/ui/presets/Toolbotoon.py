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
from ui.presets.turnos import NuevoTurno,TerminarTurno
from db.bdd import bdd
from ui.presets.popup import PopUp

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
        self.popup = None

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
        c.triggered.connect(self.cerrar)
        d.triggered.connect(self.nuevo)
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
                font-size: 18px;
                text-align: center;
            }
            Qtoolbutton{
                background-color: #293045;

            }
            QMenu {
                background-color: #293045;
                color:white;
                padding-left:5px;
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
        self.close()
    
    def nuevo(self):
            self.popup = NuevoTurno(self.nw.usuario).exec()
            print(self.popup)
            if self.popup == 12:
                usuario = bdd.cur.execute("select nombre_apellido from turnos join personal p on p.id = id_panolero WHERE fecha_egr is null").fetchone()
                if usuario != None: 
                    if self.nw.label == QtWidgets.QLabel():
                        self.nw.label = QtWidgets.QLabel(str("El pañolero en turno es: " + usuario[0]))
                        self.nw.label.setObjectName("sopas")
                        self.nw.menubar.setCornerWidget(self.nw.label,QtCore.Qt.Corner.TopRightCorner)
                    else:
                        self.nw.label.setText("El pañolero en turno es: " + usuario[0])

                    for i in range(7):
                        if i != 3:
                            self.nw.menubar.actions()[i].setVisible(False)
                self.menu().actions()[0].setVisible(False)

    def cerrar(self):
            self.popup=TerminarTurno(self.nw.usuario).exec()
            if self.popup == 8:
                self.nw.label.setText("Usuario: " + bdd.cur.execute("SELECT nombre_apellido FROM personal WHERE dni = ?",(self.nw.usuario,)).fetchone()[0])
                for i in range(7):
                    if i != 3:
                        self.nw.menubar.actions()[i].setVisible(True)
                self.menu().actions()[0].setVisible(True)
