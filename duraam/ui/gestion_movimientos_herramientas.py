"""Este módulo crea una pantalla para gestionar la tabla 
movimientos_herramientas. 

Clases
------
    GestionMovimientosHerramientas(qtw.QWidget):
        Crea una pantalla para gestionar la tabla
        movimientos_herramientas.
"""
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import os
# Librería datetime: la usaremos para obtener la fecha y hora actuales.
# Se importa bajo el alias dt.
import datetime as dt

import db.inicializar_bbdd as db
from .botones import BotonOrdenar, BotonFila
from . import mostrar_mensaje as m
from registrar_cambios import registrarCambios


class GestionMovimientosHerramientas(qtw.QWidget):
    """Esta clase crea una pantalla para gestionar la tabla
    movimientos_herramientas.

    Hereda: PyQt6.QtWidgets.QWidget

    Atributos
    ---------
        tabla : QTableWidget
            La tabla de la pantalla.
        campos : tuple
            Los títulos de las columnas de la tabla.
        barraBusqueda : QLineEdit
            La barra de búsqueda.
        radioHerramienta : QRadioButton
            El botón de radio para ordenar los datos de la tabla por
            herramienta.
        radioAlumno : QRadioButton
            El botón de radio para ordenar los datos de la tabla por
            alumno.
        radioFecha : QRadioButton
            El botón de radio para ordenar los datos de la tabla por
            fecha.
        entryFechaDesde : QDateTimeEdit
            El entry de fecha para marcar desde que fecha se pueden
            mostrar los datos.
        entryFechaHasta : QDateTimeEdit
            El entry de fecha para marcar hasta que fecha se pueden
            mostrar los datos.
        listaHerramientas : QComboBox
            Una lista para elegir una herramienta para que se muestren
            solo sus datos
        listaEstado : QComboBox
            Una lista para elegir que se muestren solo los datos con un
            dato específico

    Métodos
    -------
        __init__(self):
            El constructor de la clase GestionMovimientosHerramientas.

            Crea la pantalla, un QWidget, que contiene: un título
            descriptivo, un QLabel; una tabla, un QTableWidget, que
            muestra los datos de la tabla movimientos_herramientas y
            contiene botones para editarlos; una barra de buscador, un
            QLineEdit, para buscar los datos; tres botones de radio,
            QRadioButton, para ordenar los datos en base a columnas
            específicas; un botón, QCheckBox, para ordenar los datos
            mostrados de manera ascendente o descendente según el boton
            presionado; un botón, un QPushButton, para insertar datos a
            la tabla.

            Ver también
            -----------
            mostrarDatos: obtiene los datos de la tabla movimientos_herramientas y los
                          introduce en la tabla de la pantalla.

        mostrarDatos(self):
            Obtiene los datos de la tabla movimientos_herramientas y
            los introduce en la tabla de la pantalla.

        actualizarListas(self):
            Actualiza las listas de elementos.

        modificarLinea(self, tipo):
            Crea un formulario para insertar o editar datos en la tabla
            movimientos_herramientas.

        confirmarModificacion(self, tipo, datosPorDefecto=None):
            Modifica los datos de la tabla movimientos_herramientas.

        eliminar(self):
            Elimina la fila de la tabla movimientos_herramientas.
    """

    def __init__(self):
        super().__init__()

        self.titulo = qtw.QLabel("GESTIÓN DE MOVIMIENTOS DE herramientas")
        self.titulo.setObjectName("titulo")

        self.tabla = qtw.QTableWidget(self)
        self.tabla.setObjectName("tabla")
        self.campos = ("ID", "Herramienta", "Nombre y Apellido", "Clase", "Fecha", "Cantidad",
                       "Tipo", "Turno de Pañol", "", "")
        self.tabla.setColumnCount(len(self.campos))
        self.tabla.setHorizontalHeaderLabels(self.campos)
        self.tabla.verticalHeader().hide()
        self.tabla.setColumnWidth(2, 125)
        self.tabla.setColumnWidth(8, 35)
        self.tabla.setColumnWidth(9, 35)

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
        self.radioHerramienta = qtw.QRadioButton("Herramienta")
        self.radioAlumno = qtw.QRadioButton("Alumno")
        self.radioFecha = qtw.QRadioButton("Fecha")
        self.radioHerramienta.setObjectName("Radio1")
        self.radioAlumno.setObjectName("Radio2")
        self.radioFecha.setObjectName("Radio3")
        self.radioHerramienta.toggled.connect(lambda: self.mostrarDatos())
        self.radioAlumno.toggled.connect(lambda: self.mostrarDatos())
        self.radioFecha.toggled.connect(lambda: self.mostrarDatos())

        self.botonOrdenar = BotonOrdenar()
        self.botonOrdenar.stateChanged.connect(lambda: self.ordenar())

        labelPersona = qtw.QLabel("Persona: ")
        self.persona = qtw.QComboBox()

        labelDesdeFecha = qtw.QLabel("Desde: ")

        # QDateTimeEdit: un entry de fecha y hora.
        self.entryFechaDesde = qtw.QDateTimeEdit()

        # Se establece su valor por defecto.
        # Función setDateTime: establece la fecha y hora de un
        # QDateTime. Toma como parámetro un objeto QDateTime.
        # QDateTime: un objeto de fecha y hora de Qt. Es sublcase de
        # QtCore. Nosotros lo que hacemos es hacer un objeto QDateTime
        # a partir de un string con la función fromString.
        # fromString: transforma una fecha de un string en un objeto
        # QDateTime. Toma dos parámetros: el string con la fecha y un
        # string para "formatearla", es decir, indicarle a qt que valor
        # significa cada número. El texto de la derecha introducido
        # significa que los primeros dos dígitos son fecha, los
        # segundos dos son de mes y los cuatro siguientes son de año.
        # Estan separados con barras / como en el string para que se
        # guarde igual en el objeto. Con la hora, los dos h son de
        # hora, los dos m son de minutos y los dos s de segundos.
        # El segundo string debe estar ordenado igual que el primero,
        # significa que tiene que tener las mismas barras y espacios
        # en el mismo orden, y tener letras que representen los números
        self.entryFechaDesde.setDateTime(
            qtc.QDateTime.fromString(
                "12/12/2012 00:00:00", "dd/MM/yyyy hh:mm:ss")
        )

        # Método dateTimeChanged: señal que se dispara cuando cambia el
        # valor del entry.
        self.entryFechaDesde.dateTimeChanged.connect(
            lambda: self.mostrarDatos())
        labelHastaFecha = qtw.QLabel("Hasta: ")
        self.entryFechaHasta = qtw.QDateTimeEdit()
        # Le damos a este entry la fecha y hora actuales por defecto.
        self.entryFechaHasta.setDateTime(
            # Esta función también recibe dos parametros asi que estén
            # atentos, solo que el primero es un string que viene de
            # la librería dt, esta explicado mas adelante, pero el
            # segundo string es igual al segundo que usamos en el
            # primer entry de fecha.
            qtc.QDateTime.fromString(
                # Clase datetime: construye un objeto datetime de
                # python, que no es un QDateTime de qt.
                # Método now: obtiene la fecha y hora actuales.
                # Método strftime: transforma una fecha de python en un
                # string. Cada porcentaje y letra simboliza un tipo de
                # dato. A diferencia del segundo string, este no
                # necesita una letra por cada dígito sino que entiende
                # que cada conjunto de digitos es un tipo de dato.
                # %d son los dos digitos de dia, %m son los dos de mes,
                # %Y son los cuatro de año, %H son los dos de hora, %M
                # son los dos de minuto y %S los dos de segundo.
                # Fijense que, fuera de las letras, las barras y los :
                # estan en los mismos lugares que en el segundo string.
                dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "dd/MM/yyyy hh:mm:ss"
            )
        )
        self.entryFechaHasta.dateTimeChanged.connect(
            lambda: self.mostrarDatos())

        labelHerramienta = qtw.QLabel("Herramienta: ")
        self.listaHerramientas = qtw.QComboBox()
        self.listaHerramientas.addItem("Todas")
        self.listaHerramientas.currentIndexChanged.connect(
            lambda: self.mostrarDatos())

        labelEstado = qtw.QLabel("Estado: ")
        self.listaEstado = qtw.QComboBox()
        self.listaEstado.addItem("Cualquiera")
        self.listaEstado.addItem("Retiro")
        self.listaEstado.addItem("Devolución")
        botonAgregar = qtw.QPushButton("Agregar")
        botonAgregar.setObjectName("agregar")
        botonAgregar.clicked.connect(
            lambda: self.modificarLinea("agregar")
        )
        botonAgregar.setCursor(
            qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor)
        )

        layout = qtw.QVBoxLayout()
        layout.addWidget(self.titulo)
        contenedor1 = qtw.QWidget()
        contenedor1Layout = qtw.QGridLayout()
        contenedor1Layout.addWidget(self.barraBusqueda, 0, 0)
        contenedor1Layout.addWidget(contenedorIconoLupa, 0, 0)
        contenedor1Layout.addWidget(labelOrdenar, 0, 1)
        contenedor1Layout.addWidget(self.radioHerramienta, 0, 2)
        contenedor1Layout.addWidget(self.radioAlumno, 0, 3)
        contenedor1Layout.addWidget(self.radioFecha, 0, 4)
        contenedor1Layout.addWidget(self.botonOrdenar, 0, 5)
        contenedor1.setLayout(contenedor1Layout)
        layout.addWidget(contenedor1)
        contenedor2 = qtw.QWidget()
        contenedor2Layout = qtw.QHBoxLayout()
        contenedor2Layout.addWidget(labelPersona)
        contenedor2Layout.addWidget(self.persona)
        contenedor2Layout.addWidget(labelDesdeFecha)
        contenedor2Layout.addWidget(self.entryFechaDesde)
        contenedor2Layout.addWidget(labelHastaFecha)
        contenedor2Layout.addWidget(self.entryFechaHasta)
        contenedor2Layout.addWidget(labelHerramienta)
        contenedor2Layout.addWidget(self.listaHerramientas)
        contenedor2Layout.addWidget(labelEstado)
        contenedor2Layout.addWidget(self.listaEstado)
        contenedor2.setLayout(contenedor2Layout)
        layout.addWidget(contenedor2)
        layout.addWidget(self.tabla)
        layout.addWidget(botonAgregar)
        self.setLayout(layout)
        self.actualizarListas()
        self.mostrarDatos()

    def mostrarDatos(self):
        """Este método obtiene los datos de la tabla herramientas y los
        introduce en la tabla de la pantalla.

        Los datos se muestran acorde a los filtros seleccionados de la
        pantalla.
        """
        # Primero, comprueba si las listas seleccionan todos los
        # elementos o solo uno.
        # Si el dato seleccionado de la lista persona es todos, guarda
        # en la variable persona el valor de texto vacío (""). Esto es
        # importante para la consulta más tarde.
        if self.persona.currentText() == "Todos":
            persona = ""
        # Sino, obtiene el texto seleccionado, lo separa y guarda en
        # una lista los valores.
        # Función split: agarra un texto y lo separa, y devuelve cada
        # trozo del texto por separado. Toma como parámetros: el
        # caracter que queremos usar para partir el texto y el numero
        # de veces que queremos que separe. En este caso, queremos que
        # separe el texto por los espacios 2 veces nomas, obteniendo un
        # máximo de 3 palabras.
        else:
            datosPersona = self.persona.currentText().split(" ", 2)
            # Si la primera palabra es "Alumno":
            if datosPersona[0] == "ALUMNO":
                # Guarda en la variable de persona el segundo trozo,
                # que es el nombre de la persona.
                persona = datosPersona[2]
            # Sino, guarda el primero.
            else:
                persona = datosPersona[1]
        # Lo de arriba ocurre por lo siguiente: si es un alumno, el
        # texto va a tener tres palabras: la clase, el curso y el
        # nombre. Pero si es profesor, solo va a tener dos: la clase y
        # el nombre. Por eso, si es un alumno guardamos la tercera
        # palabra y si es profe guardamos la segunda.

        # Hacemos lo mismo con herramientas. En este caso, como no hay
        # muchas palabras, agarramos directamente el texto como viene.
        if self.listaHerramientas.currentText() == "Todas":
            herramientaABuscar = ""
        else:
            herramientaABuscar = self.listaHerramientas.currentText()

        if self.listaEstado.currentText() == "Cualquiera":
            estado = ""
        else:
            estado = self.listaHerramientas.currentText()

        if self.radioAlumno.isChecked():
            orden = "ORDER BY nombre"
        elif self.radioHerramienta.isChecked():
            orden = "ORDER BY h.descripcion"
        elif self.radioFecha.isChecked():
            orden = "ORDER BY m.fecha_hora"
        else:
            orden = ""
        
        if orden and self.botonOrdenar.isChecked():
            orden += " DESC"
        elif self.botonOrdenar.isChecked():
            orden="ORDER BY nombre DESC"

        # Voy a explicar lo que hace este select porque parece chino
        # Al principio lo es pero despues es simple.
        # Vincula seis tablas: movimientos herramientas, herramientas,
        # alumnos, profesores, alumnos historicos y profesores
        # historicos. Obtiene primero el id de la fila de movimientos
        # herramientas y la descripcion de la tabla herramientas.
        # Luego ejecuta el comando case. El comando case funciona como
        # un if en sql: si se cumple la condicion del where hace algo
        # y sino hace otra cosa. En este caso, pregunta si la clase es
        # 0 (que significa alumno). Si es 0, entonces verifica que el
        # id esté en alumnos. Esto lo hacemos con el comando EXISTS,
        # que lo que hace es verificar si una subconsulta devuelve algo
        # o no. Si lo encuentra, selecciona el nombre de la tabla
        # alumnos, y si no, lo selecciona de la tabla
        # alumnos_historicos. Si la clase es 1, entonces hace lo mismo
        # pero con las tablas profesores y profesores_historicos.
        # Selecciona el resultado bajo el alias "nombre". Luego
        # ejecuta otro comando case: si la clase es 0, devuelve el
        # texto "Alumno" para indicar que el 0 se refiere a la clase
        # alumno. Sino, devuelve "Profesor". Devuelve este campo bajo
        # el alias "clase". Luego selecciona la fecha y hora, la
        # cantidad, el tipo y el id del turno panol, todos los datos
        # de la tabla movimientos_herramientas. Luego hace los joins de
        # todas las tablas. Los joins de alumnos, alumnos historicos,
        # profesores y profesores historicos son left joins porque
        # queremos que devuelva los datos aunque no coincida con todas
        # esas tablas (de hecho, es imposible que el id de persona
        # coincida con todas, por eso si no ponemos left join no
        # devuelve nada). Una vez hechos los joins, verifica primero
        # que se haya seleccionado al menos un nombre de persona con
        # EXISTS. Luego, verifica que todos los datos coincidan con la
        # búsqueda. Por último, verifica que el nombre de la persona,
        # la descripción de la herramienta y el tipo de movimiento
        # coincidan con lo seleccionado en las listas (por esto eran
        # importantes las variables de arriba). Finalmente, si hay un
        # orden guardado en la variable orden, se ordena la consulta.
        db.cur.execute(
            f"""
            SELECT m.id, h.descripcion, 
            (
                CASE WHEN m.clase = 0 THEN 
                    CASE WHEN EXISTS(
                        SELECT id FROM alumnos WHERE m.id_persona = a.id) 
                    THEN a.nombre_apellido 
                    ELSE ah.nombre_apellido END
                ELSE
                    CASE WHEN EXISTS(
                        SELECT id FROM profesores WHERE m.id_persona = p.id) 
                    THEN p.nombre_apellido 
                    ELSE ph.nombre_apellido END
                END
            ) AS nombre,
            (CASE WHEN m.clase = 0 THEN "Alumno" ELSE "Profesor" END) AS clase, 
            m.fecha_hora, m.cantidad, m.tipo, m.id_turno_panol
            FROM movimientos_herramientas m
            JOIN herramientas h
            ON m.id_herramienta = h.id
            LEFT JOIN alumnos a
            ON m.id_persona = a.id
            LEFT JOIN alumnos_historicos ah
            ON m.id_persona = ah.id
            LEFT JOIN profesores p
            ON m.id_persona = p.id
            LEFT JOIN profesores_historicos ph
            ON m.id_persona = ph.id
            WHERE (h.descripcion LIKE ? 
            OR nombre LIKE ? 
            OR m.id LIKE ?
            OR m.fecha_hora LIKE ? 
            OR m.cantidad LIKE ? 
            OR clase LIKE ? 
            OR m.id_turno_panol LIKE ?)
            AND nombre LIKE ?
            AND h.descripcion LIKE ?
            AND m.tipo LIKE ?
            {orden}""",
            (f"%{self.barraBusqueda.text()}%", f"%{self.barraBusqueda.text()}%",
             f"%{self.barraBusqueda.text()}%", f"%{self.barraBusqueda.text()}%",
             f"%{self.barraBusqueda.text()}%", f"%{self.barraBusqueda.text()}%",
             f"%{self.barraBusqueda.text()}%", f"%{persona}%",
             f"%{herramientaABuscar}%", f"%{estado}%",)
        )

        # Por último, filtra la consulta por fecha. Agarra la fecha de
        # todas las filas obtenidas y verifica si estan entre el rango
        # de fechas seleccionado por el usuario.
        consulta = []
        for i in db.cur.fetchall():
            fecha = qtc.QDateTime.fromString(i[4], "dd/MM/yyyy hh:mm:ss")
            if fecha >= self.entryFechaDesde.dateTime() and fecha <= self.entryFechaHasta.dateTime():
                consulta.append(i)

        self.tabla.setRowCount(len(consulta))
        for i in range(len(consulta)):
            for j in range(len(consulta[i])):
                self.tabla.setItem(
                    i, j, qtw.QTableWidgetItem(str(consulta[i][j])))

            self.tabla.setRowHeight(i, 35)

            botonEditar = BotonFila("editar")
            botonEditar.clicked.connect(lambda: self.modificarLinea("editar"))
            self.tabla.setCellWidget(i, 8, botonEditar)

            botonEliminar = BotonFila("eliminar")
            botonEliminar.clicked.connect(lambda: self.eliminar())
            self.tabla.setCellWidget(i, 9, botonEliminar)

    def actualizarListas(self):
        """Este método actualiza las listas de elementos."""
        # Este try y except es por lo siguiente:
        # Lo que hace el código es actualizar las listas de búsqueda
        # del listado, los ComboBox. Sin embargo, si yo quisiera
        # hacerlo sin desconectar la señal, se bugea el código.
        # Esto es porque lo que hace la señal es que, si cambian los
        # datos de la lista, se ejecute este código, pero este código
        # cambia los datos de la lista, entonces se vuelve a ejecutar,
        # y termina en un bucle infinito. Para evitar eso, desconecta-
        # mos la señal. Sin embargo, si la señal no estaba conectada
        # antes por algún motivo, salta error, por eso es que esta el
        # try and except, para que si llega a saltar error el código
        # siga.
        try:
            self.persona.currentIndexChanged.disconnect()
        except:
            pass
        try:
            self.listaHerramientas.currentIndexChanged.disconnect()
        except:
            pass

        # Se limpian las listas y se añade el item de "todos"
        # Método clear: elimina todos los items de la lista.
        self.persona.clear()
        self.persona.addItem("Todos")
        self.listaHerramientas.clear()
        self.listaHerramientas.addItem("Todas")

        # Selecciona a cada persona regristrada en la tabla. El
        # distinct está para no seleccionar la misma persona dos veces
        # y que no quede repetida en la lista.
        db.cur.execute(
            "SELECT DISTINCT ID_persona, clase FROM movimientos_herramientas")
        consulta = db.cur.fetchall()
        for i in consulta:
            # El i[1] es la clase de persona. Si es 1, es profesor. Si
            # es 0, es alumno. El if checkea si el dato es 1 o 0. Si el
            # dato es 1, selecciona el nombre del profesor. Si el dato
            # es 0, selecciona el nombre y el curso del alumno
            if i[1]:
                db.cur.execute(
                    "SELECT nombre_apellido FROM profesores WHERE ID = ?", (i[0],))
                profesor = db.cur.fetchall()[0][0]
                self.persona.addItem(f"PROFESOR {profesor}")
            else:
                db.cur.execute(
                    "SELECT curso, nombre_apellido FROM alumnos WHERE ID = ?", (i[0],))
                datosAlumno = db.cur.fetchall()[0]
                self.persona.addItem(
                    f"ALUMNO {datosAlumno[0]} {datosAlumno[1]}")

        # Selecciona las herramientas de la tabla y las mete en la lista.
        db.cur.execute(
            "SELECT DISTINCT ID_herramienta FROM movimientos_herramientas")
        consulta = db.cur.fetchall()
        for i in consulta:
            db.cur.execute(
                "SELECT descripcion FROM herramientas WHERE ID = ?", (i[0],))
            self.listaHerramientas.addItem(db.cur.fetchall()[0][0])

        self.persona.currentIndexChanged.connect(
            lambda: self.mostrarDatos())

    def ordenar(self):
        """Este método cambia el ícono del botonOrdenar y actualiza los
        datos de la tabla de la pantalla."""
        self.botonOrdenar.cambiarIcono()
        self.mostrarDatos()

    def modificarLinea(self, tipo: str):
        """Este método crea un formulario para insertar o editar datos
        en la tabla movimientos_herramientas.

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
        movimientos_herramientas.
        """
        self.ventanaModificar = qtw.QWidget()
        self.ventanaModificar.setWindowTitle(
            "Agregar Movimiento De Herramienta")
        self.ventanaModificar.setWindowIcon(
            qtg.QIcon(f"{os.path.abspath(os.getcwd())}/duraam/images/logo.png"))

        layoutVentanaModificar = qtw.QGridLayout()

        for i in range(1, len(self.campos)-2):
            label = qtw.QLabel(f"{self.campos[i]}: ")
            label.setObjectName("modificar-label")
            layoutVentanaModificar.addWidget(
                label, i-1, 0, alignment=qtc.Qt.AlignmentFlag.AlignRight)

        self.entry1 = qtw.QLineEdit()
        db.cur.execute("SELECT descripcion FROM herramientas")
        sugerenciasHerramientas = []
        for i in db.cur.fetchall():
            sugerenciasHerramientas.append(i[0])
        cuadroSugerenciasHerramientas = qtw.QCompleter(
            sugerenciasHerramientas, self)
        cuadroSugerenciasHerramientas.setCaseSensitivity(
            qtc.Qt.CaseSensitivity.CaseInsensitive)
        self.entry1.setCompleter(cuadroSugerenciasHerramientas)

        self.entry2 = qtw.QLineEdit()

        self.radioClaseAlumno = qtw.QRadioButton("Alumno")
        self.radioClaseProfesor = qtw.QRadioButton("Profesor")
        self.radioClaseAlumno.toggled.connect(
            lambda: self.cambiarClase("Alumno"))
        self.radioClaseProfesor.toggled.connect(
            lambda: self.cambiarClase("Profesor"))
        self.radioClaseAlumno.toggle()
        self.radioClaseAlumno.setObjectName("tipo")
        self.radioClaseProfesor.setObjectName("tipo")

        # QButtonGroup: agrupa botones. Sirve para lo siguiente:
        # Supongamos que tenes cuatro botones de radio en la pantalla,
        # dos arriba y dos abajo. lo que pasa normalmente es que si
        # queres seleccionar uno de arriba y uno de abajo al mismo
        # tiempo, no te deje, porque la aplicación piensa que todos
        # los botones estan relacionados y no te deja seleccionar dos
        # radios al mismo tiempo. Si uno quiere separarlos y poder
        # seleccionar uno de arriba y uno de abajo, debe agruparlos en
        # QButtonGroups.
        # Toma como parámetro el widget al que pertenece - si no lo
        # pones no funciona.
        agruparClase = qtw.QButtonGroup(self)
        agruparClase.addButton(self.radioClaseAlumno, 0)
        agruparClase.addButton(self.radioClaseProfesor, 1)

        self.entryFechaHora = qtw.QDateTimeEdit()
        self.entry4 = qtw.QSpinBox()

        self.radioRetiro = qtw.QRadioButton("Retiro")
        self.radioDevolucion = qtw.QRadioButton("Devolución")
        self.radioRetiro.toggle()
        self.radioRetiro.setObjectName("tipo")
        self.radioDevolucion.setObjectName("tipo")
        agruparTipo = qtw.QButtonGroup(self)
        agruparTipo.addButton(self.radioRetiro, 0)
        agruparTipo.addButton(self.radioDevolucion, 1)

        self.entry6 = qtw.QSpinBox()
        self.entry4.setMaximum(9999)
        self.entry6.setMaximum(9999)

        datos = []

        if tipo == "editar":
            botonClickeado = qtw.QApplication.focusWidget()
            posicion = self.tabla.indexAt(botonClickeado.pos())

            for cell in range(0, len(self.campos)):
                datos.append(posicion.sibling(posicion.row(), cell).data())

            self.entry1.setText(datos[1])
            self.entry2.setText(datos[2])
            if int(datos[3]):
                self.radioClaseProfesor.toggle()
            else:
                self.radioClaseAlumno.toggle()
            self.entryFechaHora.setDateTime(
                qtc.QDateTime.fromString(datos[4], "yyyy/MM/dd hh:mm:ss")
            )

            self.entry4.setValue(int(datos[5]))
            if int(datos[6]):
                self.radioDevolucion.toggle()
            else:
                self.radioRetiro.toggle()
            self.entry6.setValue(int(datos[6]))
            self.ventanaModificar.setWindowTitle("Editar")

        layoutVentanaModificar.addWidget(self.entry1, 0, 1, 1, 2)
        layoutVentanaModificar.addWidget(self.entry2, 1, 1, 1, 2)
        layoutVentanaModificar.addWidget(self.radioClaseAlumno, 2, 1)
        layoutVentanaModificar.addWidget(self.radioClaseProfesor, 2, 2)
        layoutVentanaModificar.addWidget(self.entryFechaHora, 3, 1, 1, 2)
        layoutVentanaModificar.addWidget(self.entry4, 4, 1, 1, 2)
        layoutVentanaModificar.addWidget(self.radioRetiro, 5, 1)
        layoutVentanaModificar.addWidget(self.radioDevolucion, 5, 2)
        layoutVentanaModificar.addWidget(self.entry6, 6, 1, 1, 2)

        entries = [self.entry1, self.entry2, self.entryFechaHora,
                   self.entry4, self.entry6]
        for i in entries:
            i.setObjectName("modificar-entry")

        botonConfirmar = qtw.QPushButton("Confirmar")
        botonConfirmar.setObjectName("confirmar")
        botonConfirmar.clicked.connect(
            lambda: self.confirmarModificacion(tipo, datos))
        layoutVentanaModificar.addWidget(
            botonConfirmar, 7, 0, 1, 6, alignment=qtc.Qt.AlignmentFlag.AlignCenter)

        self.ventanaModificar.setLayout(layoutVentanaModificar)
        self.ventanaModificar.show()

    def cambiarClase(self, clase):
        """Este método crea un cuadro de sugerencias para el campo de
        nombre del formulario de modificación

        Ver también
        -----------
        modificarLinea: crea un formulario para insertar o editar datos
                        en la tabla movimientos_herramientas.
        """
        if clase == "Alumno":
            self.clase = 0
            db.cur.execute("SELECT nombre_apellido FROM alumnos")
        elif clase == "Profesor":
            self.clase = 1
            db.cur.execute("SELECT nombre_apellido FROM profesores")
        sugerencias = []
        for i in db.cur.fetchall():
            sugerencias.append(i[0])
        cuadroSugerencias = qtw.QCompleter(sugerencias, self)
        cuadroSugerencias.setCaseSensitivity(
            qtc.Qt.CaseSensitivity.CaseInsensitive)
        self.entry2.setCompleter(cuadroSugerencias)

    def confirmarModificacion(self, tipo: str, datosPorDefecto: list | None = None):
        """Este método modifica los datos de la tabla
        movimientos_herramientas.

        Verifica que la herramienta, la persona y el turno sean 
        correctos y luego intenta realizar los cambios, registrarlos en
        el historial, notificar al usuario el éxito de la operacion,
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
                        en la tabla movimientos_herramientas.
        """
        db.cur.execute("""
        SELECT ID
        FROM herramientas
        WHERE descripcion = ? 
        LIMIT 1""", (self.entry1.text().upper(),))

        herramienta = db.cur.fetchall()

        if not herramienta:
            return m.mostrarMensaje("Error", "Error",
                                    """La herramienta no esta ingresada.
            Por favor, verifique que la herramienta ingresada es correcta.""")

        if self.clase:
            db.cur.execute("""
            SELECT ID
            FROM profesores
            WHERE nombre_apellido = ?
            LIMIT 1
            """, (self.entry2.text().upper(),))

            persona = db.cur.fetchall()

            if not persona:
                m.mostrarMensaje("Error", "Error",
                                 "El profesor no está ingresado. Por favor, verifique que el profesor ingresado es correcto.")
                return
        else:
            db.cur.execute("""
            SELECT ID
            FROM alumnos
            WHERE nombre_apellido = ?
            LIMIT 1
            """, (self.entry2.text().upper(),))

            persona = db.cur.fetchall()

            if not persona:
                m.mostrarMensaje("Error", "Error",
                                 "El alumno no está ingresado. Por favor, verifique que el alumno ingresado es correcto.")
                return

        if self.radioRetiro.isChecked():
            tipoDevolucion = 0
        else:
            tipoDevolucion = 1

        db.cur.execute("""
        SELECT ID
        FROM turno_panol
        WHERE ID = ?
        LIMIT 1
        """, (self.entry6.value(),))

        turnoPanol = db.cur.fetchall()

        if not turnoPanol:
            m.mostrarMensaje("Error", "Error",
                             "El turno no está registrado. Por favor, verifique que el turno registrado es correcto.")
            return

        fecha = self.entryFechaHora.dateTime().toString("dd/MM/yyyy hh:mm:ss")

        datosNuevos = (
            herramienta[0][0], persona[0][0], self.clase, fecha, self.entry4.text(
            ), tipoDevolucion,
            turnoPanol[0][0]
        )
        if tipo == "editar":
            # Selecciona los datos viejos antes de eliminarlo. La
            # consulta ya esta explicada más arriba asi que no se coman
            # la cabeza y no me rompan las bolas.
            db.cur.execute("""SELECT m.id,h.descripcion, 
            (
                CASE WHEN m.clase = 0 THEN 
                    CASE WHEN EXISTS(
                        SELECT ID FROM alumnos WHERE m.id_persona = a.id) 
                    THEN A.nombre_apellido 
                    ELSE AH.nombre_apellido END
                ELSE
                    CASE WHEN EXISTS(
                        SELECT ID FROM profesores WHERE m.id_persona = p.id) 
                    THEN P.nombre_apellido 
                    ELSE PH.nombre_apellido END
                END
            ) AS nombre,
            (CASE WHEN m.clase = 0 THEN "Alumno" ELSE "Profesor" END) AS clase, 
            m.fecha_hora, m.cantidad, m.tipo, m.id_turno_panol
            FROM movimientos_herramientas M
            JOIN herramientas H
            ON m.id_herramienta = h.id
            LEFT JOIN alumnos A
            ON m.id_persona = a.id
            LEFT JOIN alumnos_historicos AH
            ON m.id_persona = Ah.id
            LEFT JOIN profesores P
            ON m.id_persona = p.id
            LEFT JOIN profesores_historicos PH
            ON m.id_persona = Ph.id""")
            datosViejos = db.cur.fetchall()
            db.cur.execute("""
            UPDATE movimientos_herramientas
            SET ID_herramienta = ?,
            ID_persona = ?,
            clase = ?,
            FECHA = ?,
            CANTIDAD = ?,
            TIPO = ?,
            ID_turno_panol = ?
            WHERE ID = ?
            """, (
                datosNuevos[0], datosNuevos[1], datosNuevos[2], datosNuevos[3], datosNuevos[4],
                datosNuevos[5], datosNuevos[6], datosPorDefecto,
            ))
            registrarCambios(
                "Edicion", "Movimientos de herramientas", datosPorDefecto[
                    0], f"{datosViejos}", f"{datosNuevos}"
            )
            db.con.commit()
            m.mostrarMensaje("Information", "Aviso",
                             "Se ha actualizado el movimiento.")

        else:
            db.cur.execute(
                "INSERT INTO movimientos_herramientas VALUES(NULL,?,?,?,?,?,?,?)", datosNuevos)
            registrarCambios("Insercion", "Movimientos de herramientas",
                             datosNuevos[0], None, f"{datosNuevos}")
            db.con.commit()
            m.mostrarMensaje("Information", "Aviso",
                             "Se ha ingresado un movimiento.")

        self.actualizarListas()
        self.mostrarDatos()
        self.ventanaModificar.close()

    def eliminar(self):
        """Este método elimina la fila de la tabla 
        movimientos_herramientas.

        Antes de eliminar, confirma la decisión del usuario. Al
        finalizar, registra los cambios y actualiza la tabla.
        """
        respuesta = m.mostrarMensaje("Pregunta", "Advertencia",
                                     "¿Está seguro que desea eliminar estos datos?")
        if respuesta == qtw.QMessageBox.StandardButton.Yes:
            botonClickeado = qtw.QApplication.focusWidget()
            posicion = self.tabla.indexAt(botonClickeado.pos())
            idd = posicion.sibling(posicion.row(), 0).data()
            db.cur.execute(
                """
                SELECT m.id,h.descripcion, 
                (
                    CASE WHEN m.clase = 0 THEN 
                        CASE WHEN EXISTS(
                            SELECT ID FROM alumnos WHERE m.id_persona = a.id) 
                        THEN A.nombre_apellido 
                        ELSE AH.nombre_apellido END
                    ELSE
                        CASE WHEN EXISTS(
                            SELECT ID FROM profesores WHERE m.id_persona = p.id) 
                        THEN P.nombre_apellido 
                        ELSE PH.nombre_apellido END
                    END
                ) AS nombre,
                (CASE WHEN m.clase = 0 THEN "Alumno" ELSE "Profesor" END) AS clase, 
                m.fecha_hora, m.cantidad, m.tipo, m.id_turno_panol
                FROM movimientos_herramientas M
                JOIN herramientas H
                ON m.id_herramienta = h.id
                LEFT JOIN alumnos A
                ON m.id_persona = a.id
                LEFT JOIN alumnos_historicos AH
                ON m.id_persona = Ah.id
                LEFT JOIN profesores P
                ON m.id_persona = p.id
                LEFT JOIN profesores_historicos PH
                ON m.id_persona = Ph.id
                """, (idd,))
            datosEliminados = db.cur.fetchall()
            db.cur.execute(
                "DELETE FROM movimientos_herramientas WHERE ID = ?", (idd,))
            registrarCambios(
                "Eliminacion simple", "Movimientos de herramientas", idd, f"{datosEliminados}", None)
            db.con.commit()
            self.mostrarDatos()
