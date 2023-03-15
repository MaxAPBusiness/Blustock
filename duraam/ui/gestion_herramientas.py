"""Este módulo crea una pantalla para gestionar la tabla herramientas.

Clases
------
    GestionHerramientas(qtw.QWidget):
        Crea una pantalla para gestionar la tabla herramientas.
"""
import sqlite3
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import os

import db.inicializar_bbdd as db
from .botones import BotonOrdenar, BotonFila
from . import mostrar_mensaje as m
from registrar_cambios import registrarCambios


class GestionHerramientas(qtw.QWidget):
    """Esta clase crea una pantalla para gestionar la tabla
    herramientas.

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
        radioGrupo : QRadioButton
            El botón de radio para ordenar los datos de la tabla por
            grupo.
        radioSubgrupo : QRadioButton
            El botón de radio para ordenar los datos de la tabla por
            subgrupo.

    Métodos
    -------
        __init__(self):
            El constructor de la clase GestionHerramientas.

            Crea la pantalla, un QWidget, que contiene: un título
            descriptivo, un QLabel; una tabla, un QTableWidget, que
            muestra los datos de la tabla herramientas y contiene
            botones para editarlos; una barra de buscador, un
            QLineEdit, para buscar los datos; tres botones de radio,
            QRadioButton, para ordenar los datos en base a columnas
            específicas; un botón, QCheckBox, para ordenar los datos
            mostrados de manera ascendente o descendente según el boton
            presionado; un botón, un QPushButton, para insertar datos a
            la tabla.

        mostrarDatos(self):
            Obtiene los datos de la tabla herramientas y los introduce en 
            la tabla de la pantalla.

        modificarLinea(self, tipo):
            Crea un formulario para insertar o editar datos en la tabla
            herramientas.

        cargarSubgrupos(self, grupo):
            Rellena el cuadro de sugerencias de subgrupos.

        confirmarModificacion(self, tipo, datosPorDefecto=None):
            Modifica los datos de la tabla herramientas.

        eliminar(self):
            Elimina la fila de la tabla herramientas.
    """

    def __init__(self):
        super().__init__()

        self.titulo = qtw.QLabel("GESTIÓN DE HERRAMIENTAS")
        self.titulo.setObjectName("titulo")

        self.tabla = qtw.QTableWidget(self)
        self.tabla.setObjectName("tabla")
        self.campos = ("ID", "Descripción", "En condiciones",
                       "En reparación", "De baja", "Total", "Grupo",
                       "SubGrupo", "", "")
        self.tabla.setColumnCount(len(self.campos))
        self.tabla.setHorizontalHeaderLabels(self.campos)
        self.tabla.verticalHeader().hide()
        self.tabla.setColumnWidth(7, 35)
        self.tabla.setColumnWidth(8, 35)

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
        self.radioGrupo = qtw.QRadioButton("Grupo")
        self.radioSubgrupo = qtw.QRadioButton("Subgrupo")
        self.radioNombre.setObjectName("Radio1")
        self.radioGrupo.setObjectName("Radio2")
        self.radioSubgrupo.setObjectName("Radio3")
        self.radioNombre.toggled.connect(lambda: self.mostrarDatos())
        self.radioGrupo.toggled.connect(lambda: self.mostrarDatos())
        self.radioSubgrupo.toggled.connect(lambda: self.mostrarDatos())

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
        contenedor1Layout.addWidget(self.radioNombre, 0, 2)
        contenedor1Layout.addWidget(self.radioGrupo, 0, 3)
        contenedor1Layout.addWidget(self.radioSubgrupo, 0, 4)
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
        if self.radioNombre.isChecked():
            orden = "ORDER BY descripcion"
        elif self.radioGrupo.isChecked():
            orden = "ORDER BY grupo"
        elif self.radioSubgrupo.isChecked():
            orden = "ORDER BY subgrupo"
        else:
            orden = ""

        if orden and self.botonOrdenar.isChecked():
            orden += " ASC"

        db.cur.execute(
            f"""
            SELECT * FROM herramientas
            WHERE id LIKE ? 
            OR descripcion LIKE ? 
            OR cant_condiciones LIKE ? 
            OR cant_reparacion LIKE ? 
            OR cant_baja LIKE ? 
            OR total LIKE ?
            OR grupo LIKE ? 
            OR subgrupo LIKE ?
            {orden}
            """,
            (
                f"%{self.barraBusqueda.text()}", f"%{self.barraBusqueda.text()}",
                f"%{self.barraBusqueda.text()}", f"%{self.barraBusqueda.text()}",
                f"%{self.barraBusqueda.text()}", f"%{self.barraBusqueda.text()}",
                f"%{self.barraBusqueda.text()}", f"%{self.barraBusqueda.text()}"
            )
        )
        consulta = db.cur.fetchall()
        self.tabla.setRowCount(len(consulta))
        for i in range(len(consulta)):
            for j in range(len(consulta[i])):
                self.tabla.setItem(
                    i, j, qtw.QTableWidgetItem(str(consulta[i][j])))
            self.tabla.setRowHeight(i, 35)

            botonEditar = BotonFila("editar")
            botonEditar.clicked.connect(lambda: self.modificarLinea("editar"))
            self.tabla.setCellWidget(i, 7, botonEditar)

            botonEliminar = BotonFila("eliminar")
            botonEliminar.clicked.connect(lambda: self.eliminar())
            self.tabla.setCellWidget(i, 8, botonEliminar)

    def ordenar(self):
        """Este método cambia el ícono del botonOrdenar y actualiza los
        datos de la tabla de la pantalla."""
        self.botonOrdenar.cambiarIcono()
        self.mostrarDatos()

    def modificarLinea(self, tipo: str):
        """Este método crea un formulario para insertar o editar datos
        en la tabla herramientas.

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
        confirmarModificacion: modifica los datos de la tabla herramientas.
        """
        self.ventanaEditar = qtw.QWidget()
        self.ventanaEditar.setWindowTitle("Agregar Herramienta")
        self.ventanaEditar.setWindowIcon(
            qtg.QIcon(f"{os.path.abspath(os.getcwd())}/duraam/images/logo.png"))

        layoutVentanaModificar = qtw.QGridLayout()
        # El c está para prevenir un bug.
        c=0
        for i in range(len(self.campos)-2):
            if self.campos[i] != "Total":
                label = qtw.QLabel(f"{self.campos[i]}: ")
                label.setObjectName("modificar-label")
                layoutVentanaModificar.addWidget(
                    label, c, 0, alignment=qtc.Qt.AlignmentFlag.AlignRight)
                c += 1

        self.entry1 = qtw.QSpinBox()
        self.entry2 = qtw.QLineEdit()
        self.entry3 = qtw.QSpinBox()
        self.entry4 = qtw.QSpinBox()
        self.entry5 = qtw.QSpinBox()
        self.entry6 = qtw.QLineEdit()

        # Este código es para insertar sugerencias en el campo de
        # grupos para ayudar al usuario.
        db.cur.execute("SELECT id FROM grupos")
        sugerenciasGrupos = []
        for i in db.cur.fetchall():
            sugerenciasGrupos.append(i[0])
        # Objeto QCompleter: un cuadro de sugerencias para un QLineEdit
        # Toma como parámetro una lista con el nombre de cada
        # sugerencia y el widget al que pertenece el entry.
        cuadroSugerenciasGrupos = qtw.QCompleter(sugerenciasGrupos, self)
        # Método setCaseSensitivity: configura si las sugerencias
        # ignoran mayúsuculas o no. Por defecto no las ignoran.
        # Toma como método variables Qt de sensibilidad.
        # Variable CaseInsensitive: valor de un cuadro de sugerencias
        # que representa que no diferencia entre mayusculas y
        # minusculas. Pertenece a la clase CaseSensitivity, que
        # contiene las variables de sensibilidad ante mayúsuculas, que
        # es subclase de Qt.
        cuadroSugerenciasGrupos.setCaseSensitivity(
            qtc.Qt.CaseSensitivity.CaseInsensitive)
        # Se introduce el cuadro de sugerencias en el entry.
        self.entry6.setCompleter(cuadroSugerenciasGrupos)
        # Cuando cambia el texto de entry5, se activa el cuadro.
        self.entry6.textEdited.connect(
            lambda: self.cargarSubgrupos(self.entry5.text()))

        self.entry7 = qtw.QLineEdit()

        sugerenciasGrupos = []
        for i in db.cur.fetchall():
            sugerenciasGrupos.append(i[0])
        cuadroSugerenciasGrupos = qtw.QCompleter(sugerenciasGrupos, self)
        cuadroSugerenciasGrupos.setCaseSensitivity(
            qtc.Qt.CaseSensitivity.CaseInsensitive)

        self.entry1.setMaximum(9999)
        self.entry2.setMaxLength(100)
        self.entry3.setMaximum(9999)
        self.entry4.setMaximum(9999)
        self.entry5.setMaximum(9999)

        datos = []
        if tipo == "editar":
            botonClickeado = qtw.QApplication.focusWidget()
            posicion = self.tabla.indexAt(botonClickeado.pos())
            for cell in range(0, 9):
                datos.append(posicion.sibling(posicion.row(), cell).data())
            self.entry1.setValue(int(datos[0]))
            self.entry2.setText(datos[1])
            self.entry3.setValue(int(datos[2]))
            self.entry4.setValue(int(datos[3]))
            self.entry5.setValue(int(datos[4]))
            self.entry6.setText(datos[6])
            self.entry7.setText(datos[7])

            self.cargarSubgrupos(datos[5])
            self.ventanaEditar.setWindowTitle("Editar")

        entries = (self.entry1, self.entry2, self.entry3,  self.entry4,
                   self.entry5, self.entry6, self.entry7)
        for i in range(len(entries)):
            entries[i].setObjectName("modificar-entry")
            layoutVentanaModificar.addWidget(entries[i], i, 1)

        botonConfirmar = qtw.QPushButton("Confirmar")
        botonConfirmar.setObjectName("confirmar")

        botonConfirmar.clicked.connect(
            lambda: self.confirmarModificacion(datos))
        layoutVentanaModificar.addWidget(
            botonConfirmar, c+1, 0, 1, 2, alignment=qtc.Qt.AlignmentFlag.AlignCenter)

        self.ventanaEditar.setLayout(layoutVentanaModificar)
        self.ventanaEditar.show()

    def cargarSubgrupos(self, grupo):
        """Este método rellena el cuadro de sugerencias de subgrupos.

        Ver también
        -----------
        modificarLinea: crea un formulario para insertar o editar datos
        en la tabla herramientas.
        """
        db.cur.execute("SELECT ID FROM subgrupos WHERE grupo = ?", (grupo,))
        sugerenciasSubgrupos = []
        for i in db.cur.fetchall():
            sugerenciasSubgrupos.append(i[0])
        cuadroSugerenciasSubgrupos = qtw.QCompleter(sugerenciasSubgrupos, self)
        cuadroSugerenciasSubgrupos.setCaseSensitivity(
            qtc.Qt.CaseSensitivity.CaseInsensitive)
        self.entry6.setCompleter(cuadroSugerenciasSubgrupos)

    def confirmarModificacion(self, tipo: str, datosPorDefecto: list | None = None):
        """Este método modifica los datos de la tabla herramientas.

        Verifica que el grupo y el subgrupo sean correctos y luego
        intenta realizar los cambios, registrarlos en el historial,
        notificar al usuario el éxito de la operacion, actualizar la
        tabla de la pantalla y cerrar el formulario. Si la base de
        datos arroja un sqlite3.IntegrityError durante el intento, le
        notifica al usuario que se ha repetido un valor único y termina
        la ejecución de la función, sin modificar la tabla.

        Parámetros
        ----------
            tipo : str
                El tipo de modificación.
            datosPorDefecto : list, default = None
                Los datos de la fila previos a la modificación. 

        Ver también
        -----------
        modificarLinea: crea un formulario para insertar o editar datos
                        en la tabla herramientas.
        """
        db.cur.execute("""
        SELECT ID
        FROM grupos
        WHERE ID = ?""", (self.entry6.text().upper(),))

        grupo = db.cur.fetchall()

        if not grupo:
            m.mostrarMensaje("Error", "Error",
                             "El grupo no está ingresado. Por favor, verifique que el grupo ingresado es correcto.")
            return

        db.cur.execute("""
        SELECT ID
        FROM subgrupos
        WHERE ID = ?""", (self.entry7.text().upper(),))

        subgrupo = db.cur.fetchall()

        if not self.entry6.text() == "" and not subgrupo:
            m.mostrarMensaje("Error", "Error",
                             "El subgrupo no está ingresado. Por favor, verifique que el grupo ingresado es correcto.")
            return

        total = self.entry3.value() + self.entry4.value() + self.entry5.value()
        datosNuevos = (
            self.entry1.value(), self.entry2.text().upper(), self.entry3.value(),
            self.entry4.value(), self.entry5.value(), self.entry6.text(), total,
            self.entry7.text()
        )

        if tipo == "editar":
            try:
                db.cur.execute(
                    "SELECT * FROM herramientasWHERE ID = ?", (datosPorDefecto[0]))
                datosViejos = db.cur.fetchall()[0]
                db.cur.execute("""
                UPDATE herramientas
                SET ID = ?, descripcion = ?, cant_condiciones = ?, 
                cant_reparacion = ?, cant_baja = ?, total = ?,
                grupo = ?, subgrupo = ?
                WHERE ID = ?""", (
                    datosNuevos[0], datosNuevos[1], datosNuevos[2], datosNuevos[3],
                    datosNuevos[4], datosNuevos[5], datosNuevos[6], datosNuevos[7], 
                    datosPorDefecto,
                ))
                registrarCambios(
                    "Edicion", "Herramientas", datosPorDefecto[0], f"{datosViejos}", f"{datosNuevos}")
                db.con.commit()
                m.mostrarMensaje("Information", "Aviso",
                                 "Se ha actualizado la herramienta.")
            except sqlite3.IntegrityError:
                return m.mostrarMensaje(
                    "Error", "Error", "El ID ingresado ya está registrado. Por favor, ingrese otro.")
        else:
            try:
                db.cur.execute(
                    "INSERT INTO herramientas VALUES(?, ?, ?, ?, ?, ?, ?, ?) ", datosNuevos)
                registrarCambios("Insercion", "Herramientas",
                                 datosNuevos[0], None, f"{datosNuevos}")
                db.con.commit()
                m.mostrarMensaje("Information", "Aviso",
                                 "Se ha ingresado una herramienta.")
            except sqlite3.IntegrityError:
                return m.mostrarMensaje(
                    "Error", "Error", "El ID ingresado ya está registrado. Por favor, ingrese otro.")

        self.mostrarDatos()
        self.ventanaEditar.close()

    def eliminar(self):
        """Este método elimina la fila de la tabla herramientas.

        Antes de eliminar, confirma la decisión del usuario.
        Si los datos están relacionados con otras tablas, vuelve a
        confirmar la decisión del usuario. Luego, elimina la fila de la
        tabla herramientas y las filas en donde los datos estaban
        relacionadas.Por último, registra los cambios y actualiza la
        tabla.
        """
        respuesta = m.mostrarMensaje("Pregunta", "Advertencia",
                                     "¿Está seguro que desea eliminar estos datos?")
        if respuesta == qtw.QMessageBox.StandardButton.Yes:
            botonClickeado = qtw.QApplication.focusWidget()
            posicion = self.tabla.indexAt(botonClickeado.pos())
            idd = posicion.sibling(posicion.row(), 0).data()
            db.cur.execute(
                """
                SELECT * 
                FROM movimientos_herramientas 
                WHERE id_herramienta = ?
                """,
                (idd))
            tipo = "Eliminacion simple"
            tablas = "Herramientas"
            if db.cur.fetchall():
                tipo = "Eliminacion compleja"
                tablas = "Herramientas Movimientos de herramientas"
                respuesta = m.mostrarMensaje("Pregunta", "Advertencia",
                                             """
                Todavía hay herramientas y/o subgrupos cargados. 
                Eliminar el grupo eliminará también TODOS los datos en los que está ingresado.
                ¿Desea eliminarlo de todas formas?
                """)
        if respuesta == qtw.QMessageBox.StandardButton.Yes:
            db.cur.execute("SELECT * FROM herramientas WHERE id = ?", (idd,))
            datosEliminados = db.cur.fetchall()[0]
            db.cur.execute("DELETE FROM herramientas WHERE id = ?", (idd,))
            db.cur.execute(
                "DELETE FROM movimientos_herramientas WHERE ID = ?", (idd,))
            registrarCambios(tipo, tablas, idd, f"{datosEliminados}", None)
            db.con.commit()
            self.mostrarDatos()
