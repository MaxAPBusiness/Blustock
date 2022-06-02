import sys
import PyQt6.QtWidgets as qtw
import gestion_herramientas
import os


# Creamos la ventana principal
class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1280, 1024)

        # Creamos la colección de pantallas
        stack = qtw.QStackedWidget()
        self.herramientas=gestion_herramientas.GestionHerramientas()

        # Añadimos las pantallas a la colección
        for i in [self.herramientas]:
            stack.addWidget(i)

        # Añadimos la colección a la ventana
        self.setCentralWidget(stack)
        stack.setSizePolicy(
            qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Expanding)


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    with open(f"{os.path.abspath(os.getcwd())}/duraam/gestion.qss", 'r') as css:
        window.setStyleSheet(css.read())
    window.show()
    app.exec()
