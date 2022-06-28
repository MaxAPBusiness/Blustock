import PyQt6.QtWidgets as qtw

# Función mostrarMensaje: muestra un mensaje en la pantalla. Los argumentos son:
# - title: funciona como el título del mensaje y también se usa para identificar el tipo de mensaje. Los tipos son:
# - - Error: muestra un error.
# - - Advertencia: muestra una advertencia en la pantalla.
# - - Aviso / Information: muestra información al usuario.
# - - Pregunta: le pregunta algo al usuario. En este caso, también cambian los botones en relación al resto.
# - msg: el mensaje principal que se muestra.
# - info: la información adicional del mensaje.
def mostrarMensaje(title, msg, info):
    # Se crea el messagebox
    window = qtw.QMessageBox()

    # Dependiendo del valor de title, cambia el icono y sus botones correspondientes.
    if title == "Error":
        window.setIcon(qtw.QMessageBox.Icon.Critical)
        window.setStandardButtons(qtw.QMessageBox.StandardButton.Ok)
    elif title == "Advertencia" or title == "Warning":
        window.setIcon(qtw.QMessageBox.Icon.Warning)
        window.setStandardButtons(qtw.QMessageBox.StandardButton.Ok)
    elif title == "Aviso" or title == "Information":
        window.setIcon(qtw.QMessageBox.Icon.Information)
        window.setStandardButtons(qtw.QMessageBox.StandardButton.Ok)
    elif title == "Pregunta" or title == "Question":
        window.setIcon(qtw.QMessageBox.Icon.Warning)
        window.setStandardButtons(
            qtw.QMessageBox.StandardButton.No | qtw.QMessageBox.StandardButton.Yes)
    else:
        print("Error de titulo")
        return
    
    # Se le da el título, el mensaje y la información adicional respectivamente.
    window.setWindowTitle(title)
    window.setText(msg)
    window.setInformativeText(info)

    # La ventana se ejecuta. El return está para obtener la respuesta que el usuario dió en el caso de que algo se le preguntara.
    return window.exec()