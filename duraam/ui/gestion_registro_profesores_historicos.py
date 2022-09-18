"""Este módulo crea una pantalla para gestionar la tabla
profesores_historicos.

Clases
------
    GestionRegistroProfesoresHistoricos(qtw.QWidget):
        Crea una pantalla para gestionar la tabla profesores.
"""
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import os
import datetime as dt

import db.inicializar_bbdd as db
from botones import BotonOrdenar, BotonEliminar
import mostrar_mensaje as m
from registrar_cambios import registrarCambios


class GestionRegistroProfesoresHistoricos(qtw.QWidget):
    """Esta clase crea una pantalla para gestionar la tabla
    profesores_historicos.

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
            GestionRegistroProfesoresHistoricos.

            Crea la pantalla, un QWidget, que contiene: un título
            descriptivo, un QLabel; una tabla, un QTableWidget, que
            muestra los datos de la tabla profesores_historicos y
            contiene botones para editarlos; una barra de buscador, un
            QLineEdit, para buscar los datos; botones de radio,
            QRadioWidget, para ordenar los datos mostrados en base a
            la columna seleccionada; un botón, un QCheckBox, para
            ordenar los datos de manera ascendente o descendente; dos
            botones, QPushButton, para insertar datos a la tabla.

        mostrarDatos(self):
            Obtiene los datos de la tabla profesores_historicos y los
            introduce en la tabla de la pantalla.

        ordenar(self):
            Llama a la función cambiarIcono y al método mostrarDatos.

        eliminar(self):
            Elimina la fila de la tabla profesores_historicos.

        paseHistorico(self):
            Crea un formulario para pasar profesores al registro
            histórico.

        cargarDNI(self, nombre):
            Crea un cuadro de sugerencias para el campo DNI del
            formulario de pase individual.

        confirmarPase(self):
            Pasa al profesor al registro histórico.
    """

    def __init__(self):
        super().__init__()

        self.titulo = qtw.QLabel(
            "GESTIÓN DEL REGISTRO DE PROFESORES HISTÓRICOS")
        self.titulo.setObjectName("titulo")

        self.subtitulo = qtw.QLabel("Pase profesores existentes a históricos.")
        self.subtitulo.setObjectName("subtitulo")

        self.tabla = qtw.QTableWidget(self)
        self.tabla.setObjectName("tabla")
        self.campos = ("ID", "DNI", "Nombre y Apellido", "Curso",
                       "Fecha de Salida", "email")
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
        botonPase = qtw.QPushButton("Pase Individual")
        botonPase.setObjectName("confirmar")
        botonPase.clicked.connect(
            lambda: self.paseHistorico())
        botonPase.setCursor(qtg.QCursor(
            qtc.Qt.CursorShape.PointingHandCursor))

        layout = qtw.QGridLayout()
        layout.addWidget(self.titulo)
        contenedor1 = qtw.QWidget()
        contenedor1Layout = qtw.QGridLayout()
        contenedor1Layout.addWidget(self.barraBusqueda, 0, 0)
        contenedor1Layout.addWidget(contenedorIconoLupa, 0, 0)
        contenedor1Layout.addWidget(labelOrdenar, 0, 1)
        contenedor1Layout.addWidget(self.radioNombre, 0, 2)
        contenedor1Layout.addWidget(self.radioDNI, 0, 3)
        contenedor1Layout.addWidget(self.radioFecha, 0, 4)
        contenedor1Layout.addWidget(self.botonOrdenar, 0, 5)
        contenedor1.setLayout(contenedor1Layout)
        layout.addWidget(contenedor1)
        layout.addWidget(self.tabla)
        layout.addWidget(botonPase)
        self.setLayout(layout)
        self.mostrarDatos()

    def mostrarDatos(self):
        """Este método obtiene los datos de la tabla
        profesores_historicos y los introduce en la tabla de la
        pantalla.
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
            orden += " ASC"

        db.cur.execute(
            f"""
            SELECT * FROM profesores_historicos 
            WHERE ID LIKE ? 
            OR DNI LIKE ? 
            OR nombre_apellido LIKE ?
            OR fecha_salida LIKE ?
            OR email LIKE ?
            {orden}
            """, (
                f"{self.barraBusqueda.text()}", f"{self.barraBusqueda.text()}",
                f"{self.barraBusqueda.text()}", f"{self.barraBusqueda.text()}",
                f"{self.barraBusqueda.text()}",)
        )
        consulta = db.cur.fetchall()
        self.tabla.setRowCount(len(consulta))
        for i in range(len(consulta)):
            for j in range(len(consulta[i])):
                self.tabla.setItem(
                    i, j, qtw.QTableWidgetItem(str(consulta[i][j])))
            self.tabla.setRowHeight(i, 35)

            botonEliminar = BotonEliminar()
            botonEliminar.clicked.connect(lambda: self.eliminar())
            self.tabla.setCellWidget(i, 5, botonEliminar)

    def ordenar(self):
        """Este método cambia el ícono del botonOrdenar y actualiza los
        datos de la tabla de la pantalla."""
        self.botonOrdenar.cambiarIcono()
        self.mostrarDatos()

    def eliminar(self):
        """Este método elimina la fila de la tabla
        profesores_historicos.

        Antes de eliminar, confirma la decisión del usuario.
        Si los datos están relacionados con otras tablas, vuelve a
        confirmar la decisión del usuario. Luego, elimina la fila de la
        tabla profesors y las filas en donde los datos estaban
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
                "SELECT * FROM movimientos_herramientas WHERE profesor_ingreso = ? OR profesor_egreso = ?", (idd, idd))
            if db.cur.fetchall():
                tipo = "Eliminacion compleja"
                tablas = "Alumnos históricos Movimientos de herramientas"
                respuesta = m.mostrarMensaje("Pregunta", "Advertencia",
                                             """
                    El profesor tiene turnos y/o movimientos registrados. 
                    Eliminarlo eliminará toda la información relacionada, 
                    como sus turnos y sus movimientos.
                    ¿Está seguro que desea continuar y eliminar la información relacionada?
                    """
                                             )

        if respuesta == qtw.QMessageBox.StandardButton.Yes:
            db.cur.execute(
                "SELECT * FROM profesores_historicos WHERE id = ?", (idd,))
            datosEliminados = db.cur.fetchall()[0]
            db.cur.execute(
                "DELETE FROM profesores_historicos WHERE id = ?", (idd,))
            db.cur.execute(
                "DELETE FROM movimientos_herramientas WHERE ROL=1 AND ID_PERSONA = ?", (idd,))
            db.cur.execute(
                "UPDATE turno_panol SET profesor_ingreso=NULL WHERE profesor_ingreso = ?", (idd,))
            db.cur.execute(
                "UPDATE turno_panol SET profesor_egreso=NULL WHERE profesor_egreso = ?", (idd,))
            registrarCambios(tipo, tablas, idd, f"{datosEliminados}", None)
            db.con.commit()
            self.mostrarDatos()

    def paseHistorico(self):
        """Este método crea un formulario para pasar profesores al
        registro histórico."""
        self.menuPase = qtw.QWidget()
        self.menuPase.setWindowTitle(
            "Realizar Pase Histórico de Profesores")
        self.menuPase.setWindowIcon(
            qtg.QIcon(f"{os.path.abspath(os.getcwd())}/duraam/images/logo.png"))

        titulo = qtw.QLabel(
            "Ingresa al profesor que quieres pasar al registro histórico")
        titulo.setObjectName("subtitulo")
        label1 = qtw.QLabel("Nombre del Profesor: ")
        label2 = qtw.QLabel("DNI: ")

        self.entry1 = qtw.QLineEdit()
        self.entry2 = qtw.QLineEdit()

        sugerenciasNombre = []

        db.cur.execute("SELECT nombre_apellido FROM profesores")

        for i in db.cur.fetchall():
            sugerenciasNombre.append(i[0])

        cuadroSugerenciasNombre = qtw.QCompleter(sugerenciasNombre, self)
        cuadroSugerenciasNombre.setCaseSensitivity(
            qtc.Qt.CaseSensitivity.CaseInsensitive)
        self.entry1.setCompleter(cuadroSugerenciasNombre)
        self.entry1.editingFinished.connect(
            lambda: self.cargarDNI(self.entry1.text()))

        datos = []

        self.entry1.setObjectName("modificar-entry")
        self.entry2.setObjectName("modificar-entry")

        botonConfirmar = qtw.QPushButton("Confirmar")
        botonConfirmar.setObjectName("confirmar")
        botonConfirmar.setWindowIcon(
            qtg.QIcon(f"{os.path.abspath(os.getcwd())}/duraam/images/logo.png"))
        botonConfirmar.clicked.connect(
            lambda: self.confirmarPase(datos))

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
        del formulario de pase histórico.

        Busca los dni relacionados con el nombre del profesor
        ingresado.

        Parámetros
        ----------
            nombre: str
                El nombre del profesor ingresado en el formulario.

        Ver también
        -----------
        paseHistorico: crea un formulario para pasar profesores al
                       registro histórico.
        """
        db.cur.execute(
            "SELECT DNI FROM profesores WHERE nombre_apellido = ?", (nombre,))

        sugerenciasDNI = []

        for i in db.cur.fetchall():
            sugerenciasDNI.append(str(i[0]))

        cuadroSugerenciasDNI = qtw.QCompleter(sugerenciasDNI, self)
        cuadroSugerenciasDNI.setCaseSensitivity(
            qtc.Qt.CaseSensitivity.CaseInsensitive)
        self.entry2.setCompleter(cuadroSugerenciasDNI)

    def confirmarPase(self):
        """Este método pasa a un profesor al registro histórico.

        Comprueba que el dni coincida con el nombre del profesor y luego
        realiza el pase, eliminandolo de la tabla profesores, agregándolo
        a la tabla profesores_historicos Y registrando los cambios en el
        historial. Luego, notifica al usuario el éxito del pase y
        cierra el formulario.

        Ver también
        -----------
        paseHistorico: crea un formulario para pasar profesores
        al registro histórico de forma individual.
        """
        respuesta = m.mostrarMensaje("Pregunta", "Atención",
                                     "¿Está seguro que desea pasar a este profesor al registro histórico? Esto no se puede deshacer")
        if respuesta:
            db.cur.execute("SELECT * FROM profesores WHERE DNI = ?",
                           (self.entry2.text(),))
            datos = db.cur.fetchall()
            if not datos:
                return m.mostrarMensaje("Error", "Error", "El DNI no coincide con el profesor. Por favor, intente nuevamente.")
            db.cur.execute("INSERT INTO profesores_historicos VALUES(?, ?, ?, ?, ?) ", (
                datos[0][0], datos[0][1], datos[0][2], dt.date.today().strftime(
                    "%Y/%m/%d"),
                datos[0][3],))
            db.cur.execute(
                "DELETE FROM profesores WHERE id = ?", (datos[0][0], ))
            registrarCambios("Pase historico individual",
                             "Profesores historicos", datos[0][0], datos[0], None)
            db.con.commit()
            m.mostrarMensaje("Information", "Aviso",
                             "Se ha pasado un profesor al registro histórico.")
            self.mostrarDatos()
            self.menuPase.close()
