import sys
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import ui.langUI
import ui.IngresarUI_en
import ui.IngresarUI_es
import ui.registroUI_es

app = qtw.QApplication(sys.argv)

class Lang(ui.langUI.Lenguaje):
    def  __init__(self):
        super().__init__()
        self.button2.clicked.connect(lambda:self.clicked2())

    def clicked2(self):
        self.setCentralWidget(IngresarEs)


class IngresarEs(ui.IngresarUI_es.IngresarEs):
    def  __init__(self):
        super().__init__()
        self.submit.clicked.connect(lambda:print("Ingresando..."))
        self.button1.clicked.connect(lambda:self.setCentralWidget(RegistrarEs))

class IngresarEn(ui.IngresarUI_es.IngresarEs):
    def  __init__(self):
        super().__init__()
        self.submit.clicked.connect(lambda:print("Ingresando..."))
        self.button1.clicked.connect(lambda:self.setCentralWidget(RegistrarEs))


class RegistrarEs(ui.registroUI_es.RegistrarEs):
    def  __init__(self):
        super().__init__()
        self.button1.clicked.connect(lambda:self.setCentralWidget(IngresarEs))


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        lang=Lang()
        self.setCentralWidget(lang)
        lang.button1.clicked.connect(self.setCentralWidget(IngresarEs))
if __name__ == "__main__":

    window = MainWindow()
    window.show()
    app.exec()
