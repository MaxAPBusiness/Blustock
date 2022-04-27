import PyQt6.QtWidgets as qtw


class Lenguaje(qtw.QWidget):
    def __init__(self):
        super().__init__()

        title = qtw.QLabel("Seleccionar Idioma / Select Language")
        self.button1 = qtw.QPushButton("Español")
        self.button2 = qtw.QPushButton("English")

        layout = qtw.QVBoxLayout()

        layout.addWidget(title)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)

        self.setLayout(layout)
