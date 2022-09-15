"""Este módulo crea una pantalla para gestionar la tabla de movimientos
de herramientas. 

Clases
------
    GestionMovimientosHerramientas:
        Crea una pantalla para gestionar la tabla de movimientos de
        herramientas.
"""
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import os
import datetime as dt
import sqlite3

import db.inicializar_bbdd as db
import mostrar_mensaje as m
from registrar_cambios import registrarCambios

class GestionMovimientosHerramientas(qtw.QWidget):
    """Esta clase crea una pantalla para gestionar la tabla de grupos.

    Hereda: PyQt6.QtWidgets.QWidget

    Atributos
    ---------
        tabla : QTableWidget
            la tabla de la pantalla.
        campos : tuple
            los títulos de las columnas de la tabla.
        barraBusqueda : QLabel
            la barra de búsqueda.
        radioHerramienta : QRadioButton
            el botón de radio para ordenar por herramienta.
        radioAlumno : QRadioButton
            el botón de radio para ordenar por alumno.
        radioFecha : QRadioButton
            el botón de radio para ordenar por fecha.
        entryFechaDesde : QDateTimeEdit
            el entry de fecha para marcar desde que fecha se pueden
            mostrar los datos.
        entryFechaHasta : QDateTimeEdit
            el entry de fecha para marcar hasta que fecha se pueden
            mostrar los datos.
        listaHerramientas : QComboBox
            una lista para elegir una herramienta para que se muestren
            solo sus datos
        listaEstado : QComboBox
            una lista para elegir que se muestren solo los datos con un
            dato específico
        
    Métodos
    -------
        __init__(self):
            El constructor de la clase GestionAlumnos.

            Crea la pantalla, un QWidget, que contiene:
                - Una tabla, un QTableWidget, que muestra los datos de
                  la tabla movimientos de herramientas y contiene 
                  botones para editarlos.
                - Una barra de buscador, un QLineEdit, para buscar los
                  datos.
                - Tres botones de radio, QRadioButton, para ordenar los
                  datos en base a columnas específicas.
                - Un botón, QCheckBox, para ordenar los
                  datos mostrados de manera ascendente o descendente
                  según el boton presionado.
                - Un botón para insertar datos a la tabla.
            
            Ver también
            -----------
            mostrarDatos: obtiene los datos de la tabla movimientos de herramientas y los
                          introduce en la tabla de la pantalla.

        mostrarDatos(self):
            Obtiene los datos de la tabla movimientos de herramientas y
            los introduce en la tabla de la pantalla.
        
        actualizarListas(self):
            Este método actualiza las listas de elementos.
        
        modificarLinea(self, tipo):
            Crea un formulario para insertar o editar datos en la tabla
            grupos.
        
        confirmarModificacion(self, tipo, datosPorDefecto=None):
            Modifica los datos de la tabla movimientos de herramientas.
        
        eliminar(self):
            Elimina la fila de la tabla movimientos de herramientas.
    """
    def __init__(self):
        # Se inicializa la clase QWidget.
        super().__init__()

        # Se crea el título.
        self.titulo=qtw.QLabel("GESTIÓN DE MOVIMIENTOS DE HERRAMIENTAS")
        self.titulo.setObjectName("titulo")

        # Se crea la tabla.
        self.tabla = qtw.QTableWidget(self)
        self.tabla.setObjectName("tabla")

        # Se crean los títulos de las columnas de la tabla y se introducen en esta.
        self.campos = ("ID", "Herramienta", "Nombre y Apellido", "Clase", "Fecha", "Cantidad", 
                        "Tipo", "Turno de Pañol", "", "") 
                                
        # Se establece el número de columnas que va a tener. 
        self.tabla.setColumnCount(len(self.campos))
        # Se introducen los títulos en la tabla.
        self.tabla.setHorizontalHeaderLabels(self.campos)

        # Se esconden los números de fila de la tabla que vienen por defecto para evitar confusión con el campo ID.
        self.tabla.verticalHeader().hide()
        # Se cambia el ancho de las dos últimas columnas, porque son las que van a tener los botones de editar y eliminar.
        self.tabla.setColumnWidth(2, 125)
        self.tabla.setColumnWidth(8, 35)
        self.tabla.setColumnWidth(9, 35)

        # Se crea una barra de búsqueda
        self.barraBusqueda = qtw.QLineEdit()
        self.barraBusqueda.setObjectName("buscar")
        # Se introduce un botón a la derecha que permite borrar la busqueda con un click.
        self.barraBusqueda.setClearButtonEnabled(True)
        # Se le pone el texto por defecto a la barra de búsqueda
        self.barraBusqueda.setPlaceholderText("Buscar...")
        # Se importa el ícono de lupa para la barra.
        iconoLupa=qtg.QPixmap(f"{os.path.abspath(os.getcwd())}/duraam/images/buscar.png")
        # Se crea un label que va a contener el ícono.
        contenedorIconoLupa=qtw.QLabel()
        contenedorIconoLupa.setObjectName("lupa")
        contenedorIconoLupa.setPixmap(iconoLupa)

        # Se le da la función de buscar los datos introducidos.
        self.barraBusqueda.textEdited.connect(lambda: self.mostrarDatos())
        # Se crean 3 botones de radio y un label para dar contexto.
        labelOrdenar = qtw.QLabel("Ordenar por: ")
        self.radioHerramienta = qtw.QRadioButton("Herramienta")
        self.radioAlumno = qtw.QRadioButton("Alumno")
        self.radioFecha = qtw.QRadioButton("Fecha")
        self.radioHerramienta.setObjectName("Radio1")
        self.radioAlumno.setObjectName("Radio2")
        self.radioFecha.setObjectName("Radio3")
        # Se le da a los botones de radio la función de mostrar datos en un orden específico.
        self.radioHerramienta.toggled.connect(lambda:self.mostrarDatos("Listado", 1))
        self.radioAlumno.toggled.connect(lambda:self.mostrarDatos("Listado", 2))
        self.radioFecha.toggled.connect(lambda:self.mostrarDatos("Listado", 3))

        labelPersona=qtw.QLabel("Persona: ")
        self.persona=qtw.QComboBox()

        labelDesdeFecha=qtw.QLabel("Desde: ")
        self.entryFechaDesde=qtw.QDateTimeEdit()
        self.entryFechaDesde.setDateTime(
            qtc.QDateTime.fromString("12/12/2012 00:00:00", "dd/MM/yyyy hh:mm:ss")
            )
        self.entryFechaDesde.dateTimeChanged.connect(lambda:self.mostrarDatos("Listado"))
        labelHastaFecha=qtw.QLabel("Hasta: ")
        self.entryFechaHasta=qtw.QDateTimeEdit()
        self.entryFechaHasta.setDateTime(
            qtc.QDateTime.fromString(
                dt.datetime.now.strftime("%d/%m/%Y %H:%M:%S"),
                "dd/MM/yyyy hh:mm:ss")
            )
        self.entryFechaHasta.dateTimeChanged.connect(lambda:self.mostrarDatos("Listado"))

        
        labelHerramienta=qtw.QLabel("Herramienta: ")
        self.listaHerramientas=qtw.QComboBox()
        self.listaHerramientas.addItem("Todas")
        self.listaHerramientas.currentIndexChanged.connect(lambda:self.mostrarDatos("Listado"))

        labelEstado=qtw.QLabel("Estado: ")
        self.listaEstado=qtw.QComboBox()
        self.listaEstado.addItem("Cualquiera")
        self.listaEstado.addItem("Retiro")
        self.listaEstado.addItem("Devolución")
        # Se crea el boton de agregar herramientas nuevas.
        botonAgregar = qtw.QPushButton("Agregar")
        botonAgregar.setObjectName("agregar")
        # Se le da la función.
        botonAgregar.clicked.connect(
            lambda: self.modificarLinea("agregar")
            )
        # Cuando el cursor pasa por el botón, cambia de forma.
        botonAgregar.setCursor(
            qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor)
            )

        # Se crea el layout y se le añaden todos los widgets anteriores.
        layout = qtw.QVBoxLayout()
        layout.addWidget(self.titulo)
        container1=qtw.QWidget()
        container1Layout=qtw.QGridLayout()
        container1Layout.addWidget(self.barraBusqueda, 0, 0)
        container1Layout.addWidget(contenedorIconoLupa, 0, 0)
        container1Layout.addWidget(labelOrdenar, 0, 1)
        container1Layout.addWidget(self.radioHerramienta, 0, 2)
        container1Layout.addWidget(self.radioAlumno, 0, 3)
        container1Layout.addWidget(self.radioFecha, 0, 4)
        container1.setLayout(container1Layout)
        layout.addWidget(container1)
        container2=qtw.QWidget()
        container2Layout=qtw.QHBoxLayout()
        container2Layout.addWidget(labelPersona)
        container2Layout.addWidget(self.persona)
        container2Layout.addWidget(labelDesdeFecha)
        container2Layout.addWidget(self.entryFechaDesde)
        container2Layout.addWidget(labelHastaFecha)
        container2Layout.addWidget(self.entryFechaHasta)
        container2Layout.addWidget(labelHerramienta)
        container2Layout.addWidget(self.listaHerramientas)
        container2Layout.addWidget(labelEstado)
        container2Layout.addWidget(self.listaEstado)
        container2.setLayout(container2Layout)
        layout.addWidget(container2)
        layout.addWidget(self.tabla)
        layout.addWidget(botonAgregar)
        # Se le da el layout al widget central
        self.setLayout(layout)
        # Se muestran los datos.
        self.actualizarListas()
        self.mostrarDatos()

    def mostrarDatos(self, consulta="Normal", orden=""):
        """Este método obtiene los datos de la tabla herramientas y los
        introduce en la tabla de la pantalla.
        """
        if self.persona.currentText() == "Todos":
            persona=""
        else:
            persona=self.persona.currentText()[10:]
        
        if self.listaHerramientas.currentText() == "Todas":
            herramientaABuscar=""
        else:
            herramientaABuscar=self.listaHerramientas.currentText()
        
        if self.listaEstado.currentText() == "Cualquiera":
            estado=""
        else:
            estado=self.listaHerramientas.currentText()
        
        ordenStatement=""
        if orden:
            if orden==1:
                ordenStatement="ORDER BY H.DESC_LARGA"
            if orden==2:
                ordenStatement="ORDER BY NOMBRE"
            if orden==3:
                ordenStatement="ORDER BY M.FECHA"


        db.cur.execute(
            f"""
            SELECT M.ID, H.DESC_LARGA, 
            (
                CASE WHEN M.CLASE = 0 THEN 
                    CASE WHEN EXISTS(
                        SELECT ID FROM ALUMNOS WHERE M.ID_PERSONA = A.ID) 
                    THEN A.nombre_apellido 
                    ELSE AH.nombre_apellido END
                ELSE
                    CASE WHEN EXISTS(
                        SELECT ID FROM PROFESORES WHERE M.ID_PERSONA = P.ID) 
                    THEN P.nombre_apellido 
                    ELSE PH.nombre_apellido END
                END
            ) AS NOMBRE,
            (CASE WHEN M.CLASE = 0 THEN "Alumno" ELSE "Profesor" END) AS CLASE, 
            M.FECHA, M.CANTIDAD, M.TIPO, M.ID_TURNO_PANOL
            FROM MOVIMIENTOS_HERRAMIENTAS M
            JOIN HERRAMIENTAS H
            ON M.ID_HERRAMIENTA = H.ID
            LEFT JOIN ALUMNOS A
            ON M.ID_PERSONA = A.ID
            LEFT JOIN ALUMNOS_HISTORICOS AH
            ON M.ID_PERSONA = AH.ID
            LEFT JOIN PROFESORES P
            ON M.ID_PERSONA = P.ID
            LEFT JOIN PROFESORES_HISTORICOS PH
            ON M.ID_PERSONA = PH.ID
            WHERE (H.DESC_LARGA LIKE ? 
            OR NOMBRE LIKE ? 
            OR M.ID LIKE ?
            OR M.FECHA LIKE ? 
            OR M.CANTIDAD LIKE ? 
            OR CLASE LIKE ? 
            OR M.ID_TURNO_PANOL LIKE ?)
            AND NOMBRE LIKE ?
            AND H.DESC_LARGA LIKE ?
            AND M.TIPO LIKE ?
            {ordenStatement}""", 
            (f"%{self.barraBusqueda.text()}%", f"%{self.barraBusqueda.text()}%",
            f"%{self.barraBusqueda.text()}%", f"%{self.barraBusqueda.text()}%", 
            f"%{self.barraBusqueda.text()}%", f"%{self.barraBusqueda.text()}%", 
            f"%{self.barraBusqueda.text()}%", f"%{persona}%", 
            f"%{herramientaABuscar}%", f"%{estado}%",)
        )

        consulta = []
        for i in db.cur.fetchall():
            fecha = qtc.QDateTime.fromString(i[4], "dd/MM/yyyy hh:mm:ss")
            if fecha >= self.entryFechaDesde.dateTime() and fecha <= self.entryFechaHasta.dateTime():
                consulta.append(i)

        # Se establece la cantidad de filas que va a tener la tabla
        self.tabla.setRowCount(len(consulta))
        # Bucle: por cada fila de la consulta obtenida, se guarda su id y se genera otro bucle que inserta todos los datos en la fila de la tabla de la ui.
        # Además, se insertan dos botones al costado de cada tabla: uno para editarla y otro para eliminarla.
        for i in range(len(consulta)):
            # Bucle: se introduce en cada celda el elemento correspondiente de la fila.
            for j in range(len(consulta[i])):
                self.tabla.setItem(i, j, qtw.QTableWidgetItem(str(consulta[i][j])))

            self.tabla.setRowHeight(i, 35)

            # Se crea el boton de editar, se le da la función de editar y se lo introduce después de introducir los datos.
            botonEditar = qtw.QPushButton()
            botonEditar.setIcon(qtg.QIcon(
                qtg.QPixmap(f"{os.path.abspath(os.getcwd())}/duraam/images/editar.png")))
            botonEditar.setIconSize(qtc.QSize(25, 25))
            botonEditar.setObjectName("editar")
            botonEditar.clicked.connect(lambda: self.modificarLinea("editar"))
            botonEditar.setCursor(qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor))
            self.tabla.setCellWidget(i, 8, botonEditar)

            # Se crea el boton de eliminar, se le da la función de eliminar la tabla con su id correspondiente y se introduce el boton al final de la fila.
            botonEliminar = qtw.QPushButton()
            botonEliminar.setIcon(qtg.QIcon(
                qtg.QPixmap(f"{os.path.abspath(os.getcwd())}/duraam/images/eliminar.png")))
            botonEliminar.setIconSize(qtc.QSize(25, 25))
            botonEliminar.setObjectName("eliminar")
            botonEliminar.clicked.connect(lambda: self.eliminar())
            botonEliminar.setCursor(qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor))
            self.tabla.setCellWidget(i, 9, botonEliminar)

    def actualizarListas(self):
        """Este método actualiza las listas de elementos."""
        try:
            self.persona.currentIndexChanged.disconnect()
        except:
            pass
        try:
            self.listaHerramientas.currentIndexChanged.disconnect()
        except:
            pass
        
        self.persona.clear()
        self.persona.addItem("Todos")
        self.listaHerramientas.clear()
        self.listaHerramientas.addItem("Todas")
        db.cur.execute("SELECT DISTINCT ID_PERSONA, CLASE FROM MOVIMIENTOS_HERRAMIENTAS")
        consulta=db.cur.fetchall()
        for i in consulta:
            if i[1]:
                db.cur.execute("SELECT nombre_apellido FROM PROFESORES WHERE ID = ?", (i[0],))
                self.persona.addItem(f"PROFESOR {db.cur.fetchall()[0][0]}")
            else:
                db.cur.execute("SELECT nombre_apellido FROM ALUMNOS WHERE ID = ?", (i[0],))
                nombre=db.cur.fetchall()[0][0]
                db.cur.execute("""
                SELECT CURSO
                FROM ALUMNOS
                WHERE ID IN (
                    SELECT ID_PERSONA
                    FROM MOVIMIENTOS_HERRAMIENTAS
                    WHERE ID = ? AND CLASE=0
                )
                """, (i[0],))
                self.persona.addItem(f"ALUMNO {db.cur.fetchall()[0][0]} {nombre}")

        db.cur.execute("SELECT DISTINCT ID_HERRAMIENTA FROM MOVIMIENTOS_HERRAMIENTAS")
        consulta=db.cur.fetchall()
        for i in consulta:
            db.cur.execute("SELECT DESC_LARGA FROM HERRAMIENTAS WHERE ID = ?", (i[0],))
            self.listaHerramientas.addItem(db.cur.fetchall()[0][0])
        
        self.persona.currentIndexChanged.connect(lambda:self.mostrarDatos("Listado"))

    def modificarLinea(self, tipo):
        """Este método crea un formulario para insertar o editar datos
        en la tabla movimientos de herramientas.

        El formulario es un QWidget que funciona como ventana. Por cada
        campo de la fila, agrega un entry y un label descriptivo. Al 
        confirmar los datos, ejecuta el método confirmar.

        Parámetros
        ----------
            tipo : str
                el tipo de formulario.
        
        Ver también
        -----------
        confirmarModificacion: modifica los datos de la tabla
        movimientos de herramientas.
        """
        # Se crea el widget que va a funcionar como ventana.
        self.edita = qtw.QWidget()
        # Se le da el título a la ventana, que por defecto es agregar.
        self.edita.setWindowTitle("Agregar Movimiento De Herramienta")
        self.edita.setWindowIcon(qtg.QIcon(f"{os.path.abspath(os.getcwd())}/duraam/images/bitmap.png"))

        # Se crea el layout.
        layoutVentanaModificar = qtw.QGridLayout()

        # Inserta un label por cada campo.
        for i in range(1, len(self.campos)-2):
            label = qtw.QLabel(f"{self.campos[i]}: ")
            label.setObjectName("modificar-label")
            layoutVentanaModificar.addWidget(label, i-1, 0, alignment=qtc.Qt.AlignmentFlag.AlignRight)
        
        # Crea los entries.
        self.entry1 = qtw.QLineEdit()
        db.cur.execute("SELECT DESC_LARGA FROM HERRAMIENTAS")
        sugerenciasHerramientas=[]
        for i in db.cur.fetchall():
            sugerenciasHerramientas.append(i[0])
        cuadroSugerenciasHerramientas=qtw.QCompleter(sugerenciasHerramientas, self)
        cuadroSugerenciasHerramientas.setCaseSensitivity(qtc.Qt.CaseSensitivity.CaseInsensitive)
        self.entry1.setCompleter(cuadroSugerenciasHerramientas)

        self.entry2 = qtw.QLineEdit()

        self.radioHerramienta = qtw.QRadioButton("Alumno")
        self.radioAlumno = qtw.QRadioButton("Profesor")
        agruparClase=qtw.QButtonGroup(self)
        agruparClase.addButton(self.radioHerramienta, 0)
        agruparClase.addButton(self.radioAlumno, 1)

        self.entry3= qtw.QDateTimeEdit()
        self.entry4 = qtw.QSpinBox()
        self.radioFecha = qtw.QRadioButton("Retiro")
        self.radio4 = qtw.QRadioButton("Devolución")
        agruparTipo=qtw.QButtonGroup(self)
        agruparTipo.addButton(self.radioFecha, 0)
        agruparTipo.addButton(self.radio4, 1)

        self.clase=0
        self.tipo=0
        self.radioHerramienta.toggled.connect(lambda: self.cambiarClase("Alumno"))
        self.radioAlumno.toggled.connect(lambda: self.cambiarClase("Profesor"))
        self.radioFecha.toggled.connect(lambda: self.cambiarTipo("Retiro"))
        self.radio4.toggled.connect(lambda: self.cambiarTipo("Devolucion"))
        self.radioHerramienta.toggle()
        self.radioFecha.toggle()

        self.radioHerramienta.setObjectName("tipo")
        self.radioAlumno.setObjectName("tipo")
        self.radioFecha.setObjectName("tipo")
        self.radio4.setObjectName("tipo")
        self.entry6 = qtw.QSpinBox()
        self.entry4.setMaximum(9999)
        self.entry6.setMaximum(9999)

        # Se crea una lista de datos vacía en la que se introduciran los valores que pasaran por defecto a la ventana.
        datos = []

        # Si el tipo es editar, se crea la pantalla de editar.
        if tipo == "editar":
            # Se obtiene la posición del boton clickeado: 
            # primero se obtiene cual fue último widget clickeado (en este caso el boton)
            botonClickeado = qtw.QApplication.focusWidget()
            # luego se obtiene la posicion del boton.
            posicion = self.tabla.indexAt(botonClickeado.pos())
            
            # Se añaden a la lista los valores de la fila, recorriendo cada celda de la fila. Cell se refiere a la posición de cada celda en la fila.
            for cell in range(0, len(self.campos)):
                datos.append(posicion.sibling(posicion.row(), cell).data())
            

            # Se crea la ventana de edición, pasando como parámetros los títulos de los campos de la tabla y los datos por defecto para que se muestren
            # Si se ingresaron datos, se muestran por defecto. Además, se muestra el id.
            # Se les añade a los entries sus valores por defecto.
            self.entry1.setText(datos[1])
            self.entry2.setText(datos[2])
            if int(datos[3]):
                self.radioAlumno.toggle()
            else:
                self.radioHerramienta.toggle()
            self.entry3.setDateTime(
                qtc.QDateTime.fromString(datos[4], "yyyy/MM/dd hh:mm:ss")
                )

            self.entry4.setValue(int(datos[5]))
            if int(datos[6]):
                self.radio4.toggle()
            else:
                self.radioFecha.toggle()
            self.entry6.setValue(int(datos[6]))
            self.edita.setWindowTitle("Editar")

        layoutVentanaModificar.addWidget(self.entry1, 0, 1, 1, 2)
        layoutVentanaModificar.addWidget(self.entry2, 1, 1, 1, 2)
        layoutVentanaModificar.addWidget(self.radioHerramienta, 2, 1)
        layoutVentanaModificar.addWidget(self.radioAlumno, 2, 2)
        layoutVentanaModificar.addWidget(self.entry3, 3, 1, 1, 2)
        layoutVentanaModificar.addWidget(self.entry4, 4, 1, 1, 2)
        layoutVentanaModificar.addWidget(self.radioFecha, 5, 1)
        layoutVentanaModificar.addWidget(self.radio4, 5, 2)
        layoutVentanaModificar.addWidget(self.entry6, 6, 1, 1, 2)

        entries=[self.entry1, self.entry2, self.entry4, self.entry6]
        for i in entries:
            i.setObjectName("modificar-entry")

        self.entry3.setObjectName("modificar-entry")
        # Se crea el boton de confirmar, y se le da la función de confirmarr.
        botonConfirmar = qtw.QPushButton("Confirmar")
        botonConfirmar.setObjectName("confirmar")
        botonConfirmar.setWindowIcon(qtg.QIcon(f"{os.path.abspath(os.getcwd())}/duraam/images/bitmap.png"))
        botonConfirmar.clicked.connect(lambda: self.confirmarModificacion(tipo, datos))
        layoutVentanaModificar.addWidget(botonConfirmar, 7, 0, 1, 6, alignment=qtc.Qt.AlignmentFlag.AlignCenter)

        # Se le da el layout a la ventana.
        self.edita.setLayout(layoutVentanaModificar)
        # Se muestra la ventana
        self.edita.show()

    def cambiarClase(self, clase):
        """Esta función crea un cuadro de sugerencias para el campo de
        nombre del formulario de modificación
        
        Ver también
        -----------
        modificarLinea: crea un formulario para insertar o editar datos
                        en la tabla movimientos de herramientas.
        """
        if clase=="Alumno":
            self.clase=0
            db.cur.execute("SELECT nombre_apellido FROM ALUMNOS")
        elif clase=="Profesor":
            self.clase=1
            db.cur.execute("SELECT nombre_apellido FROM PROFESORES")
        sugerencias=[]
        for i in db.cur.fetchall():
            sugerencias.append(i[0])
        cuadroSugerencias=qtw.QCompleter(sugerencias, self)
        cuadroSugerencias.setCaseSensitivity(qtc.Qt.CaseSensitivity.CaseInsensitive)
        self.entry2.setCompleter(cuadroSugerencias)
    
    def cambiarTipo(self, tipo):
        if tipo=="Retiro":
            self.tipo=0
        elif tipo=="Devolucion":
            self.tipo=1
    # Función confirmar: se añaden o cambian los datos de la tabla en base al parámetro datos.
    def confirmarModificacion(self, tipo, datosPorDefecto=None):
        """Esta función modifica los datos de la tabla herramientas.

        Verifica que la herramienta, la persona y el turno sean 
        correctos y luego intenta realizar los cambios, registrarlos en
        el historial y notificar al usuario el éxito de la operacion. 
        Si la base de datos arroja un sqlite3.IntegrityError durante el
        intento, le notifica al usuario que se ha repetido un valor 
        único y termina la ejecución de la función, sin modificar la
        tabla.

        Parámetros
        ----------
            tipo : str
                El tipo de modificación.
            datosPorDefecto : list
                Los datos de la fila previos a la modificación. 

        Ver también
        -----------
        modificarLinea: crea un formulario para insertar o editar datos
                        en la tabla movimientos de herramientas.
        """
        db.cur.execute("""
        SELECT ID
        FROM HERRAMIENTAS
        WHERE DESC_LARGA = ? 
        LIMIT 1""", (self.entry1.text().upper(),))

        herramienta=db.cur.fetchall()

        if not herramienta:
            return m.mostrarMensaje("Error", "Error", 
            """La herramienta no esta ingresada.
            Por favor, verifique que la herramienta ingresada es correcta.""")
            
        if self.clase:
            db.cur.execute("""
            SELECT ID
            FROM PROFESORES
            WHERE nombre_apellido = ?
            LIMIT 1
            """, (self.entry2.text().upper(),))

            persona=db.cur.fetchall()

            if not persona:
                m.mostrarMensaje("Error", "Error", 
                "El profesor no está ingresado. Por favor, verifique que el profesor ingresado es correcto.")
                return
        else:
            db.cur.execute("""
            SELECT ID
            FROM ALUMNOS
            WHERE nombre_apellido = ?
            LIMIT 1
            """, (self.entry2.text().upper(),))

            persona=db.cur.fetchall()

            if not persona:
                m.mostrarMensaje("Error", "Error", 
                "El alumno no está ingresado. Por favor, verifique que el alumno ingresado es correcto.")
                return
        
        db.cur.execute("""
        SELECT ID
        FROM TURNO_PANOL
        WHERE ID = ?
        LIMIT 1
        """, (self.entry6.value(),))

        turnoPanol=db.cur.fetchall()

        if not turnoPanol:
            m.mostrarMensaje("Error", "Error", 
            "El turno no está registrado. Por favor, verifique que el turno registrado es correcto.")
            return

        fecha=self.entry3.dateTime().toString("dd/MM/yyyy hh:mm:ss")
        
        datosNuevos=(
            herramienta[0][0], persona[0][0], self.clase, fecha, self.entry4.text(), self.tipo, 
            turnoPanol[0][0]
            )
        # Si habían datos por defecto, es decir, si se quería editar una fila, se edita la fila en la base de datos y muestra el mensaje.
        if tipo=="editar":
            db.cur.execute("""SELECT M.ID, H.DESC_LARGA, 
            (
                CASE WHEN M.CLASE = 0 THEN 
                    CASE WHEN EXISTS(
                        SELECT ID FROM ALUMNOS WHERE M.ID_PERSONA = A.ID) 
                    THEN A.nombre_apellido 
                    ELSE AH.nombre_apellido END
                ELSE
                    CASE WHEN EXISTS(
                        SELECT ID FROM PROFESORES WHERE M.ID_PERSONA = P.ID) 
                    THEN P.nombre_apellido 
                    ELSE PH.nombre_apellido END
                END
            ) AS NOMBRE,
            (CASE WHEN M.CLASE = 0 THEN "Alumno" ELSE "Profesor" END) AS CLASE, 
            M.FECHA, M.CANTIDAD, M.TIPO, M.ID_TURNO_PANOL
            FROM MOVIMIENTOS_HERRAMIENTAS M
            JOIN HERRAMIENTAS H
            ON M.ID_HERRAMIENTA = H.ID
            LEFT JOIN ALUMNOS A
            ON M.ID_PERSONA = A.ID
            LEFT JOIN ALUMNOS_HISTORICOS AH
            ON M.ID_PERSONA = AH.ID
            LEFT JOIN PROFESORES P
            ON M.ID_PERSONA = P.ID
            LEFT JOIN PROFESORES_HISTORICOS PH
            ON M.ID_PERSONA = PH.ID""")
            datosViejos=db.cur.fetchall()
            # Se actualiza la fila con su id correspondiente en la tabla de la base de datos.
            db.cur.execute("""
            UPDATE MOVIMIENTOS_HERRAMIENTAS
            SET ID_HERRAMIENTA = ?,
            ID_PERSONA = ?,
            CLASE = ?,
            FECHA = ?,
            CANTIDAD = ?,
            TIPO = ?,
            ID_TURNO_PANOL = ?
            WHERE ID = ?
            """, (
                datosNuevos[0], datosNuevos[1], datosNuevos[2], datosNuevos[3], datosNuevos[4], 
                datosNuevos[5], datosNuevos[6], datosPorDefecto,
            ))
            registrarCambios(
                "Edición", "Movimientos de herramientas", datosPorDefecto[0], f"{datosViejos}", f"{datosNuevos}"
                )
            db.con.commit()
            # Se muestra el mensaje exitoso.
            m.mostrarMensaje("Information", "Aviso",
                        "Se ha actualizado el movimiento.")           

        # Si no, se inserta la fila en la tabla de la base de datos.
        else:
            db.cur.execute("INSERT INTO MOVIMIENTOS_HERRAMIENTAS VALUES(NULL,?,?,?,?,?,?,?)", datosNuevos)
            registrarCambios("Inserción", "Movimientos de herramientas", datosNuevos[0], None, f"{datosNuevos}") 
            db.con.commit()
            m.mostrarMensaje("Information", "Aviso",
                        "Se ha ingresado un movimiento.")
            
        
        #Se refrescan los datos.
        self.actualizarListas()
        self.mostrarDatos()
        self.edita.close()

    # Función eliminar: elimina la fila de la tabla de la base de datos y de la tabla de la ui. Parámetro:
    # - idd: el id de la fila que se va a eliminar.
    def eliminar(self):
        """Esta función elimina la fila de la tabla movimientos de
        herramientas.

        Antes de eliminar, confirma la decisión del usuario.
        """
        respuesta = m.mostrarMensaje("Pregunta", "Advertencia",
                              "¿Está seguro que desea eliminar estos datos?")
        # si pulsó el boton de sí:
        if respuesta == qtw.QMessageBox.StandardButton.Yes:
            botonClickeado = qtw.QApplication.focusWidget()
            # luego se obtiene la posicion del boton.
            posicion = self.tabla.indexAt(botonClickeado.pos())
            idd=posicion.sibling(posicion.row(), 0).data()
            db.cur.execute(
            """
            SELECT M.ID, H.DESC_LARGA, 
            (
                CASE WHEN M.CLASE = 0 THEN 
                    CASE WHEN EXISTS(
                        SELECT ID FROM ALUMNOS WHERE M.ID_PERSONA = A.ID) 
                    THEN A.nombre_apellido 
                    ELSE AH.nombre_apellido END
                ELSE
                    CASE WHEN EXISTS(
                        SELECT ID FROM PROFESORES WHERE M.ID_PERSONA = P.ID) 
                    THEN P.nombre_apellido 
                    ELSE PH.nombre_apellido END
                END
            ) AS NOMBRE,
            (CASE WHEN M.CLASE = 0 THEN "Alumno" ELSE "Profesor" END) AS CLASE, 
            M.FECHA, M.CANTIDAD, M.TIPO, M.ID_TURNO_PANOL
            FROM MOVIMIENTOS_HERRAMIENTAS M
            JOIN HERRAMIENTAS H
            ON M.ID_HERRAMIENTA = H.ID
            LEFT JOIN ALUMNOS A
            ON M.ID_PERSONA = A.ID
            LEFT JOIN ALUMNOS_HISTORICOS AH
            ON M.ID_PERSONA = AH.ID
            LEFT JOIN PROFESORES P
            ON M.ID_PERSONA = P.ID
            LEFT JOIN PROFESORES_HISTORICOS PH
            ON M.ID_PERSONA = PH.ID
            """, (idd,))
            datosEliminados=db.cur.fetchall()
            # elimina la fila con el id correspondiente de la tabla de la base de datos.
            db.cur.execute("DELETE FROM MOVIMIENTOS_HERRAMIENTAS WHERE ID = ?", (idd,))
            registrarCambios("Eliminación simple", "Movimientos de herramientas", idd, f"{datosEliminados}", None)
            db.con.commit()
            self.mostrarDatos()