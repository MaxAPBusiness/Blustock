"""Este módulo contiene clases relacionadas con crear botones.

Clases
------
    BotonEditar(qtw.QPushButton):
        Crea un botón diseñado para editar.
    BotonEliminar(qtw.QPushButton):
        Crea un botón diseñado para eliminar.
    BotonMostrarContrasena(qtw.QCheckBox):
        Crea un botón para mostrar o esconder una contraseña.
    BotonOrdenar(qtw.QCheckBox):
        Crea un botón para ordenar los datos de la tabla de una
        pantalla de manera ascendente o descendente.
"""
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import os


class BotonEditar(qtw.QPushButton):
    """Esta clase crea un botón diseñado para editar.
    
    Hereda: PyQt6.QtWidgets.QPushButton

    Métodos
    -------
        __init__(self):
            El constructor de la clase BotonEditar.

            Crea el boton y establece su ícono y su tamaño.
    """
    def __init__(self):
        super().__init__()

        # Se introduce el ícono en el boton.
        # Método setIcon: establece el ícono de un botón. Toma como
        # parámetro un objeto QIcon.
        # QIcon: un ícono qt para introducir en widgets. Puede tomar
        # como parámetro un pixmap, que representa la imágen que va a 
        # tener el ícono.
        self.setIcon(qtg.QIcon(
            qtg.QPixmap(f"{os.path.abspath(os.getcwd())}/duraam/images/editar.png")))
        
        # Se cambia el tamaño del ícono. 
        # Método setIconSize: establece el tamaño del ícono de un
        # widget. Toma como parámetro un objeto QSize.
        # QSize: representa un tamaño. No se porque tienen un
        # objeto para un tamaño pero bueno. 
        # Parámetros: 
        #     w (int): el ancho.
        #     h (int): el alto.
        self.setIconSize(qtc.QSize(25, 25))
        self.setObjectName("editar")
        self.setCursor(qtg.QCursor(
            qtc.Qt.CursorShape.PointingHandCursor))


class BotonEliminar(qtw.QPushButton):
    """Esta clase crea un botón diseñado para eliminar.
    
    Hereda: PyQt6.QtWidgets.QPushButton

    Métodos
    -------
        __init__(self):
            El constructor de la clase BotonEliminar.

            Crea el boton y establece su ícono y su tamaño.
    """
    def __init__(self):
        super().__init__()

        self.setIcon(qtg.QIcon(
            qtg.QPixmap(f"{os.path.abspath(os.getcwd())}/duraam/images/eliminar.png")))
        self.setIconSize(qtc.QSize(25, 25))
        self.setObjectName("eliminar")
        self.setCursor(qtg.QCursor(
            qtc.Qt.CursorShape.PointingHandCursor))


class BotonMostrarContrasena(qtw.QCheckBox):
    """Esta clase crea un botón para mostrar o esconder una contraseña.
    
    Hereda: PyQt6.QtWidgets.QCheckBox

    Atributos
    ---------
        entry : qtw.QLineEdit
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
    def __init__(self, entry: qtw.QLineEdit):
        super().__init__()

        self.entry = entry
        self.setIcon(
            qtg.QIcon(
                qtg.QPixmap(
                    f"{os.path.abspath(os.getcwd())}/duraam/images/mostrar.png")
            )
        )
        self.setIconSize(qtc.QSize(25, 25))
        self.stateChanged.connect(lambda: self.mostrarContrasena())
        self.setObjectName("show")
        self.setCursor(
            qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor))

    def mostrarContrasena(self):
        """Este método muestra o esconde la contraseña dependiendo del
        estado de activación del botón."""
        if self.isChecked():
            self.entry.setEchoMode(qtw.QLineEdit.EchoMode.Normal)
            pixmap = qtg.QPixmap(
                f"{os.path.abspath(os.getcwd())}/duraam/images/hide.png")
        else:
            self.entry.setEchoMode(qtw.QLineEdit.EchoMode.Password)
            pixmap = qtg.QPixmap(
                f"{os.path.abspath(os.getcwd())}/duraam/images/mostrar.png")
        self.setIcon(qtg.QIcon(pixmap))
        self.setIconSize(qtc.QSize(25, 25))


class BotonOrdenar(qtw.QCheckBox):
    """Esta clase crea un botón para ordenar los datos de la tabla de
    una pantalla de manera ascendente o descendente.
    
    Hereda: PyQt6.QtWidgets.QCheckBox

    Métodos
    -------
        __init__(self):
            El constructor de la clase BotonOrdenar.

            Crea el boton y establece su ícono y su tamaño.

        cambiarIcono(self):
            Cambia el ícono del botón.
    """
    def __init__(self):
        super().__init__()

        self.setIcon(
            qtg.QIcon(
                qtg.QPixmap(
                    f"{os.path.abspath(os.getcwd())}/duraam/images/descendente.png")
            )
        )
        self.setIconSize(qtc.QSize(25, 25))
        self.setObjectName("show")
        self.setCursor(
            qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor)
        )

    def cambiarIcono(self):
        """Este método cambia el ícono del botón.

        El icono dependerá del estado de activación del botón."""
        if self.isChecked():
            pixmap = qtg.QPixmap(
                f"{os.path.abspath(os.getcwd())}/duraam/images/ascendente.png")
        else:
            pixmap = qtg.QPixmap(
                f"{os.path.abspath(os.getcwd())}/duraam/images/descendente.png")
        self.setIcon(qtg.QIcon(pixmap))
        self.setIconSize(qtc.QSize(25, 25))
