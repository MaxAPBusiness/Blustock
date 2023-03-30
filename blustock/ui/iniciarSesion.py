"""Este módulo crea una pantalla para iniciar sesión en la aplicación.

Clases
------
    IniciarSesion(qtw.QWidget):
        Crea una pantalla para iniciar sesión en la aplicación.
"""
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
from textwrap import dedent

from .botones import BotonMostrarContrasena


class IniciarSesion(qtw.QWidget):
    """Esta clase crea una pantalla para iniciar sesión en la
    aplicación.

    Hereda: PyQt6.QtWidgets.QWidget

    Atributos
    ---------
        entry1 : QLineEdit
            El campo de usuario.
        entry2 : QLineEdit
            El campo de contraseña.
        confirmar : QPushButton
            El boton para confirmar los datos.
        registrarse : QPushButton
            El boton para ir a la pantalla de registro de usuario.

    Métodos
    -------
        __init__(self):
            El constructor de la clase IniciarSesion.

            Crea la pantalla, un QWidget, que contiene un título
            descriptivo, un QLabel, dos campos, QLineEdit, para
            ingresar usuario y contraseña respectivamente, acompañados
            de labels descriptivos, QLabel, un boton para mostrar la
            contraseña, QCheckBox, un boton para iniciar sesion,
            QPushButton, y otro para ir a la pantalla de registro,
            también QPushButton.
    """

    def __init__(self):
        super().__init__()

        titulo = qtw.QLabel(
            dedent("""Bienvenido al sistema de gestión de bases de datos del pañol!
                                                  Inicia sesión
            """)
        )
        titulo.setObjectName("titulo")

        label1 = qtw.QLabel("Usuario: ")
        label2 = qtw.QLabel("Contraseña: ")

        label1.setObjectName("ingresar-label")
        label2.setObjectName("ingresar-label")

        self.entry1 = qtw.QLineEdit()
        self.entry2 = qtw.QLineEdit()
        self.entry2.setEchoMode(qtw.QLineEdit.EchoMode.Password)
        self.entry1.setObjectName("modificar-entry")
        self.entry2.setObjectName("modificar-entry")
        self.entry1.setMaxLength(20)
        self.entry2.setMaxLength(20)

        # Cuando el usuario termine de escribir su usuario y presione
        # enter, automáticamente selecciona el campo de la contraseña.
        # Método setFocus: selecciona un widget.
        self.entry1.returnPressed.connect(lambda: self.entry2.setFocus())

        
        # Creamos el botón mostrarContrasena y lo vinculamos con el
        # entry 2. Para más información, lean la documentación de la
        # clase BotonMostrarContrasena() del módulo botones.py
        mostrarContrasena = BotonMostrarContrasena(self.entry2)

        self.confirmar = qtw.QPushButton("confirmar")
        self.confirmar.setObjectName("confirmar-grande")
        self.confirmar.setCursor(qtg.QCursor(
            qtc.Qt.CursorShape.PointingHandCursor))

        self.registrarse = qtw.QPushButton("¿No tienes una cuenta? Regístrate")
        self.registrarse.setObjectName("boton-texto")
        self.registrarse.setCursor(qtg.QCursor(
            qtc.Qt.CursorShape.PointingHandCursor))

        layout = qtw.QGridLayout()
        layout.addWidget(titulo, 0, 0, 1, 3,
                         alignment=qtc.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(
            label1, 1, 0, alignment=qtc.Qt.AlignmentFlag.AlignRight)
        layout.addWidget(
            label2, 2, 0, alignment=qtc.Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.entry1, 1, 1)
        layout.addWidget(self.entry2, 2, 1)
        layout.addWidget(mostrarContrasena, 2, 2)
        layout.addWidget(self.confirmar, 3, 0, 1, 3,
                         alignment=qtc.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.registrarse, 4, 0, 1, 3,
                         alignment=qtc.Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
