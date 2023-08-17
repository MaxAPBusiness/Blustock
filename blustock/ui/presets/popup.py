"""Este módulo contiene una clase que genera un mensaje emergente.

Clases
---------
    PopUp(QMessageBox()):
        Genera un mensaje emergente.
"""
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt

class PopUp(QMessageBox):
    """Esta clase genera un mensaje emergente.

    Hereda: QMessageBox
    
    Parámetros
    ----------
        type : str
            El tipo de ventana: botones, ícono y título.
        info : str
            La información adicional del mensaje.
    """
    def __init__(self, type, info):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        # Dependiendo del título, cambia el tipo de ventana y su ícono.
        # Los iconos son: critical (La cruz), warning (El triangulo 
        # amarillo con el !) y Information (una i en un dialogo azul)
        if type == "Error":
            self.setIcon(QMessageBox.Icon.Critical)
            # Método setStandardButtons: elije los botones del mensaje.
            # Ok significa que va a tener un boton que dice ok.
            self.setStandardButtons(QMessageBox.StandardButton.Cancel |QMessageBox.StandardButton.Ok)
            self.setWindowTitle(type)
            self.setText(type)
        elif type == "Advertencia":
            self.setIcon(QMessageBox.Icon.Warning)
            self.setStandardButtons(QMessageBox.StandardButton.Cancel |QMessageBox.StandardButton.Ok)
            self.setWindowTitle(type)
            self.setText(type)
        elif type == "Aviso":
            self.setIcon(QMessageBox.Icon.Information)
            self.setStandardButtons(QMessageBox.StandardButton.Cancel |QMessageBox.StandardButton.Ok)
            self.setWindowTitle(type)
            self.setText(type)
        elif type == "Turno":
            self.setIcon(QMessageBox.Icon.Question)
            self.setWindowTitle("Turno no finalizado")
            self.setText("Pregunta")
            self.setStandardButtons(
            QMessageBox.StandardButton.Cancel |
            QMessageBox.StandardButton.No |
            QMessageBox.StandardButton.Yes)
            self.button(QMessageBox.StandardButton.Yes).setText("Continuar turno")
            self.button(QMessageBox.StandardButton.No).setText("Finalizar turno")
        elif type[:8] == 'Pregunta':
            if type == "Pregunta":
                self.setIcon(QMessageBox.Icon.Warning)
                self.setWindowTitle("Advertencia")
                self.setText("Advertencia")
                self.setStandardButtons(
                    QMessageBox.StandardButton.Cancel |
                    QMessageBox.StandardButton.No |
                    QMessageBox.StandardButton.Yes)
            elif type == "Pregunta-Info":
                self.setIcon(QMessageBox.Icon.Information)
                self.setWindowTitle("Pregunta")
                self.setText("Pregunta")
                self.setStandardButtons(
                    QMessageBox.StandardButton.Cancel |
                    QMessageBox.StandardButton.No |
                    QMessageBox.StandardButton.Yes)
            # Va a tener dos botones, uno de no y uno de sí.
            # Obtenemos el boton sí para cambiarle el texto, asi dice
            # sí en vez de yes.
            self.button(QMessageBox.StandardButton.Yes).setText("Sí")
        
        self.button(QMessageBox.StandardButton.Cancel).hide()
        # Método setInformativeText: establece el texto informativo.
        # Tiene un dedent para quitar la identación del código y que se
        # muestre bien, sino tiene márgen de más.
        self.setInformativeText(info)
