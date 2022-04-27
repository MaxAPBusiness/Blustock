import PyQt6.QtWidgets as qtw


class IngresarEn(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.back = qtw.QPushButton("<-- Back")

        title = qtw.QLabel("Log In")
        label1 = qtw.QLabel("User: ")
        label2 = qtw.QLabel("Password: ")

        entry1 = qtw.QLineEdit()
        entry2 = qtw.QLineEdit()
        entry2.setEchoMode(qtw.QLineEdit.EchoMode.Password)

        submit = qtw.QPushButton("Log In")
        self.button1 = qtw.QPushButton("¿Need registration? Register")

        layout = qtw.QGridLayout()
        layout.addWidget(self.back, 0, 0)
        layout.addWidget(title, 1, 0, 1, 0)
        layout.addWidget(label1, 2, 0)
        layout.addWidget(label2, 3, 0)
        layout.addWidget(entry1, 2, 1)
        layout.addWidget(entry2, 3, 1)
        layout.addWidget(submit, 4, 0, 1, 0)
        layout.addWidget(self.button1, 5, 0, 1, 0)

        self.setLayout(layout)
