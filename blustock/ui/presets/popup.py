"""Este módulo crea una función para mostrar un mensaje en la pantalla.

Clases
---------
    PopUp(QMessageBox()):
        Genera un mensaje emergente.
"""
from PyQt6.QtWidgets import QMessageBox
from textwrap import dedent

class PopUp(QMessageBox):
    """Esta clase genera un mensaje emergente.

    Atributos
    ----------
        type : str
            El tipo de ventana: botones, ícono y título.
        info : str
            La información adicional del mensaje.
    """
    def __init__(self, type, info):
        super().__init__()

        # Dependiendo del título, cambia el tipo de ventana y su ícono.
        # Los iconos son: critical (La cruz), warning (El triangulo 
        # amarillo con el !) y Information (una i en un dialogo azul)
        if type == "Error":
            self.setIcon(QMessageBox.Icon.Critical)

            # Método setStandardButtons: elije los botones del mensaje.
            # Ok significa que va a tener un boton que dice ok.
            self.setStandardButtons(QMessageBox.StandardButton.Ok)
            self.setWindowTitle(type)
            self.setText(type)
        elif type == "Advertencia" or type == "Warning":
            self.setIcon(QMessageBox.Icon.Warning)
            self.setStandardButtons(QMessageBox.StandardButton.Ok)
            self.setWindowTitle(type)
            self.setText(type)
        elif type == "Aviso" or type == "Information":
            self.setIcon(QMessageBox.Icon.Information)
            self.setStandardButtons(QMessageBox.StandardButton.Ok)
            self.setWindowTitle(type)
            self.setText(type)
        elif type == "Pregunta" or type == "Question":
            self.setIcon(QMessageBox.Icon.Warning)
            # Va a tener dos botones, uno de no y uno de sí.
            self.setStandardButtons(
                QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes)
            # Obtenemos el boton sí para cambiarle el texto, asi dice
            # sí en vez de yes.
            si = self.button(QMessageBox.StandardButton.Yes)
            si.setText("Sí")
            self.setWindowTitle("Advertencia")
            self.setText(type)

        # Método setInformativeText: establece el texto informativo.
        # Tiene un dedent para quitar la identación del código y que se
        # muestre bien, sino tiene márgen de más.
        self.setInformativeText(dedent(info))
        # Se ejecuta la ventana emergente.
        self.exec()