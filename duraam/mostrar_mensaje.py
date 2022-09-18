"""Este módulo crea una función para mostrar un mensaje en la pantalla.

Funciones
---------
    mostrarMensaje(title: str, msg: str, info: str):
        muestra un mensaje en la pantalla.
"""
import PyQt6.QtWidgets as qtw
from textwrap import dedent


def mostrarMensaje(title: str, msg: str, info: str):
    """Esta función muestra un mensaje en la pantalla.

    Parámetros
    ----------
        title : str
            El título y el tipo de ventana del mensaje.
        msg : str
            El título del mensaje.
        info : str
            La información adicional del mensaje.
    """
    window = qtw.QMessageBox()

    # Dependiendo del título, cambia el tipo de ventana y su ícono.
    # Los iconos son: critical (La cruz), warning (El triangulo 
    # amarillo con el !) y Information (una i en un dialogo azul)
    if title == "Error":
        window.setIcon(qtw.QMessageBox.Icon.Critical)

        # Método setStandardButtons: elije los botones del mensaje.
        # Ok significa que va a tener un boton que dice ok.
        window.setStandardButtons(qtw.QMessageBox.StandardButton.Ok)
    elif title == "Advertencia" or title == "Warning":
        window.setIcon(qtw.QMessageBox.Icon.Warning)
        window.setStandardButtons(qtw.QMessageBox.StandardButton.Ok)
    elif title == "Aviso" or title == "Information":
        window.setIcon(qtw.QMessageBox.Icon.Information)
        window.setStandardButtons(qtw.QMessageBox.StandardButton.Ok)
    # Si el tip
    elif title == "Pregunta" or title == "Question":
        window.setIcon(qtw.QMessageBox.Icon.Warning)
        # Va a tener dos botones, uno de no y uno de sí.
        window.setStandardButtons(
            qtw.QMessageBox.StandardButton.No | qtw.QMessageBox.StandardButton.Yes)
        # Obtenemos el boton sí para cambiarle el texto, asi se
        # sí en vez de yes.
        si = window.button(qtw.QMessageBox.StandardButton.Yes)
        si.setText("Sí")
    else:
        return print("Error de titulo")

    window.setWindowTitle(title)

    #Método setText: establece el texto inicial o título.
    window.setText(msg)
    # Método setInformativeText: establece el texto informativo.
    # Tiene un dedent para quitar la identación del código y que se
    # muestre bien, sino tiene márgen de más.
    window.setInformativeText(dedent(info))

    return window.exec()