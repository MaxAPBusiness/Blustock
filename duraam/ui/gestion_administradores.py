"""Este módulo crea una pantalla para gestionar la tabla de
administradores. 

Clases
------
    GestionAdministradores:
        Crea una pantalla para gestionar la tabla de administradores.
"""
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import db.inicializar_bbdd as db
import os

from registrar_cambios import registrarCambios
import mostrar_mensaje as m


class GestionDeAdministradores(qtw.QWidget):
    """Esta clase crea una pantalla para gestionar la tabla de
    administradores.

    Hereda: PyQt6.QtWidgets.QWidget

    Atributos
    ---------
        tabla : QTableWidget
            la tabla de la pantalla.
        campos : tuple
            los títulos de las columnas de la tabla.
        
    Métodos
    -------
        __init__(self):
            El constructor de la clase GestionAdministradores.

            Crea la pantalla, un QWidget, que contiene una tabla, un
            QTableWidget, que muestra los datos de la tabla
            administradores y botones para degradar su rol.
            
            Ver también
            -----------
            mostrarDatos: obtiene los datos de la tabla administradores
                          y los introduce en la tabla de la pantalla.

        mostrarDatos(self):
            Obtiene los datos de la tabla administradores y los
            introduce en la tabla de la pantalla.

        degradar(self):
            Degrada el rol del administrador a usuario.
    """
    def __init__(self):
        super().__init__()

        self.titulo=qtw.QLabel("Gestión de administradores")
        self.titulo.setObjectName("titulo")

        self.tabla = qtw.QTableWidget(self)
        self.tabla.setObjectName("tabla")
        self.campos = ("Usuario", "Nombre y Apellido", "")                          
        self.tabla.setColumnCount(len(self.campos))
        self.tabla.setHorizontalHeaderLabels(self.campos)
        self.tabla.verticalHeader().hide()
        self.tabla.setColumnWidth(1, 125)
        self.tabla.setColumnWidth(2, 35)
        self.mostrarDatos()

        layout = qtw.QVBoxLayout()
        layout.addWidget(self.titulo)
        layout.addWidget(self.tabla)
        self.setLayout(layout)

    def mostrarDatos(self):
        """Este método obtiene los datos de la tabla administradores y
        los introduce en la tabla de la pantalla.
        """
        db.cur.execute("SELECT usuario, nombre_apellido FROM administradores")
        consulta = db.cur.fetchall()

        self.tabla.setRowCount(len(consulta))

        for i in range(len(consulta)):
            for j in range(len(consulta[i])):
                self.tabla.setItem(i, j, qtw.QTableWidgetItem(str(consulta[i][j])))
            self.tabla.setRowHeight(i, 35)

            # Se crea el boton de editar con sus elementos necesarios.
            botonDegradar = qtw.QPushButton()
            botonDegradar.setIcon(
                qtg.QIcon(
                    qtg.QPixmap(
                        f"{os.path.abspath(os.getcwd())}/duraam/images/degradar.png"
                        )
                    )
                )
            botonDegradar.setIconSize(qtc.QSize(25, 25))
            botonDegradar.setObjectName("aceptar")
            botonDegradar.clicked.connect(lambda: self.degradar())
            botonDegradar.setCursor(qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor))
            self.tabla.setCellWidget(i, len(self.campos)-1, botonDegradar)

    def degradar(self):
        """Degrada el rol del administrador a usuario.

        Elimina la fila de la tabla de administradores y la añade a la
        tabla de usuarios.
        """
        # se le pregunta al usuario si desea degradar el administrador.
        resp = m.mostrarMensaje("Pregunta", "Advertencia",
            "¿Está seguro que desea degradar al administrador?")
        # si pulsó el boton de sí sigue el código.
        if resp == qtw.QMessageBox.StandardButton.Yes:    
            botonClickeado = qtw.QApplication.focusWidget()
            posicion = self.tabla.indexAt(botonClickeado.pos())
            idd=posicion.sibling(posicion.row(), 0).data()
            # Obtiene los datos del admin
            db.cur.execute(
                "SELECT * FROM administradores WHERE usuario = ?", 
                (idd,)
                ) 
            datos=db.cur.fetchall()

            # Lo quita de la tabla de administradores y lo inserta en
            # la tabla de usuarios.
            db.cur.execute(
                "INSERT INTO usuarios VALUES (?, ?, ?, ?)",
                datos[0]
                )
            db.cur.execute(
                "DELETE FROM administradores WHERE usuario = ?", 
                (datos[0][1],)
                )

            # Se guardan los cambios y bla bla bla.
            registrarCambios(
                "Descenso", "Administradores Usuarios",
                datos[0][0], None, 
                f"Nombre: {datos[0][3]} Usuario: {datos[0][1]}"
                )
            db.con.commit()
            self.mostrarDatos()