"""Este módulo contiene una clase para crear lineEdits parametrizados
para celdas de una tabla de la ui.
"""
from PyQt6 import QtWidgets, QtCore


class ParamEdit(QtWidgets.QLineEdit):
    """Esta clase crea un lineEdit con un campo de sugerencia.
    
    Hereda: QtWidgets.QLineEdit

    Atributos
    ---------
        sugerencias: list | tuple
            Las sugerencias que va a tener el cuadro de sugerencias.
        texto: str
            El texto que estará por defecto en el lineEdit.
    """
    def __init__(self, sugerencias: list | tuple, texto: str):
        super().__init__()
        self.setObjectName('paramEdit')
        self.setText(texto)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        cuadroSugerencias = QtWidgets.QCompleter(sugerencias, self)
        cuadroSugerencias.setCaseSensitivity(
            QtCore.Qt.CaseSensitivity.CaseInsensitive)
        # Se introduce el cuadro de sugerencias en el entry.
        self.setCompleter(cuadroSugerencias)



