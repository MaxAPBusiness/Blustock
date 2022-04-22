import PyQt6.QtWidgets as qtw


class IngresarEs(qtw.QWidget):
    def __init__(self):
        super().__init__()

        title = qtw.QLabel("Log In")
        label1 = qtw.QLabel("User: ")
        label2 = qtw.QLabel("Password: ")

        entry1 = qtw.QLineEdit()
        entry2 = qtw.QLineEdit()
        entry2.setEchoMode(qtw.QLineEdit.EchoMode.Password)

        self.submit=qtw.QPushButton("Log in")

        layout = qtw.QGridLayout()

        layout.addWidget(title, 0, 0, 1,0)
        layout.addWidget(label1, 1, 0)
        layout.addWidget(label2, 2, 0)

        layout.addWidget(entry1, 1, 1)
        layout.addWidget(entry2, 2, 1)
        layout.addWidget(self.submit, 3, 0, 1, 0)

        self.setLayout(layout)

