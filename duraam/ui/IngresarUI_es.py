import PyQt6.QtWidgets as qtw


class IngresarEs(qtw.QWidget):
    def __init__(self):
        super().__init__()

        title = qtw.QLabel("Ingresar")
        label1 = qtw.QLabel("Usuario: ")
        label2 = qtw.QLabel("Contraseña: ")

        entry1 = qtw.QLineEdit()
        entry2 = qtw.QLineEdit()
        entry2.setEchoMode(qtw.QLineEdit.EchoMode.Password)

        submit=qtw.QPushButton("Ingresar")
        button1=qtw.QPushButton("¿No estás ingresado? Ingresar")

        layout = qtw.QGridLayout()

        layout.addWidget(title, 0, 0, 1,0)
        layout.addWidget(label1, 1, 0)
        layout.addWidget(label2, 2, 0)
        layout.addWidget(entry1, 1, 1)
        layout.addWidget(entry2, 2, 1)
        layout.addWidget(submit, 3, 0, 1, 0)
        layout.addWidget(button1, 4, 0, 1,0)

        self.setLayout(layout)
