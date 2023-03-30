"""Este módulo crea la cabecera de la ventana.

Clases:
    Cabecera(qtw.QToolBar): crea la cabecera de la ventana.
"""
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import os


class Cabecera(qtw.QToolBar):
    """Esta clase crea la cabecera de la ventana.

    Contiene el logo, el título y el boton de usuario.

    Hereda: qtw.QToolBar

    Métodos
    -------
        __init__(self):
            El constructor de la clase Cabecera.

            Crea la cabecera de la ventana con el logo, el título y el
            boton de usuario. Por defecto, el boton de usuario no se
            inserta.
    """

    def __init__(self):
        super().__init__()

        # Método setFloatable: regula si la barra se puede mover de
        # lugar por el usuario o no. Nosotros lo dejamos que no (false)
        self.setFloatable(False)

        # Método setMovable: regula si la barra se puede mover de
        # lugar por el usuario o no. Nosotros lo dejamos que no (false)
        # La diferencia con setFloatable es que floatable permite que
        # la barra se mueva libremente por la pantalla, mientras que
        # setMovable solo permite moverla de borde. Nosotros ponemos
        # las dos en false.
        self.setMovable(False)
        self.setContextMenuPolicy(qtc.Qt.ContextMenuPolicy.PreventContextMenu)

        pixmap = qtg.QPixmap(
            f"{os.path.abspath(os.getcwd())}/duraam/images/logo.png")
        icono = qtw.QLabel("")
        icono.setPixmap(pixmap)
        icono.setObjectName("icono")

        headerLabel = qtw.QLabel("DURAAM")
        headerLabel.setObjectName("header-label")

        spacer = qtw.QWidget()
        spacer.setSizePolicy(qtw.QSizePolicy.Policy.Expanding,
                             qtw.QSizePolicy.Policy.Expanding)

        self.usuario = qtw.QPushButton()
        self.usuario.setIcon(qtg.QIcon(qtg.QPixmap(
            f"{os.path.abspath(os.getcwd())}/duraam/images/usuario.png")))
        self.usuario.setIconSize(qtc.QSize(100, 100))
        self.usuario.setObjectName("usuario")
        self.usuario.setCursor(qtg.QCursor(
            qtc.Qt.CursorShape.PointingHandCursor))

        contenedor = qtw.QWidget()
        self.contenedorLayout = qtw.QHBoxLayout()
        self.contenedorLayout.addWidget(icono)
        self.contenedorLayout.addWidget(headerLabel)
        self.contenedorLayout.addWidget(spacer)
        contenedor.setLayout(self.contenedorLayout)
        contenedor.setMinimumHeight(100)
        self.addWidget(contenedor)

        with open(f"{os.path.abspath(os.getcwd())}/duraam/styles/cabecera.qss", "r") as qss:
            self.setStyleSheet(qss.read())
