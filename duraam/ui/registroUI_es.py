import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc


class RegistrarEs(qtw.QWidget):
    def __init__(self):
        super().__init__()

        title = qtw.QLabel("Registrarse")
        title.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)

        label1 = qtw.QLabel("Nombre: ")
        label2 = qtw.QLabel("Apellido: ")
        label3 = qtw.QLabel("DNI: ")
        label4 = qtw.QLabel("Usuario: ")
        label5 = qtw.QLabel("Email: ")
        label6 = qtw.QLabel("Contraseña: ")
        label7 = qtw.QLabel("Repetir contraseña: ")

        entry1 = qtw.QLineEdit()
        entry2 = qtw.QLineEdit()
        entry3 = qtw.QLineEdit()
        entry4 = qtw.QLineEdit()
        entry5 = qtw.QLineEdit()
        entry6 = qtw.QLineEdit()
        entry7 = qtw.QLineEdit()
        entry6.setEchoMode(qtw.QLineEdit.EchoMode.Password)
        entry7.setEchoMode(qtw.QLineEdit.EchoMode.Password)

        self.submit = qtw.QPushButton("Registrarse")
        self.button1 = qtw.QPushButton("¿Ya estás registrado? Inicia sesión")

        widgets = (label1, label2, label3, label4, label5, label6, label7,
                   entry1, entry2, entry3, entry4, entry5, entry6, entry7)

        layout = qtw.QGridLayout()
        layout.addWidget(title, 0, 0, 1, 0)
        for i in range(0, 7):
            layout.addWidget(widgets[i], i+2, 0)
        for i in range(7, 14):
            widgets[i].setFixedWidth(120)
            layout.addWidget(widgets[i], i-5, 1)

        layout.addWidget(self.submit, 14, 0, 1, 0)
        layout.addWidget(self.button1, 15, 0, 1, 0)

        self.setLayout(layout)
