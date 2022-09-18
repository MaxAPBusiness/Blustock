"""Este módulo crea una pantalla para registrarse en la aplicación.

Clases
------
    Registrarse(qtw.QWidget):
        Esta clase crea una pantalla para registrarse en la aplicación.
"""
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg

from botones import BotonMostrarContrasena


class Registrarse(qtw.QWidget):
    """Esta clase crea una pantalla para registrarse en la aplicación.

    Hereda: PyQt6.QtWidgets.QWidget

    Atributos
    ---------
        entry1 : QLineEdit
            El campo de nombre y apellido.
        entry2 : QLineEdit
            El campo de usuario.
        entry2 : QLineEdit
            El campo de contraseña.
        entry2 : QLineEdit
            El campo de confirmar contraseña.
        confirmar : QPushButton
            El boton para confirmar los datos.
        registrarse : QPushButton
            El boton para ir a la pantalla de registro de usuario.

    Métodos
    -------
        __init__(self):
            El constructor de la clase Registrarse.

            Crea la pantalla, un QWidget, que contiene un título
            descriptivo, un QLabel, cuatro campos, QLineEdit, para
            ingresar nombre y apellido, usuario, contraseña y confirmar
            contraseña respectivamente, acompañados de labels
            descriptivos, QLabel, dos botonos para mostrar las
            contraseñas, QCheckBox, un boton para registrarse,
            QPushButton, y otro para ir a la pantalla de inicio de 
            sesión, también QPushButton.
    """

    def __init__(self):
        super().__init__()

        titulo = qtw.QLabel("Regístrate")
        titulo.setObjectName("titulo-grande")

        subtitulo = qtw.QLabel(
            "Recuerda que, para acceder a las bases de datos de gestión,\ntu registro debe ser autorizado por el administrador.")
        subtitulo.setObjectName("subtitulo")
        subtitulo.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)

        label1 = qtw.QLabel("Nombre y Apellido: ")
        label2 = qtw.QLabel("Usuario: ")
        label3 = qtw.QLabel("Contraseña: ")
        label4 = qtw.QLabel("Confirmar contraseña: ")

        label1.setObjectName("ingresar-label")
        label2.setObjectName("ingresar-label")
        label3.setObjectName("ingresar-label")
        label4.setObjectName("ingresar-label")

        self.entry1 = qtw.QLineEdit()
        self.entry2 = qtw.QLineEdit()
        self.entry3 = qtw.QLineEdit()
        self.entry4 = qtw.QLineEdit()
        self.entry1.setObjectName("modificar-entry")
        self.entry2.setObjectName("modificar-entry")
        self.entry3.setObjectName("modificar-entry")
        self.entry4.setObjectName("modificar-entry")
        self.entry2.setMaxLength(20)
        self.entry3.setMaxLength(20)
        self.entry4.setMaxLength(20)
        self.entry1.returnPressed.connect(lambda: self.entry2.setFocus())
        self.entry2.returnPressed.connect(lambda: self.entry3.setFocus())
        self.entry3.returnPressed.connect(lambda: self.entry4.setFocus())

        mostrarContrasena1 = BotonMostrarContrasena(self.entry3)
        mostrarContrasena2 = BotonMostrarContrasena(self.entry4)

        self.confirmar = qtw.QPushButton("confirmar")
        self.confirmar.setObjectName("confirmar-grande")
        self.confirmar.setCursor(qtg.QCursor(
            qtc.Qt.CursorShape.PointingHandCursor))

        self.ingresar = qtw.QPushButton("¿Ya estás registrado? Inicia sesión.")
        self.ingresar.setObjectName("boton-texto")
        self.ingresar.setCursor(qtg.QCursor(
            qtc.Qt.CursorShape.PointingHandCursor))

        layout = qtw.QGridLayout()
        layout.addWidget(titulo, 0, 0, 1, 3,
                         alignment=qtc.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitulo, 1, 0, 1, 3,
                         alignment=qtc.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(
            label1, 2, 0, alignment=qtc.Qt.AlignmentFlag.AlignRight)
        layout.addWidget(
            label2, 3, 0, alignment=qtc.Qt.AlignmentFlag.AlignRight)
        layout.addWidget(
            label3, 4, 0, alignment=qtc.Qt.AlignmentFlag.AlignRight)
        layout.addWidget(
            label4, 5, 0, alignment=qtc.Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.entry1, 2, 1)
        layout.addWidget(self.entry2, 3, 1)
        layout.addWidget(self.entry3, 4, 1)
        layout.addWidget(self.entry4, 5, 1)
        layout.addWidget(mostrarContrasena1, 4, 2)
        layout.addWidget(mostrarContrasena2, 5, 2)
        layout.addWidget(self.confirmar, 6, 0, 1, 3,
                         alignment=qtc.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.ingresar, 7, 0, 1, 3,
                         alignment=qtc.Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
