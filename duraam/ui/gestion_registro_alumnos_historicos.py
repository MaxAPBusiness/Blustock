"""Este módulo crea una pantalla para gestionar la tabla
alumnos_historicos.

Clases
------
    GestionRegistroAlumnosHistoricos(qtw.QWidget):
        Crea una pantalla para gestionar la tabla alumnos_historicos.
"""
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import os
import datetime as dt

import db.inicializar_bbdd as db
from .botones import BotonOrdenar, BotonFila
from . import mostrar_mensaje as m
from registrar_cambios import registrarCambios


class GestionRegistroAlumnosHistoricos(qtw.QWidget):
    """Esta clase crea una pantalla para gestionar la tabla
    alumnos_historicos.

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
        radioFecha : QRadioButton
            El botón de radio para ordenar los datos de la tabla por
            fecha de salida.
        botonOrdenar : QPushButton
            Un botón para ordenar los datos de manera ascendente o
            descendente.

    Métodos
    -------
        __init__(self):
            El constructor de la clase
            GestionRegistroAlumnosHistoricos.

            Crea la pantalla, un QWidget, que contiene: un título
            descriptivo, un QLabel; una tabla, un QTableWidget, que
            muestra los datos de la tabla alumnos_historicos y contiene
            botones para editarlos; una barra de buscador, un
            QLineEdit, para buscar los datos; botones de radio,
            QRadioWidget, para ordenar los datos mostrados en base a
            una columna seleccionada, un botón, un QCheckBox, para
            ordenar los datos de manera ascendente o descendente según
            el boton presionado; dos botones, QPushButton, para
            insertar datos a la tabla.

        mostrarDatos(self):
            Obtiene los datos de la tabla alumnos_historicos y los
            introduce en la tabla de la pantalla.

        ordenar(self):
            Llama a la función cambiarIcono y al método mostrarDatos.

        eliminar(self):
            Elimina la fila de la tabla alumnos_historicos.

        paseHistoricoIndividual(self):
            crea un formulario para pasar alumnos al registro histórico
            de forma individual.

        cargarDNI(self, nombre):
            Crea un cuadro de sugerencias para el campo DNI
            del formulario de pase histórico individual.

        confirmarIndividual(self):
            Pasa a un alumno al registro histórico.

        paseHistoricoGrupal(self):
            Crea una ventana para pasar alumnos al registro
            histórico de forma grupal.

        mostrarDatosPase(self):
            Obtiene los datos de los alumnos de los cursos
            7A y 7B y los introduce en la tabla de la ventana del pase 
            histórico grupal de alumnos.

        confirmarGrupal(self):
            Pasa al grupo de alumnos seleccionados al
            registro histórico.
    """

    def __init__(self):
        super().__init__()

        self.titulo = qtw.QLabel("GESTIÓN DEL REGISTRO DE ALUMNOS HISTÓRICOS")
        self.titulo.setObjectName("titulo")

        self.subtitulo = qtw.QLabel("Pase alumnos existentes a históricos.")
        self.subtitulo.setObjectName("subtitulo")

        self.tabla = qtw.QTableWidget(self)
        self.tabla.setObjectName("tabla")
        self.campos = ("ID", "DNI", "Nombre y Apellido", "Curso",
                       "Fecha de Salida", "email", "")
        self.tabla.setColumnCount(len(self.campos))
        self.tabla.setHorizontalHeaderLabels(self.campos)
        self.tabla.verticalHeader().hide()
        self.tabla.setColumnWidth(2, 120)
        self.tabla.setColumnWidth(3, 200)
        self.tabla.setColumnWidth(5, 35)
        self.tabla.setColumnWidth(6, 35)

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
        self.radioFecha = qtw.QRadioButton("Fecha de salida")
        self.radioNombre.setObjectName("Radio1")
        self.radioDNI.setObjectName("Radio2")
        self.radioFecha.setObjectName("Radio3")
        self.radioNombre.toggled.connect(lambda: self.mostrarDatos())
        self.radioDNI.toggled.connect(lambda: self.mostrarDatos())
        self.radioFecha.toggled.connect(lambda: self.mostrarDatos())

        self.botonOrdenar = BotonOrdenar()
        self.botonOrdenar.stateChanged.connect(lambda: self.ordenar())

        botonPaseIndividual = qtw.QPushButton("Pase Individual")
        botonPaseIndividual.setObjectName("confirmar")
        botonPaseIndividual.clicked.connect(
            lambda: self.paseHistoricoIndividual())
        botonPaseIndividual.setCursor(qtg.QCursor(
            qtc.Qt.CursorShape.PointingHandCursor))

        botonPaseGrupal = qtw.QPushButton("Pase de Egresados")
        botonPaseGrupal.setObjectName("confirmar")
        botonPaseGrupal.clicked.connect(
            lambda: self.paseHistoricoGrupal())
        botonPaseGrupal.setCursor(
            qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor)
        )

        layout = qtw.QVBoxLayout()
        layout.addWidget(self.titulo)
        contenedor1 = qtw.QWidget()
        contenedor1Layout = qtw.QGridLayout()
        contenedor1Layout.addWidget(self.barraBusqueda, 0, 0)
        contenedor1Layout.addWidget(contenedorIconoLupa, 0, 0)
        contenedor1Layout.addWidget(labelOrdenar, 0, 1)
        contenedor1Layout.addWidget(self.radioNombre, 0, 2)
        contenedor1Layout.addWidget(self.radioDNI, 0, 3)
        contenedor1Layout.addWidget(self.botonOrdenar, 0, 4)
        contenedor1.setLayout(contenedor1Layout)
        layout.addWidget(contenedor1)
        layout.addWidget(self.tabla)
        contenedor2 = qtw.QWidget()
        contenedor2Layout = qtw.QHBoxLayout()
        contenedor2Layout.addWidget(botonPaseIndividual)
        contenedor2Layout.addWidget(botonPaseGrupal)
        contenedor2.setLayout(contenedor2Layout)
        layout.addWidget(contenedor2)
        self.setLayout(layout)
        self.mostrarDatos()

    def mostrarDatos(self):
        """Este método obtiene los datos de la tabla alumnos_historicos
        y los introduce en la tabla de la pantalla.
        """
        if self.radioNombre.isChecked():
            orden = "ORDER BY nombre_apellido"
        elif self.radioDNI.isChecked():
            orden = "ORDER BY dni"
        elif self.radioFecha.isChecked():
            orden = "ORDER BY fecha_salida"
        else:
            orden = ""

        if orden and self.botonOrdenar.isChecked():
            orden += " DESC"
        elif self.botonOrdenar.isChecked():
            orden="ORDER BY nombre_apellido DESC"

        db.cur.execute(
            f"""
            SELECT * FROM alumnos_historicos 
            WHERE ID LIKE ? 
            OR DNI LIKE ? 
            OR nombre_apellido LIKE ?
            OR curso LIKE ?
            OR fecha_salida LIKE ? 
            OR email LIKE ?
            {orden}
            """, (
                f"%{self.barraBusqueda.text()}%", f"%{self.barraBusqueda.text()}%",
                f"%{self.barraBusqueda.text()}%", f"%{self.barraBusqueda.text()}%",
                f"%{self.barraBusqueda.text()}%", f"%{self.barraBusqueda.text()}%",
            )
        )
        consulta = db.cur.fetchall()
        self.tabla.setRowCount(len(consulta))
        for i in range(len(consulta)):
            for j in range(len(consulta[i])):
                self.tabla.setItem(
                    i, j, qtw.QTableWidgetItem(str(consulta[i][j])))
            self.tabla.setRowHeight(i, 35)

            botonEliminar = BotonFila("eliminar")
            botonEliminar.clicked.connect(lambda: self.eliminar())
            self.tabla.setCellWidget(i, len(self.campos)-1, botonEliminar)

    def ordenar(self):
        """Este método cambia el ícono del botonOrdenar y actualiza los
        datos de la tabla de la pantalla."""
        self.botonOrdenar.cambiarIcono()
        self.mostrarDatos()

    def eliminar(self):
        """Este método elimina la fila de la tabla alumnos_historicos.

        Antes de eliminar, confirma la decisión del usuario.
        Si los datos están relacionados con otras tablas, vuelve a
        confirmar la decisión del usuario. Luego, elimina la fila de la
        tabla alumnos y las filas en donde los datos estaban
        relacionados. Por último, registra los cambios y actualiza la
        tabla.
        """
        respuesta = m.mostrarMensaje("Pregunta", "Advertencia",
                                     "¿Está seguro que desea eliminar estos datos?")
        if respuesta == qtw.QMessageBox.StandardButton.Yes:
            botonClickeado = qtw.QApplication.focusWidget()
            posicion = self.tabla.indexAt(botonClickeado.pos())
            idd = posicion.sibling(posicion.row(), 0).data()

            tipo = "Eliminacion simple"
            tablas = "Alumnos históricos"

            db.cur.execute(
                "SELECT * FROM movimientos_herramientas WHERE CLASE=0 AND ID_PERSONA = ?", (idd,))
            if db.cur.fetchall():
                tipo = "Eliminacion compleja"
                tablas = "Alumnos históricos Movimientos de herramientas"
                respuesta = m.mostrarMensaje("Pregunta", "Advertencia", """
                El alumno tiene movimientos registrados. 
                Eliminarlo eliminará tambien TODOS los movimientos en los que está registrado,
                por lo que sus registros de deudas se eliminarán y podría perderse información valiosa.

                ¿Desea eliminarlo de todas formas?
                """)
        if respuesta == qtw.QMessageBox.StandardButton.Yes:
            db.cur.execute(
                "SELECT * FROM alumnos_historicos WHERE ID = ?", (idd,))
            datosEliminados = db.cur.fetchall()[0]
            db.cur.execute(
                "DELETE FROM alumnos_historicos WHERE ID = ?", (idd,))
            db.cur.execute(
                "DELETE FROM movimientos_herramientas WHERE CLASE=0 AND ID_PERSONA = ?", (idd,))
            db.cur.execute(
                "UPDATE turno_panol SET ID_ALUMNO=NULL WHERE ID_ALUMNO = ?", (idd,))
            registrarCambios(tipo, tablas, idd, f"{datosEliminados}", None,)
            db.con.commit()
            self.mostrarDatos()

    def paseHistoricoIndividual(self):
        """Este método crea un formulario para pasar alumnos al
        registro histórico de forma individual."""
        self.menuPase = qtw.QWidget()
        self.menuPase.setWindowTitle(
            "Realizar Pase Histórico Individual de Alumnos")
        self.menuPase.setWindowIcon(
            qtg.QIcon(f"{os.path.abspath(os.getcwd())}/duraam/images/logo.png"))

        titulo = qtw.QLabel(
            "Ingresa al alumno que quieres pasar al registro histórico")
        titulo.setObjectName("subtitulo")

        label1 = qtw.QLabel("Nombre del Alumno: ")
        label2 = qtw.QLabel("DNI: ")
        self.entry1 = qtw.QLineEdit()
        self.entry2 = qtw.QLineEdit()
        self.entry1.setObjectName("modificar-entry")
        self.entry2.setObjectName("modificar-entry")

        # El código de abajo añade un cuadro de sugerencias al campo de
        # nombre del alumno. Busca todos los nombres cargados y los
        # introduce en el campo.
        sugerenciasNombre = []
        db.cur.execute("SELECT nombre_apellido FROM alumnos")
        for i in db.cur.fetchall():
            sugerenciasNombre.append(i[0])
        cuadroSugerenciasNombre = qtw.QCompleter(sugerenciasNombre, self)
        cuadroSugerenciasNombre.setCaseSensitivity(
            qtc.Qt.CaseSensitivity.CaseInsensitive)
        self.entry1.setCompleter(cuadroSugerenciasNombre)
        self.entry1.editingFinished.connect(
            lambda: self.cargarDNI(self.entry1.text()))

        botonConfirmar = qtw.QPushButton("Confirmar")
        botonConfirmar.setObjectName("confirmar")
        botonConfirmar.setWindowIcon(
            qtg.QIcon(f"{os.path.abspath(os.getcwd())}/duraam/images/logo.png"))
        botonConfirmar.clicked.connect(lambda: self.confirmarIndividual())

        layoutMenuPase = qtw.QGridLayout()
        layoutMenuPase.addWidget(
            titulo, 0, 0, 1, 2, alignment=qtc.Qt.AlignmentFlag.AlignCenter)
        layoutMenuPase.addWidget(
            label1, 1, 0, alignment=qtc.Qt.AlignmentFlag.AlignRight)
        layoutMenuPase.addWidget(
            label2, 2, 0, alignment=qtc.Qt.AlignmentFlag.AlignRight)
        layoutMenuPase.addWidget(self.entry1, 1, 1)
        layoutMenuPase.addWidget(self.entry2, 2, 1)
        layoutMenuPase.addWidget(
            botonConfirmar, 3, 0, 1, 2, alignment=qtc.Qt.AlignmentFlag.AlignCenter)
        self.menuPase.setLayout(layoutMenuPase)
        self.menuPase.show()

    def cargarDNI(self, nombre: str):
        """Este método crea un cuadro de sugerencias para el campo DNI
        del formulario de pase histórico individual.

        Busca los dni relacionados con el nombre de alumno ingresado.

        Parámetros
        ----------
            nombre: str
                El nombre del alumno ingresado en el formulario.

        Ver también
        -----------
        paseHistoricoIndividual: crea un formulario para pasar alumnos
                                 al registro histórico de forma
                                 individual.
        """
        sugerenciasDNI = []
        db.cur.execute(
            "SELECT DNI FROM alumnos WHERE nombre_apellido = ?", (nombre,))
        for i in db.cur.fetchall():
            sugerenciasDNI.append(str(i[0]))
        cuadroSugerenciasDNI = qtw.QCompleter(sugerenciasDNI, self)
        cuadroSugerenciasDNI.setCaseSensitivity(
            qtc.Qt.CaseSensitivity.CaseInsensitive)
        self.entry2.setCompleter(cuadroSugerenciasDNI)

    def confirmarIndividual(self):
        """Este método pasa a un alumno al registro histórico.

        Comprueba que el dni coincida con el nombre del alumno y luego
        realiza el pase, eliminandolo de la tabla alumnos, agregándolo
        a la tabla alumnos_historicos Y registrando los cambios en el
        historial. Luego, notifica al usuario el éxito del pase y
        cierra el formulario.

        Ver también
        -----------
        paseHistoricoIndividual: crea un formulario para pasar alumnos
        al registro histórico de forma individual.
        """
        respuesta = m.mostrarMensaje("Pregunta", "Atención",
                                     "¿Está seguro que desea pasar a este alumno al registro histórico? Esto no se puede deshacer")
        if respuesta:
            db.cur.execute("SELECT * FROM alumnos WHERE DNI = ?",
                           (self.entry2.text(),))
            datos = db.cur.fetchall()
            if not datos:
                return m.mostrarMensaje("Error", "Error", "El DNI no coincide con el alumno. Por favor, intente nuevamente.")

            db.cur.execute("INSERT INTO alumnos_historicos VALUES(?, ?, ?, ?, ?, ?) ", (
                datos[0][0], datos[0][1], datos[0][2], datos[0][3],
                dt.date.today().strftime("%Y/%m/%d"), datos[0][4]
            ))
            db.cur.execute("DELETE FROM alumnos WHERE ID = ?", (datos[0][0],))
            registrarCambios("Pase historico individual",
                             "Alumnos historicos", datos[0][0], f"{datos[0]}", None,)
            db.con.commit()
            m.mostrarMensaje("Information", "Aviso",
                             "Se ha pasado un alumno al registro histórico.")
            self.mostrarDatos()
            self.menuPase.close()

    def paseHistoricoGrupal(self):
        """Este método crea una ventana para pasar alumnos al registro
        histórico de forma grupal.

        La ventana es un QWidget, que contiene:
            \n- Una tabla, un QTableWidget, que muestra los datos de
              la tabla alumnos_historicos.
            \n- Una barra de buscador, un QLineEdit, para buscar los
              datos.
            \n- Un botón para realizar el pase. 
        """
        self.menuPase = qtw.QWidget()
        self.menuPase.setWindowTitle(
            "Realizar Pase Histórico Grupal de Alumnos")
        self.menuPase.setWindowIcon(
            qtg.QIcon(f"{os.path.abspath(os.getcwd())}/duraam/images/logo.png"))

        titulo = qtw.QLabel(
            "Seleccione los alumnos que desea egresar y dejar registrados históricamente.")
        titulo.setObjectName("subtitulo")

        self.barraBusquedaPase = qtw.QLineEdit()
        self.barraBusquedaPase.setObjectName("buscar")
        self.barraBusquedaPase.setClearButtonEnabled(True)
        self.barraBusquedaPase.setPlaceholderText("Buscar...")
        iconoLupa = qtg.QPixmap(
            f"{os.path.abspath(os.getcwd())}/duraam/images/buscar.png")
        contenedorIconoLupa = qtw.QLabel()
        contenedorIconoLupa.setObjectName("lupa")
        contenedorIconoLupa.setPixmap(iconoLupa)

        self.barraBusquedaPase.textEdited.connect(
            lambda: self.mostrarDatosPase())

        self.tablaListaAlumnos = qtw.QTableWidget()
        self.tablaListaAlumnos.setMaximumSize(400, 345)

        self.camposPase = ("", "Nombre y Apellido", "DNI", "Curso")

        self.tablaListaAlumnos.setColumnCount(len(self.camposPase))
        self.tablaListaAlumnos.setColumnWidth(0, 15)
        self.tablaListaAlumnos.setColumnWidth(1, 125)
        self.tablaListaAlumnos.setHorizontalHeaderLabels(self.camposPase)
        self.tablaListaAlumnos.verticalHeader().hide()
        self.mostrarDatosPase()

        botonConfirmar = qtw.QPushButton("Confirmar")
        botonConfirmar.setObjectName("confirmar")
        botonConfirmar.setWindowIcon(
            qtg.QIcon(f"{os.path.abspath(os.getcwd())}/duraam/images/logo.png"))
        botonConfirmar.clicked.connect(lambda: self.confirmarGrupal())
        botonConfirmar.setCursor(qtg.QCursor(
            qtc.Qt.CursorShape.PointingHandCursor))

        layoutMenuPase = qtw.QGridLayout()
        layoutMenuPase.addWidget(
            titulo, 0, 0, alignment=qtc.Qt.AlignmentFlag.AlignCenter)
        layoutMenuPase.addWidget(self.barraBusquedaPase, 1, 0)
        layoutMenuPase.addWidget(contenedorIconoLupa, 1, 0)
        layoutMenuPase.addWidget(self.tablaListaAlumnos, 2, 0, 1, 4)
        layoutMenuPase.addWidget(botonConfirmar, 3, 0)
        layoutMenuPase.addWidget(botonConfirmar, 3, 0,
                                 alignment=qtc.Qt.AlignmentFlag.AlignCenter)

        self.menuPase.setLayout(layoutMenuPase)
        self.menuPase.show()

    def mostrarDatosPase(self):
        """Este método obtiene los datos de los alumnos de los cursos
        7A y 7B y los introduce en la tabla de la ventana del pase 
        hsitórico grupal de alumnos.

        Ver también
        -----------
        paseHistoricoGrupal: crea una ventana para pasar alumnos al
        registro histórico de forma grupal.
        """
        db.cur.execute("""
        SELECT nombre_apellido, DNI, curso
        FROM alumnos
        WHERE curso IN (?, ?)
        AND nombre_apellido LIKE ?
        OR DNI LIKE ?
        OR curso LIKE ?
        ORDER BY curso, ID
        """, (
            "7A", "7B", f"%{self.barraBusquedaPase.text()}%",
            f"%{self.barraBusquedaPase.text()}%", f"%{self.barraBusquedaPase.text()}%"
        )
        )
        consulta = db.cur.fetchall()
        self.tablaListaAlumnos.setRowCount(len(consulta))
        # Por cada fila, añade un boton de tick al inicio para
        # seleccionarla.
        for i in range(len(consulta)):
            check = qtw.QCheckBox()
            check.setObjectName("check")
            check.toggle()
            self.tablaListaAlumnos.setCellWidget(i, 0, check)
            for j in range(len(consulta[i])):
                self.tablaListaAlumnos.setItem(
                    i, j+1, qtw.QTableWidgetItem(str(consulta[i][j])))
            self.tablaListaAlumnos.setRowHeight(i, 35)

    def confirmarGrupal(self):
        """Este método pasa al grupo de alumnos seleccionados al
        registro histórico.

        Ver también
        -----------
        paseHistoricoGrupal: crea un formulario para pasar alumnos
        al registro histórico de forma grupal.
        """
        for i in range(self.tablaListaAlumnos.rowCount()):
            datosGrupales = []
            # Comprueba que el botón este checkeado para pasar al
            # alumno al registro histórico.
            if self.tablaListaAlumnos.cellWidget(i, 0).isChecked():
                db.cur.execute("SELECT * FROM alumnos WHERE DNI = ?",
                               (int(self.tablaListaAlumnos.item(i, 2).text()),))
                datos = db.cur.fetchall()
                db.cur.execute("INSERT INTO alumnos_historicos VALUES(?, ?, ?, ?, ?, ?)", (
                    datos[0][0], datos[0][1], datos[0][2], datos[0][3],
                    dt.date.today().strftime("%Y/%m/%d"), datos[0][4]
                ))
                datosGrupales.append(datos[0][0])
                db.cur.execute(
                    "DELETE FROM alumnos WHERE ID = ?", (datos[0][0],))
        registrarCambios(
            "Pase historico grupal", "Alumnos historicos", datos[
                0][0], f"{datosGrupales}", None
        )
        self.mostrarDatos()
        m.mostrarMensaje("Information", "Aviso", "Se han pasado los egresados seleccionados al registro histórico.")
        self.menuPase.close()
        db.con.commit()
