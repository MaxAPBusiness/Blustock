"""Este módulo crea una pantalla para gestionar la tabla turno_panol.

Clases
------
    GestionTurnos(qtw.QWidget):
        Crea una pantalla para gestionar la tabla turno_panol.
"""
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import os

import db.inicializar_bbdd as db
from botones import BotonOrdenar, BotonEditar, BotonEliminar
import mostrar_mensaje as m
from registrar_cambios import registrarCambios


class GestionTurnos(qtw.QWidget):
    """Esta clase crea una pantalla para gestionar la tabla
    turno_panol.

    Hereda: PyQt6.QtWidgets.QWidget

    Atributos
    ---------
        tabla : QTableWidget
            La tabla de la pantalla.
        campos : tuple
            Los títulos de las columnas de la tabla.
        barraBusqueda : QLineEdit
            La barra de búsqueda.
        radioID : QRadioButton
            El botón de radio para ordenar por id.
        radioAlumno : QRadioButton
            El botón de radio para ordenar por alumno.
        radioFecha : QRadioButton
            El botón de radio para ordenar por fecha.

    Métodos
    -------
        __init__(self):
            El constructor de la clase GestionTurnos.

            Crea la pantalla, un QWidget, que contiene: un título
            descriptivo, un QLabel; una tabla, un QTableWidget, que
            muestra los datos de la tabla turno_panol y contiene
            botones para editarlos; una barra de buscador, un
            QLineEdit, para buscar los datos; tres botones de radio,
            QRadioButton, para ordenar los datos en base a columnas
            específicas; un botón, QCheckBox, para ordenar los datos
            mostrados de manera ascendente o descendente según el boton
            presionado; un botón, un QPushButton, para insertar datos a
            la tabla.

        mostrarDatos(self):
            Obtiene los datos de la tabla turno_panol y los introduce
            en la tabla de la pantalla.

        actualizarListas(self):
            Actualiza las listas de elementos.

        modificarLinea(self, tipo):
            Crea un formulario para insertar o editar datos en la tabla
            turno_panol.

        confirmarModificacion(self, tipo, datosPorDefecto=None):
            Modifica los datos de la tabla turno_panol.

        eliminar(self):
            Elimina la fila de la tabla turno_panol.
    """

    def __init__(self):
        super().__init__()

        self.titulo = qtw.QLabel("GESTIÓN DE TURNOS DEL PAÑOL")
        self.titulo.setObjectName("titulo")

        self.tabla = qtw.QTableWidget(self)
        self.tabla.setObjectName("tabla")
        self.campos = ("ID", "Fecha", "Alumno", "Horario Ingreso", "Horario Egreso", "Profesor Ingreso",
                       "Profesor Egreso", "", "")
        self.tabla.setColumnCount(len(self.campos))
        self.tabla.setHorizontalHeaderLabels(self.campos)
        self.tabla.verticalHeader().hide()
        self.tabla.setColumnWidth(5, 125)
        self.tabla.setColumnWidth(6, 125)
        self.tabla.setColumnWidth(7, 35)
        self.tabla.setColumnWidth(8, 35)

        self.barraBusqueda = qtw.QLineEdit()
        self.barraBusqueda.setObjectName("buscar")
        self.barraBusqueda.setClearButtonEnabled(True)
        self.barraBusqueda.setPlaceholderText("Buscar...")
        iconoLupa = qtg.QPixmap(
            f"{os.path.abspath(os.getcwd())}/duraam/images/buscar.png")
        contenedorIconoLupa = qtw.QLabel()
        contenedorIconoLupa.setObjectName("lupa")
        contenedorIconoLupa.setPixmap(iconoLupa)

        self.barraBusqueda.textEdited.connect(lambda: self.mostrarDatos())
        labelOrdenar = qtw.QLabel("Ordenar por: ")
        self.radioID = qtw.QRadioButton("ID")
        self.radioAlumno = qtw.QRadioButton("Alumno")
        self.radioFecha = qtw.QRadioButton("Fecha")
        self.radioID.setObjectName("Radio1")
        self.radioAlumno.setObjectName("Radio2")
        self.radioFecha.setObjectName("Radio3")
        self.radioID.toggled.connect(lambda: self.mostrarDatos())
        self.radioAlumno.toggled.connect(lambda: self.mostrarDatos())
        self.radioFecha.toggled.connect(lambda: self.mostrarDatos())

        self.botonOrdenar = BotonOrdenar()
        self.botonOrdenar.stateChanged.connect(lambda: self.ordenar())

        botonAgregar = qtw.QPushButton("Agregar")
        botonAgregar.setObjectName("agregar")
        botonAgregar.clicked.connect(
            lambda: self.modificarLinea("agregar"))
        botonAgregar.setCursor(qtg.QCursor(
            qtc.Qt.CursorShape.PointingHandCursor))

        layout = qtw.QVBoxLayout()
        layout.addWidget(self.titulo)
        contenedor1 = qtw.QWidget()
        contenedor1Layout = qtw.QGridLayout()
        contenedor1Layout.addWidget(self.barraBusqueda, 0, 0)
        contenedor1Layout.addWidget(contenedorIconoLupa, 0, 0)
        contenedor1Layout.addWidget(labelOrdenar, 0, 1)
        contenedor1Layout.addWidget(self.radioID, 0, 2)
        contenedor1Layout.addWidget(self.radioAlumno, 0, 3)
        contenedor1Layout.addWidget(self.radioFecha, 0, 4)
        contenedor1Layout.addWidget(self.botonOrdenar, 0, 5)
        contenedor1.setLayout(contenedor1Layout)
        layout.addWidget(contenedor1)
        layout.addWidget(self.tabla)
        layout.addWidget(botonAgregar)
        self.setLayout(layout)
        self.mostrarDatos()

    def mostrarDatos(self):
        """Este método obtiene los datos de la tabla herramientas y los
        introduce en la tabla de la pantalla.
        """
        if self.radioID.isChecked():
            orden = "ORDER BY t.id"
        elif self.radioAlumno.isChecked():
            orden = "ORDER BY nombre"
        elif self.radioFecha.isChecked():
            orden = "ORDER BY m.fecha_hora"
        else:
            orden = ""

        if orden and self.botonOrdenar.isChecked():
            orden += " ASC"
        
        # Explico lo que significa esta consulta enorme.
        # Selecciona primero el id y la fecha de la tabla turnos.
        # Luego ejecuta el comando case. Si no saben cual es, lean
        # primero la explicación de la consulta de movimientos
        # herramientas. Si el id del alumno está en la tabla
        # alumnos, entonces selecciona el nombre de la misma tabla.
        # Sino, selecciona el nombre de la tabla alumnos
        # historicos. Obtiene el nombre con el alias "alumno".
        # Luego, selecciona la hora de ingreso y de egreso del
        # turno. Después, verifica si el id del profesor de ingreso
        # está en la tabla profesores. Si lo está, selecciona el
        # nombre de la tabla profesores. Si no, selecciona el
        # nombre de la tabla profesores historicos. Hace lo mismo
        # con el id del profesor de egreso. Luego une todas las
        # tablas. Después, hace la comparación con lo buscado
        # en la barra de búsqueda
        db.cur.execute(
            f"""SELECT t.id, t.fecha, 
        (CASE WHEN EXISTS(
                SELECT id FROM alumnos WHERE t.id_alumno = a.id
            ) THEN a.nombre_apellido ELSE ah.nombre_apellido END
        ) AS alumno, 
        t.hora_ingreso, 
        t.hora_egreso, 
        (CASE WHEN EXISTS(
                SELECT ID FROM profesores WHERE t.profesor_ingreso = p_ing.id
            ) THEN p_ing.nombre_apellido ELSE ph_ing.nombre_apellido END
        ) AS profesor_ingreso, 
        (CASE WHEN EXISTS(
                SELECT ID FROM profesores WHERE T.profesor_egreso = p_egr.id
            ) THEN p_egr.nombre_apellido ELSE ph_egr.nombre_apellido END
        ) AS profesor_egreso
        FROM TURNO_PANOL t
        LEFT JOIN alumnos a
        ON t.id_alumno = a.id
        LEFT JOIN alumnos_HISTORICOS ah
        ON t.id_alumno = ah.id
        LEFT JOIN profesores p_ing
        ON t.profesor_ingreso = p_ing.id
        LEFT JOIN profesores_HISTORICOS ph_ing
        ON t.profesor_ingreso = ph_ing.id
        LEFT JOIN profesores p_egr
        ON t.profesor_egreso = p_egr.id
        LEFT JOIN profesores_HISTORICOS ph_egr
        ON t.profesor_egreso = ph_egr.id
        WHERE t.id LIKE ? 
        OR t.fecha LIKE ? 
        OR alumno LIKE ?
        OR t.hora_ingreso LIKE ? 
        OR t.hora_egreso LIKE ? 
        OR profesor_ingreso LIKE ? 
        OR profesor_egreso LIKE ?
        {orden}""", (
                f"{self.barraBusqueda.text()}", f"{self.barraBusqueda.text()}",
                f"{self.barraBusqueda.text()}", f"{self.barraBusqueda.text()}",
                f"{self.barraBusqueda.text()}", f"{self.barraBusqueda.text()}",
                f"{self.barraBusqueda.text()}",
            ))
        consulta = db.cur.fetchall()
        self.tabla.setRowCount(len(consulta))
        for i in range(len(consulta)):
            for j in range(len(consulta[i])):
                self.tabla.setItem(
                    i, j, qtw.QTableWidgetItem(str(consulta[i][j])))
            self.tabla.setRowHeight(i, 35)

            botonEditar = BotonEditar()
            botonEditar.clicked.connect(lambda: self.modificarLinea("editar"))
            self.tabla.setCellWidget(i, 7, botonEditar)

            botonEliminar = BotonEliminar()
            self.tabla.setCellWidget(i, 8, botonEliminar)

    def ordenar(self):
        """Este método cambia el ícono del botonOrdenar y actualiza los
        datos de la tabla de la pantalla."""
        self.botonOrdenar.cambiarIcono()
        self.mostrarDatos()

    def modificarLinea(self, tipo: str):
        """Este método crea un formulario para insertar o editar datos
        en la tabla turno_panol.

        El formulario es un QWidget que funciona como ventana. Por cada
        campo de la fila, agrega un entry y un label descriptivo. Al 
        confirmar los datos, ejecuta el método confirmarModificacion.

        Parámetros
        ----------
            tipo : str
                el tipo de formulario.

        Ver también
        -----------
        confirmarModificacion: modifica los datos de la tabla
        turno_panol.
        """
        self.ventanaEditar = qtw.QWidget()
        self.ventanaEditar.setWindowTitle("Agregar Turno")
        self.ventanaEditar.setWindowIcon(
            qtg.QIcon(
                f"{os.path.abspath(os.getcwd())}/duraam/images/logo.png"
            )
        )

        layoutVentanaModificar = qtw.QGridLayout()
        for i in range(1, len(self.campos)-2):
            label = qtw.QLabel(f"{self.campos[i]}: ")
            label.setObjectName("modificar-label")
            layoutVentanaModificar.addWidget(
                label, i-1, 0, alignment=qtc.Qt.AlignmentFlag.AlignRight
            )

        # objeto QDateEdit: un entry solo de fecha.
        self.entry1 = qtw.QDateEdit()
        self.entry2 = qtw.QLineEdit()

        db.cur.execute("SELECT nombre_apellido FROM alumnos")
        sugerenciasAlumnos = []
        for i in db.cur.fetchall():
            sugerenciasAlumnos.append(i[0])
        cuadroSugerenciasAlumnos = qtw.QCompleter(sugerenciasAlumnos, self)
        cuadroSugerenciasAlumnos.setCaseSensitivity(
            qtc.Qt.CaseSensitivity.CaseInsensitive
        )
        self.entry2.setCompleter(cuadroSugerenciasAlumnos)

        # objeto QTimeEdit: un entry solo de hora.
        self.entry3 = qtw.QTimeEdit()
        self.entry4 = qtw.QTimeEdit()
        self.entry5 = qtw.QLineEdit()
        self.entry6 = qtw.QLineEdit()

        db.cur.execute("SELECT nombre_apellido FROM profesores")
        sugerenciasProfesores = []
        for i in db.cur.fetchall():
            sugerenciasProfesores.append(i[0])
        cuadroSugerenciasProfesores = qtw.QCompleter(
            sugerenciasProfesores, self)
        cuadroSugerenciasProfesores.setCaseSensitivity(
            qtc.Qt.CaseSensitivity.CaseInsensitive
        )
        self.entry5.setCompleter(cuadroSugerenciasProfesores)
        self.entry6.setCompleter(cuadroSugerenciasProfesores)
        datos = []

        if tipo == "editar":
            botonClickeado = qtw.QApplication.focusWidget()
            posicion = self.tabla.indexAt(botonClickeado.pos())
            for cell in range(0, len(self.campos)):
                datos.append(posicion.sibling(posicion.row(), cell).data())
            self.entry1.setDate(qtc.QDate.fromString(datos[1], "dd/MM/yyyy"))
            self.entry2.setText(datos[2])
            self.entry3.setTime(qtc.QTime.fromString(datos[3], "hh:mm"))
            self.entry4.setTime(qtc.QTime.fromString(datos[4], "hh:mm"))
            self.entry5.setText(datos[5])
            self.entry6.setText(datos[6])

            self.ventanaEditar.setWindowTitle("Editar")

        layoutVentanaModificar.addWidget(self.entry1, 0, 1)
        self.entry1.setObjectName("modificar-entry")

        layoutVentanaModificar.addWidget(self.entry2, 1, 1)
        self.entry2.setObjectName("modificar-entry")

        layoutVentanaModificar.addWidget(self.entry3, 2, 1)
        layoutVentanaModificar.addWidget(self.entry4, 3, 1)

        self.entry3.setObjectName("modificar-entry")
        self.entry4.setObjectName("modificar-entry")

        layoutVentanaModificar.addWidget(self.entry5, 4, 1)
        self.entry5.setObjectName("modificar-entry")
        layoutVentanaModificar.addWidget(self.entry6, 5, 1)
        self.entry6.setObjectName("modificar-entry")

        botonConfirmar = qtw.QPushButton("Confirmar")
        botonConfirmar.setObjectName("confirmar")
        botonConfirmar.setWindowIcon(
            qtg.QIcon(f"{os.path.abspath(os.getcwd())}/duraam/images/logo.png"))
        botonConfirmar.clicked.connect(
            lambda: self.confirmarModificacion(datos))
        layoutVentanaModificar.addWidget(
            botonConfirmar, 6, 0, 1, 2, alignment=qtc.Qt.AlignmentFlag.AlignCenter)

        self.ventanaEditar.setLayout(layoutVentanaModificar)
        self.ventanaEditar.show()

    def confirmarModificacion(self, tipo: str, datosPorDefecto: list | None = None):
        """Este método modifica los datos de la tabla turno_panol.

        Verifica que el alumno y los profesores que autorizaron el
        ingreso y el egreso sean correctos y luego intenta realizar los
        cambios, registrarlos en el historial, notificar al usuario el
        éxito de la operacion, actualizar la tabla de la pantalla y
        cerrar el formulario. Si la base de datos arroja un
        sqlite3.IntegrityError durante el intento, le notifica al
        usuario que se ha repetido un valor único y termina la
        ejecución de la función, sin modificar la tabla.

        Parámetros
        ----------
            tipo : str
                El tipo de modificación.
            datosPorDefecto : list, default = None
                Los datos de la fila previos a la modificación. 

        Ver también
        -----------
        modificarLinea: crea un formulario para insertar o editar datos
                        en la tabla turno_panol.
        """
        db.cur.execute("""
        SELECT ID
        FROM alumnos
        WHERE nombre_apellido = ?
        LIMIT 1
        """, (self.entry2.text().upper(),))

        alumno = db.cur.fetchall()

        if not alumno:
            return m.mostrarMensaje("Error", "Error",
                                    "El alumno no está ingresado. Por favor, verifique que el alumno ingresado exista.")

        db.cur.execute("""
        SELECT ID
        FROM profesores
        WHERE nombre_apellido = ?
        LIMIT 1
        """, (self.entry5.text().upper(),))

        profeIngreso = db.cur.fetchall()

        if not profeIngreso:
            return m.mostrarMensaje("Error", "Error",
                                    "El profesor que autorizó el ingreso no está ingresado. Por favor, verifique que el profesor ingresado exista.")

        db.cur.execute("""
        SELECT ID
        FROM profesores
        WHERE nombre_apellido = ?
        LIMIT 1
        """, (self.entry6.text().upper(),))

        profeEgreso = db.cur.fetchall()

        if not profeEgreso:
            return m.mostrarMensaje("Error", "Error",
                                    "El profesor que autorizó el egreso no está ingresado. Por favor, verifique que el profesor ingresado exista.")

        fecha = self.entry1.date().toString("dd/MM/yyyy")
        ingreso = self.entry3.time().toString("hh:mm")
        egreso = self.entry4.time().toString("hh:mm")

        datosNuevos = (fecha, alumno[0][0], ingreso,
                       egreso, profeIngreso[0][0], profeEgreso[0][0])
        if tipo == "editar":
            db.cur.execute(
                "SELECT * FROM TURNO_PANOL WHERE ID = ?", (datosPorDefecto[0],))
            datosViejos = db.cur.fetchall()[0]
            db.cur.execute("""
            UPDATE TURNO_PANOL
            SET FECHA = ?,
            ID_alumno = ?,
            HORA_INGRESO = ?,
            HORA_EGRESO = ?,
            profesor_ingreso = ?,
            profesor_egreso = ?
            WHERE ID = ?
            """, (
                datosNuevos[0], datosNuevos[1], datosNuevos[2], datosNuevos[3], datosNuevos[4],
                datosNuevos[5], datosPorDefecto[0],
            ))

            registrarCambios(
                "Edicion", "Turnos del pañol", datosPorDefecto[0], f"{datosViejos}", f"{datosNuevos}"
            )
            db.con.commit()
            m.mostrarMensaje("Information", "Aviso",
                             "Se ha actualizado el movimiento.")
        else:
            db.cur.execute(
                "INSERT INTO TURNO_PANOL VALUES(NULL, ?, ?, ?, ?, ?, ?)", (
                    fecha, alumno[0][0], ingreso, egreso, profeIngreso[0][0], profeEgreso[0][0],
                ))
            registrarCambios("Insercion", "Subgrupos",
                             datosNuevos[0], None, f"{datosNuevos}")
            db.con.commit()
            m.mostrarMensaje("Information", "Aviso",
                             "Se ha ingresado un turno.")

        self.mostrarDatos()
        self.ventanaEditar.close()

    def eliminar(self):
        """Este método elimina la fila de la tabla turno_panol.

        Antes de eliminar, confirma la decisión del usuario. Al
        finalizar, registra los cambios y actualiza la tabla.
        """
        respuesta = m.mostrarMensaje("Pregunta", "Advertencia",
                                     "¿Está seguro que desea eliminar estos datos?")
        db.cur.execute(
            "SELECT * FROM MOVIMIENTOS_HERRAMIENTAS WHERE ID_TURNO_PANOL = ?", (idd,))
        tipo = "Eliminacion simple"
        tablas = "Alumnos"
        if db.cur.fetchall():
            tipo = "Eliminacion compleja"
            tablas = "Alumnos Movimientos de herramientas"
            respuesta = m.mostrarMensaje("Pregunta", "Advertencia",
                                         """
                Todavía hay movimientos registrados con este turno. 
                Eliminar el turno eliminará también TODOS los movimientos relacionados.
                ¿Desea eliminarlo de todas formas?
                """)
        if respuesta == qtw.QMessageBox.StandardButton.Yes:
            botonClickeado = qtw.QApplication.focusWidget()
            posicion = self.tabla.indexAt(botonClickeado.pos())
            idd = posicion.sibling(posicion.row(), 0).data()
            db.cur.execute("SELECT * FROM TURNO_PANOL WHERE ID = ?", (idd,))
            datosEliminados = db.cur.fetchall()[0]
            db.cur.execute("DELETE FROM TURNO_PANOL WHERE ID = ?", (idd,))
            db.cur.execute(
                "DELETE FROM MOVIMIENTOS_HERRAMIENTAS WHERE ID_TURNO_PANOL = ?", (idd,))
            registrarCambios(tipo, tablas, idd, f"{datosEliminados}", None)
            db.con.commit()
            self.mostrarDatos()
