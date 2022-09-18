"""Este módulo crea una pantalla para gestionar la tabla de profesores.

Clases
------
    GestionProfesores(qtw.QWidget):
        Crea una pantalla para gestionar la tabla de profesores.
"""
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import os
import sqlite3

import db.inicializar_bbdd as db
from botones import BotonOrdenar, BotonEditar, BotonEliminar
import mostrar_mensaje as m
from registrar_cambios import registrarCambios


class GestionProfesores(qtw.QWidget):
    """Esta clase crea una pantalla para gestionar la tabla profesores.

    Hereda: PyQt6.QtWidgets.QWidget

    Atributos
    ---------
        tabla : QTableWidget
            La tabla de la pantalla.
        campos : tuple
            Los títulos de las columnas de la tabla.
        barraBusqueda : QLineEdit
            La barra de búsqueda.
        radioNombre : QRadioButton
            El botón de radio para ordenar los datos de la tabla por
            nombre.
        radioDNI : QRadioButton
            El botón de radio para ordenar los datos de la tabla por
            DNI.
        botonOrdenar : QPushButton
            Un botón para ordenar los datos de manera ascendente o
            descendente.

    Métodos
    -------
        __init__(self):
            El constructor de la clase GestionProfesores.

            Crea la pantalla, un QWidget, que contiene: un título
            descriptivo, un QLabel; una tabla, un QTableWidget, que
            muestra los datos de la tabla profesores y contiene botones
            para editarlos; una barra de buscador, un QLineEdit, para
            buscar los datos; botones de radio, QRadioWidget, para
            ordenar los datos mostrados según un dato seleccionado, un
            botón, QCheckBox, para ordenar los datos mostrados de
            manera ascendente o descendente según el boton presionado;
            un botón, un QPushButton, para insertar datos a la tabla.

        mostrarDatos(self):
            Obtiene los datos de la tabla profesores y los introduce en 
            la tabla de la pantalla.

        ordenar(self):
            Llama a la función cambiarIcono y al método mostrarDatos.

        modificarLinea(self, tipo):
            Crea un formulario para insertar o editar datos en la tabla
            profesores.

        confirmarModificacion(self, tipo, datosPorDefecto=None):
            Modifica los datos de la tabla profesores.

        eliminar(self):
            Elimina la fila de la tabla profesores.
    """

    def __init__(self):
        super().__init__()

        self.titulo = qtw.QLabel("GESTIÓN DE profesores")
        self.titulo.setObjectName("titulo")

        self.tabla = qtw.QTableWidget(self)
        self.tabla.setObjectName("tabla")
        self.campos = ("ID", "DNI", "Nombre y Apellido", "Email", "", "")
        self.tabla.setColumnCount(len(self.campos))
        self.tabla.setHorizontalHeaderLabels(self.campos)
        self.tabla.verticalHeader().hide()
        self.tabla.setColumnWidth(2, 120)
        self.tabla.setColumnWidth(3, 200)
        self.tabla.setColumnWidth(4, 35)
        self.tabla.setColumnWidth(5, 35)

        self.barraBusqueda = qtw.QLineEdit()
        self.barraBusqueda.setObjectName("buscar")
        self.barraBusqueda.setClearButtonEnabled(True)
        self.barraBusqueda.setPlaceholderText("Buscar...")
        self.barraBusqueda.textEdited.connect(lambda: self.mostrarDatos())

        iconoLupa = qtg.QPixmap(
            f"{os.path.abspath(os.getcwd())}/duraam/images/buscar.png")
        contenedorIconoLupa = qtw.QLabel()
        contenedorIconoLupa.setObjectName("lupa")
        contenedorIconoLupa.setPixmap(iconoLupa)

        labelOrdenar = qtw.QLabel("Ordenar por: ")
        self.radioNombre = qtw.QRadioButton("Nombre")
        self.radioDNI = qtw.QRadioButton("DNI")
        self.radioNombre.setObjectName("Radio1")
        self.radioDNI.setObjectName("Radio2")
        self.radioNombre.toggled.connect(lambda: self.mostrarDatos())
        self.radioDNI.toggled.connect(lambda: self.mostrarDatos())

        self.botonOrdenar = BotonOrdenar()
        self.botonOrdenar.stateChanged.connect(lambda: self.ordenar())

        self.agregar = qtw.QPushButton("Agregar")
        self.agregar.setObjectName("agregar")
        self.agregar.clicked.connect(
            lambda: self.modificarLinea("agregar"))
        self.agregar.setCursor(qtg.QCursor(
            qtc.Qt.CursorShape.PointingHandCursor))

        layout = qtw.QGridLayout()
        layout.addWidget(self.titulo, 0, 0)
        layout.addWidget(self.barraBusqueda, 1, 0)
        layout.addWidget(contenedorIconoLupa, 1, 0)
        layout.addWidget(labelOrdenar, 1, 1)
        layout.addWidget(self.radioNombre, 1, 2)
        layout.addWidget(self.radioDNI, 1, 3)
        layout.addWidget(self.botonOrdenar, 1, 4)
        layout.addWidget(self.tabla, 2, 0, 1, 9)
        layout.addWidget(self.agregar, 3, 0)
        self.setLayout(layout)
        self.mostrarDatos()

    def mostrarDatos(self):
        """Este método obtiene los datos de la tabla profesores y los
        introduce en la tabla de la pantalla.
        """
        if self.radioNombre.isChecked():
            orden = "ORDER BY nombre_apellido"
        elif self.radioDNI.isChecked():
            orden = "ORDER BY dni"
        else:
            orden = ""

        if orden and self.botonOrdenar.isChecked():
            orden += " ASC"

        db.cur.execute(
            f"""
            SELECT * FROM profesores
            WHERE ID LIKE ? 
            OR ID LIKE ?
            OR nombre_apellido LIKE ?  
            OR email LIKE ?
            {orden}
            """, (
                f"{self.barraBusqueda.text()}", f"{self.barraBusqueda.text()}",
                f"{self.barraBusqueda.text()}", f"{self.barraBusqueda.text()}",
            )
        )

        consulta = db.cur.fetchall()
        self.tabla.setRowCount(len(consulta))
        for i in range(len(consulta)):
            for j in range(len(consulta[i])):
                self.tabla.setItem(
                    i, j, qtw.QTableWidgetItem(str(consulta[i][j])))

            self.tabla.setRowHeight(i, 35)

            botonEditar = BotonEditar()
            botonEditar.clicked.connect(lambda: self.modificarLinea("editar"))
            self.tabla.setCellWidget(i, 4, botonEditar)

            botonEliminar = BotonEliminar()
            botonEliminar.clicked.connect(lambda: self.eliminar())
            self.tabla.setCellWidget(i, 5, botonEliminar)

    def ordenar(self):
        """Este método cambia el ícono del botonOrdenar y actualiza los
        datos de la tabla de la pantalla."""
        self.botonOrdenar.cambiarIcono()
        self.mostrarDatos()

    def modificarLinea(self, tipo: str):
        """Este método crea un formulario para insertar o editar datos
        en la tabla profesores.

        El formulario es un QWidget que funciona como ventana. Por cada
        campo de la fila, agrega un entry (QLineEdit o QSpinbox) y un
        label descriptivo. Al confirmar los datos, ejecuta el método 
        confirmarModificacion.

        Parámetros
        ----------
            tipo : str
                el tipo de formulario.

        Ver también
        -----------
        confirmarModificacion: modifica los datos de la tabla profesores.
        """
        self.ventanaEditar = qtw.QWidget()
        self.ventanaEditar.setWindowTitle("Agregar Profesor")
        self.ventanaEditar.setWindowIcon(
            qtg.QIcon(f"{os.path.abspath(os.getcwd())}/duraam/images/logo.png"))

        layoutVentanaModificar = qtw.QGridLayout()

        for i in range(len(self.campos)-1):
            label = qtw.QLabel(f"{self.campos[i]}: ")
            label.setObjectName("modificar-label")
            layoutVentanaModificar.addWidget(
                label, i, 0, alignment=qtc.Qt.AlignmentFlag.AlignRight)

        self.entry1 = qtw.QLineEdit()
        self.entry2 = qtw.QSpinBox()
        self.entry3 = qtw.QLineEdit()
        self.entry4 = qtw.QLineEdit()

        self.entry1.setMaxLength(4)
        self.entry2.setMaximum(99999999)
        self.entry3.setMaxLength(50)
        self.entry3.setMaxLength(320)

        datos = []

        if tipo == "editar":
            botonClickeado = qtw.QApplication.focusWidget()
            posicion = self.tabla.indexAt(botonClickeado.pos())

            for cell in range(0, 4):
                datos.append(posicion.sibling(posicion.row(), cell).data())

            self.entry1.setText(datos[0])
            self.entry2.setValue(int(datos[1]))
            self.entry3.setText(datos[2])
            self.entry4.setText(datos[3])

            self.ventanaEditar.setWindowTitle("Editar")

        entries = [self.entry1, self.entry2, self.entry3, self.entry4]
        for i in range(len(entries)):
            entries[i].setObjectName("modificar-entry")
            layoutVentanaModificar.addWidget(entries[i], i, 1)

        botonConfirmar = qtw.QPushButton("Confirmar")
        botonConfirmar.setObjectName("confirmar")
        botonConfirmar.setWindowIcon(
            qtg.QIcon(f"{os.path.abspath(os.getcwd())}/duraam/images/logo.png"))
        botonConfirmar.clicked.connect(
            lambda: self.confirmarModificacion(datos))
        layoutVentanaModificar.addWidget(
            botonConfirmar, i+1, 0, 1, 2, alignment=qtc.Qt.AlignmentFlag.AlignCenter)

        self.ventanaEditar.setLayout(layoutVentanaModificar)
        self.ventanaEditar.show()

    def confirmarModificacion(self, tipo: str, datosPorDefecto: list | None = None):
        """Este método modifica los datos de la tabla profesores.

        Verifica que el id no esté repetido en profesores históricos.
        Luego intenta realizar los cambios, registrarlos en el 
        historial, notificar al usuario el éxito de la operacion, 
        actualizar la tabla de la pantalla y cerrar el formulario. Si
        la base de datos arroja un sqlite3.IntegrityError durante el
        intento, le notifica al usuario que se ha repetido un valor
        único y termina la ejecución de la función, sin modificar la
        tabla.

        Parámetros
        ----------
            tipo : str
                El tipo de modificación.
            datosPorDefecto : list, default = None
                Los datos de la fila previos a la modificación. 

        Ver también
        -----------
        modificarLinea: crea un formulario para insertar o editar datos
                        en la tabla profesores.
        """
        db.cur.execute(
            "SELECT id FROM profesores_historicos WHERE id = ?", (self.entry1.text(),))
        if db.cur.fetchall():
            return m.mostrarMensaje("Error", "Error",
                                    "El ID ingresado ya está registrado en la tabla profesores históricos. Por favor, ingrese otro.")
        datosNuevos = (
            self.entry1.text(), self.entry2.value(
            ), self.entry3.text().upper(), self.entry4.text()
        )
        if tipo == "editar":
            try:
                db.cur.execute(
                    "SELECT * FROM profesores WHERE ID = ?", (datosPorDefecto[0], ))
                datosViejos = db.cur.fetchall()[0]
                db.cur.execute("""
                UPDATE profesores
                SET ID = ?, dni = ?, nombre_apellido = ?, email = ?
                where id  = ?
                """, (
                    datosNuevos[0], datosNuevos[1], datosNuevos[2], datosNuevos[3], datosPorDefecto[0],
                ))
                registrarCambios(
                    "Edicion", "Profesores", datosPorDefecto[0][0], f"{datosViejos}", f"{datosNuevos}")
                db.con.commit()
                m.mostrarMensaje("Information", "Aviso",
                                 "Se ha actualizado el profesor.")
            except sqlite3.IntegrityError:
                return m.mostrarMensaje("Error", "Error", "El ID ingresado ya está registrado. Por favor, ingrese otro.")
        else:
            try:
                db.cur.execute("INSERT INTO profesores VALUES(?, ? , ?, ?) ", (
                    self.entry1.text(), self.entry2.value(),
                    self.entry3.text().upper(), self.entry4.text(),
                ))
                registrarCambios("Insercion", "Profesores",
                                 datosNuevos[0], None, f"{datosNuevos}")
                db.con.commit()

                m.mostrarMensaje("Information", "Aviso",
                                 "Se ha ingresado un Profesor.")
            except sqlite3.IntegrityError:
                return m.mostrarMensaje("Error", "Error", "El ID ingresado ya está registrado. Por favor, ingrese otro.")

        self.mostrarDatos()
        self.ventanaEditar.close()

    def eliminar(self):
        """Este método elimina la fila de la tabla profesores.

        Antes de eliminar, confirma la decisión del usuario.
        Si los datos están relacionados con otras tablas, vuelve a
        confirmar la decisión del usuario. Luego, elimina la fila de la
        tabla profesores y las filas en donde los datos estaban
        relacionados. Por último, registra los cambios y actualiza la
        tabla.
        """
        respuesta = m.mostrarMensaje("Pregunta", "Advertencia",
                                     "¿Está seguro que desea eliminar estos datos?")
        if respuesta == qtw.QMessageBox.StandardButton.Yes:
            botonClickeado = qtw.QApplication.focusWidget()
            posicion = self.tabla.indexAt(botonClickeado.pos())
            idd = posicion.sibling(posicion.row(), 0).data()

            db.cur.execute(
                "SELECT * FROM MOVIMIENTOS_HERRAMIENTAS WHERE CLASE=0 AND ID_PERSONA = ?", (idd,))
            movimientos = db.cur.fetchall()
            db.cur.execute(
                "SELECT * FROM TURNO_PANOL WHERE profesor_ingreso = ? OR profesor_egreso = ?", (idd, idd,))
            turnos = db.cur.fetchall()
            tipo = "Eliminacion simple"
            tablas = "Profesores"
            if movimientos or turnos:
                tipo = "Eliminacion compleja"
                tablas = "Profesores Movimientos de herramientas"
                respuesta = m.mostrarMensaje("Pregunta", "Advertencia",
                                             """
                    El profesor tiene turnos y/o movimientos registrados. 
                    Es recomendable que lo pase a registro histórico, quedando
                    eliminado de profesores vigentes pero su información relacionada
                    y sus datos siguen registrados en la base de datos. Eliminarlo 
                    eliminará toda la información relacionada, como sus turnos y sus movimientos.
                    ¿Está seguro que desea continuar y eliminar la información relacionada?
                    """)

        if respuesta == qtw.QMessageBox.StandardButton.Yes:
            db.cur.execute("SELECT * FROM profesores WHERE ID = ?", (idd,))
            datosEliminados = db.cur.fetchall()[0]
            db.cur.execute("DELETE FROM profesores WHERE ID = ?", (idd,))
            db.cur.execute(
                "DELETE FROM MOVIMIENTOS_HERRAMIENTAS WHERE CLASE=0 AND ID_PERSONA = ?", (idd,))
            db.cur.execute(
                "UPDATE TURNO_PANOL SET profesor_ingreso = NULL WHERE profesor_ingreso = ?", (idd,))
            db.cur.execute(
                "UPDATE TURNO_PANOL SET profesor_egreso = NULL WHERE profesor_egreso = ?", (idd,))
            registrarCambios(tipo, tablas, idd, f"{datosEliminados}", None)
            db.con.commit()
            self.mostrarDatos()
