"""Este módulo crea una pantalla para gestionar la tabla alumnos.

Clases
------
    GestionAlumnos(qtw.QWidget):
        Crea una pantalla para gestionar la tabla alumnos.
"""

# Se importan las librerías de python:
# * PyQt6.QtWidgets: contiene los widgets de qt que usaremos en el
#                    módulo. Se importa con el alias qtw.
# * PyQt6.QtCore: contiene las clases núcleo de qt. La usaremos para
#                 obtener funcionalidades especiales. Se importa con el
#                 alias qtc.
# * PyQt6.QtGui: contiene clases que manejan los gráficos 2d, ventanas,
#                imágenes y fuentes. Se importa con el alias qtg.
# * os: permite manejar las rutas de archivos.
# * sqlite3: la usamos para poder manejar errores de la base de datos.
import sqlite3
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import os

# Se importan los módulos de la aplicación:
# * inicializar_bbdd: se encarga de la conexión a la base de datos.
# * botones: crea botones reutilizados en todos los módulos.
#                     Se importa con el nombre de db.
# * mostrar_mensaje: contiene una función que muestra un popup en la
#                    pantalla.
# * cursos: una lista con los cursos del colegio.
# * cambiar_icono: cambia el icono del boton de ordenar.
# * registrarCambios: guarda los cambios a la tabla en el historial.
import db.inicializar_bbdd as db
from .botones import BotonOrdenar, BotonFila
from . import mostrar_mensaje as m
from cursos import cursos
from registrar_cambios import registrarCambios


class GestionAlumnos(qtw.QWidget):
    """Esta clase crea una pantalla para gestionar la tabla alumnos.

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
            El botón de radio para ordenar los datos de la tabla
            por DNI.
        radioCurso : QRadioButton
            El botón de radio para ordenar los datos de la tabla por
            curso.
        botonOrdenar : QPushButton
            Un botón para ordenar los datos de la tabla de manera
            ascendente o descendente.

    Métodos
    -------
        __init__(self):
            El constructor de la clase GestionAlumnos.

            Crea la pantalla, un QWidget, que contiene: un título
            descriptivo, un QLabel; una tabla, un QTableWidget, que
            muestra los datos de la tabla alumnos y contiene botones
            para editarlos; una barra de buscador, un QLineEdit, para
            buscar los datos; botones de radio, QRadioWidget, para
            ordenar los datos mostrados según un dato seleccionado, un
            botón, QCheckBox, para ordenar los datos mostrados de
            manera ascendente o descendente según el boton presionado;
            un botón, un QPushButton, para insertar datos a la tabla.

        mostrarDatos(self):
            Obtiene los datos de la tabla alumnos y los introduce en 
            la tabla de la pantalla.

        ordenar(self):
            Cambia el ícono del botonOrdenar y actualiza los datos de
            la tabla de la pantalla.

        modificarLinea(self, tipo: str):
            Crea un formulario para insertar o editar datos en la tabla
            alumnos.

        confirmarModificacion(self, tipo: str, datosPorDefecto: list | None = None):
            Modifica los datos de la tabla alumnos.

        eliminar(self):
            Elimina la fila de la tabla alumnos.

        realizarPaseAnual(self):
            Crea un menú para realizar el pase anual de los alumnos de
            forma grupal.

        mostrarDatosPase(self):
            Obtiene los datos de los alumnos a pasar y los introduce en
            la tabla del menú de pase anual.

        confirmarPase(self):
            Actualiza los cursos en la tabla alumnos, realizando el
            pase anual y registrando los cambios en el historial.
    """
    # Se inicializa la clase con el constructor.

    def __init__(self):
        # Se inicializa la clase QWidget, de la que hereda nuestra
        # clase. QWidget: un widget vacío, que usaremos para crear
        # contenedores y pantallas.
        super().__init__()

        # Se crea el título, que es un widget QLabel.
        # QLabel: un label.
        titulo = qtw.QLabel("GESTIÓN DE ALUMNOS")

        # Se le pone el nombre de objeto para personalizarlo más tarde
        # con estilos. Método setObjectName: le pone un tag al objeto
        # para reconocerlo y poder aplicarle cambios de estilo.
        titulo.setObjectName("titulo")

        # Se crea la tabla, que es un QTableWidget. QTableWidget: un
        # widget que funciona como una tabla.
        self.tabla = qtw.QTableWidget(self)
        self.tabla.setObjectName("tabla")

        # Se crea la tupla campos, que contiene los títulos de las
        # columnas de la tabla. Los últimos dos títulos son texto vacío
        # porque ahí van a ir los botones para interactuar con las
        # filas, y no van a tener un título. Si no pusieramos texto
        # vacío, mostraría números por defecto.
        # Nota: una tupla es igual que una lista pero sus datos no
        # pueden cambiar.
        self.campos = ("ID", "DNI", "Nombre y Apellido",
                       "Curso", "Email", "", "")

        # Se establece el número de columnas que va a tener.
        # Método setColumnCount: establece el número de columnas
        # de un QTableWidget. En este caso, el número es del largo de
        # la lista campos, porque como cada columna va a tener un
        # título, la cantidad de columnas van a ser la cantidad de
        # títulos.
        self.tabla.setColumnCount(len(self.campos))

        # Se introducen los títulos en la tabla.
        # Método setHorizontalHeaderLabels: cambia los títulos de las
        # columnas de las tablas. Recibe de parámetro una lista con los
        # títulos. En este caso recibe la lista de campos.
        self.tabla.setHorizontalHeaderLabels(self.campos)

        # Se esconden los números de fila de la tabla que vienen por
        # defecto para evitar confusión con el campo ID.
        # Método verticalHeader().hide(): esconde los títulos
        # verticales (los de las filas).
        self.tabla.verticalHeader().hide()

        # Se cambia el ancho de las columnas para que los datos se vean
        # correctamente y los títulos no se corten.
        # Método setColumnWidth: cambia el ancho de una columna.
        # Recibe dos parámetros: el índice de la columna y el 
        # numero de pixeles de ancho, los dos como int.
        self.tabla.setColumnWidth(2, 120)
        self.tabla.setColumnWidth(4, 200)
        self.tabla.setColumnWidth(5, 35)
        self.tabla.setColumnWidth(6, 35)

        # Se crea una barra de búsqueda, que es un QLineEdit.
        # Clase QLineEdit: crea una caja de un renglón en el que se
        # escribe texto.
        self.barraBusqueda = qtw.QLineEdit()
        self.barraBusqueda.setObjectName("buscar")

        # Método setClearButtonEnabled: cuando es true, se introduce un
        # botón con una cruz a la derecha del QLineEdit que permite
        # borrar la busqueda al clickearlo.
        self.barraBusqueda.setClearButtonEnabled(True)

        # Se le pone el texto por defecto a la barra de búsqueda.
        # Método setPlaceholderText: le pone un texto que se muestra
        # al usuario pero que desaparece al comenzar a escribir,
        # haciendo de guía
        self.barraBusqueda.setPlaceholderText("Buscar...")

        # Se importa el ícono de lupa para la barra.
        # Método QPixmap: crea un mapa de pixeles de una imagen, que
        # qt usa para manejar las imágenes.
        iconoLupa = qtg.QPixmap(
            f"{os.path.abspath(os.getcwd())}/duraam/images/buscar.png")

        # Se crea un label que va a contener el ícono. Este label no va
        # a tener texto, solo el ícono.
        contenedorIconoLupa = qtw.QLabel()
        contenedorIconoLupa.setObjectName("lupa")

        # Se le pone el pixmap al ícono. Método setPixmap: introduce un
        # pixmap en un widget que lo pueda contener y lo muestra como
        # imagen.
        contenedorIconoLupa.setPixmap(iconoLupa)

        # Se le da la función de buscar los datos introducidos.
        # Todos los widgets arrojan señales cuando ocurren cosas, como
        # clicks, apretar enter, escribir, etc.
        # Método connect: conecta una función a una señal de un widget,
        # para que, cuando se dispare la señal, se ejecute la función.
        # Método textEdited: es una señal que se dispara cuando el
        # texto de un qlineedit es editado.
        # El lambda está ahí porque si no se bugea. No se que función
        # cumple en el connect (se que hace pero no entiendo que tiene
        # que ver con el connect). En tkinter también pasa lo mismo
        # para darle funciones a los botones. Despues investigo.
        self.barraBusqueda.textEdited.connect(
            lambda: self.mostrarDatos()
        )

        # Se crean 3 botones de radio y un label para dar contexto.
        # QRadioButton: un botón de radio.
        labelOrdenar = qtw.QLabel("Ordenar por: ")
        self.radioNombre = qtw.QRadioButton("Nombre")
        self.radioDNI = qtw.QRadioButton("DNI")
        self.radioCurso = qtw.QRadioButton("Curso")
        self.radioNombre.setObjectName("radio")
        self.radioDNI.setObjectName("radio")
        self.radioCurso.setObjectName("radio")

        # Se crea el botón para ordenar los resultados de manera
        # ascendente o descendente.
        self.botonOrdenar = BotonOrdenar()

        # Se le da la funcionalidad al botón.
        # Método stateChanged: señal que se dispara cuando se tickea el
        # botón.
        self.botonOrdenar.stateChanged.connect(lambda: self.ordenar())

        # Se le da la funcionalidad a los botones de radio.
        # Método toggled: señal que se dispara cuando se activa un
        # botón de radio o de tick.
        self.radioNombre.toggled.connect(lambda: self.mostrarDatos())
        self.radioDNI.toggled.connect(lambda: self.mostrarDatos())
        self.radioCurso.toggled.connect(lambda: self.mostrarDatos())

        # Se crea el boton de agregar alumnos nuevos.
        # QPushButton: un botón normal.
        botonAgregar = qtw.QPushButton("Agregar")
        botonAgregar.setObjectName("agregar")

        # Se le da la funcionalidad. Método clicked: señal que se
        # dispara cuando se clickea el widget.
        botonAgregar.clicked.connect(
            lambda: self.modificarLinea("agregar")
        )

        # Cambia la forma del cursor cuando pasa por encima del botón.
        # Método setCursor: maneja la forma del cursor cuando pasa por
        # encima del widget. El parámetro que recibe es un objeto
        # CursorShape de qt, que representa la forma del cursor.
        # Clase Qt: contiene identificadores misceláneos. Subclase de
        # QtCore
        # Clase CursorShape: contiene las distintas formas de cursor
        # que se pueden usar en Qt. Subclase de QtCore.Qt
        # Atributo PointingHandCursor: representa la forma de mano del
        # cursor. Pertenece a la clase CursorShape.
        botonAgregar.setCursor(
            qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor)
        )

        # Se crea el boton para realizar el pase anual.
        botonPaseAnual = qtw.QPushButton("Pase Anual")
        botonPaseAnual.setObjectName("confirmar")
        botonPaseAnual.clicked.connect(lambda: self.realizarPaseAnual())
        botonPaseAnual.setCursor(qtg.QCursor(
            qtc.Qt.CursorShape.PointingHandCursor))

        # Se crea el layout principal.
        # QVBoxLayout: un layout vertical.
        layout = qtw.QVBoxLayout()

        # Se le añade el título. Método addWidget: añade un widget.
        layout.addWidget(titulo)

        # Se crea el widget que sevirá de contenedor de la primera fila
        # de elementos.
        contenedor1 = qtw.QWidget()

        # Se crea el layout que se le dará al primer contenedor.
        # QGridLayout: un layout de grilla. Usamos este porque permite
        # meter dos objetos en el mismo lugar, ya que los otros no
        # permiten tener dos en la misma posición.
        contenedor1Layout = qtw.QGridLayout()

        # Se añade la barra de búsqueda, el ícono de lupa y los botones
        # de radio con su label.
        contenedor1Layout.addWidget(self.barraBusqueda, 0, 0)
        contenedor1Layout.addWidget(contenedorIconoLupa, 0, 0)
        contenedor1Layout.addWidget(labelOrdenar, 0, 1)
        contenedor1Layout.addWidget(self.radioNombre, 0, 2)
        contenedor1Layout.addWidget(self.radioDNI, 0, 3)
        contenedor1Layout.addWidget(self.radioCurso, 0, 4)
        contenedor1Layout.addWidget(self.botonOrdenar, 0, 5)
        # Se le da el layout al contenedor 1.
        # Método setLayout: le pone un layout a un widget.
        contenedor1.setLayout(contenedor1Layout)

        # Se añade el primer contenedor y la tabla al layout principal.
        layout.addWidget(contenedor1)
        layout.addWidget(self.tabla)

        # Se crea el segundo contenedor.
        contenedor2 = qtw.QWidget()

        # Se crea el layout para el segundo contenedor.
        # QHBoxLayout: un layout horizontal.
        contenedor2Layout = qtw.QHBoxLayout()

        # Se introducen los botones en el layout del contenedor 2.
        contenedor2Layout.addWidget(botonAgregar)
        contenedor2Layout.addWidget(botonPaseAnual)

        # Se le da el layout al contenedor 2 y se introduce en el
        # layout principal.
        contenedor2.setLayout(contenedor2Layout)
        layout.addWidget(contenedor2)

        # Se le pone el layout al widget central.
        self.setLayout(layout)

        # Se refrescan los datos de la tabla. Para saber exactamente
        # qué hace esta función, leanla más adelante.
        self.mostrarDatos()

    def mostrarDatos(self):
        """Este método obtiene los datos de la tabla alumnos y los
        introduce en la tabla de la pantalla.
        """
        # Si algún botón de radio de ordenar está apretado, guarda el
        # código SQL correspondiente. Sino, deja el orden vacío.
        # Método isChecked: devuelve true si el botón está checkeado,
        # y false si no.
        if self.radioNombre.isChecked():
            orden = "ORDER BY nombre_apellido"
        elif self.radioDNI.isChecked():
            orden = "ORDER BY dni"
        elif self.radioCurso.isChecked():
            orden = "ORDER BY curso"
        else:
            orden = ""

        # Si el botonOrdenar está presionado y hay un orden
        # seleccionado, lo ordena de forma ascendente, añadiendo
        # el " ASC" al final del order by.
        if orden and self.botonOrdenar.isChecked():
            orden += " ASC"

        # Se hace la consulta. Se seleccionan todas las filas que
        # coincidan con el texto de la barra de búsqueda y se introduce
        # el código SQL guardado en la variable orden para ordenar los
        # resultados de la consulta.
        # Los símbolos de pregunta ("?") representan un dato que
        # queremos poner desde python (texto, números, etc). En este
        # caso, cada uno representa el texto de la barra de búsqueda.
        # Despues del texto de la consulta, debe introducirse una tupla
        # o lista con valores, uno por cada ?. En este caso, como hay
        # 4 ?, la tupla tiene 4 datos, y cada uno es el texto de la
        # barra de búsqueda, por lo que cada ? va a ser ese texto.
        # El like lo que hace es devolver el texto que contenga otro
        # texto, es decir, checkea si el texto de la derecha del like
        # está dentro del texto del campo de la izquierda. Por ejemplo,
        # si se quiere buscar todas las filas con la fecha 2022, se
        # debería hacer lo siguiente: "WHERE FECHA LIKE %/2022". Esto
        # se traduce a "Seleccionar donde la fecha contenga el texto
        # /2022". Esto selecciona todas las fechas con el año 2022.
        # La variable orden puede ser un order by o nada, dependiendo
        # del botón de orden presionado.
        # Aclaro que si el usuario no busco nada no pasa nada, porque
        # entonces el texto de la barra quedará vacío y seleccionara
        # todas las filas por defecto. El like con un texto vacío
        # automáticamente selecciona todos los datos.
        # cur.execute(): ejecuta una sentencia SQL en la base de datos.
        db.cur.execute(
            f"""
            SELECT * FROM alumnos 
            WHERE id LIKE ? 
            OR dni LIKE ? 
            OR nombre_apellido LIKE ? 
            OR email LIKE ? 
            {orden}
            """,
            (
                f"%{self.barraBusqueda.text()}%",
                f"%{self.barraBusqueda.text()}%",
                f"%{self.barraBusqueda.text()}%",
                f"%{self.barraBusqueda.text()}%",
            )
        )

        # Se guarda el resultado de la consulta en una variable.
        consulta = db.cur.fetchall()

        # Se establece la cantidad de filas que va a tener la tabla.
        # setRowCount: establece el número de filas. En este caso,
        # el número de filas va a ser la cantidad de filas
        # seleccionadas en la consulta.
        self.tabla.setRowCount(len(consulta))

        # Por cada fila de la consulta, se genera otro bucle que
        # recorre todos los campos e inserta cada dato en la celda
        # correspondiente en la fila correspondiente de la tabla de la
        # ui. Al final de cada fila, se insertan dos botones, uno para
        # editar y el otro para eliminar los datos.
        for i in range(len(consulta)):
            # Se introduce el valor de cada celda de la fila de la
            # consulta en la celda correspondiente de la fila de la
            # tabla.
            for j in range(len(consulta[i])):
                # Método setItem: introduce un item de texto en la
                # celda correspondiente. Parámetros: ancho, alto
                # y un objeto QTableWidgetItem.
                # QTableWidgetItem: un item que se puede introducir en
                # una tabla. Parámetro: el texto del item.
                self.tabla.setItem(
                    i, j, qtw.QTableWidgetItem(str(consulta[i][j]))
                )

            # Aumentamos el tamaño de la altura de la fila en la tabla.
            # Método setRowHeight: cambia la altura de la fila.
            # Parámetros: índice de la fila y alto en píxeles.
            self.tabla.setRowHeight(i, 35)

            # Se crea el boton de editar, se le da la función de editar
            # y se lo introduce al final de la fila. Para ver una
            # explicación detallada del qpixmap y qsize, lean el módulo
            # de botones.py
            botonEditar = BotonFila("editar")
            botonEditar.clicked.connect(lambda: self.modificarLinea("editar"))
            self.tabla.setCellWidget(i, 5, botonEditar)

            # Se crea el botón de eliminar y se introduce al final de
            # la fila.
            botonEliminar = BotonFila("eliminar")
            botonEliminar.clicked.connect(lambda: self.eliminar())
            self.tabla.setCellWidget(i, 6, botonEliminar)

    def ordenar(self):
        """Este método cambia el ícono del botonOrdenar y actualiza los
        datos de la tabla de la pantalla."""
        self.botonOrdenar.cambiarIcono()
        self.mostrarDatos()

    def modificarLinea(self, tipo: str):
        """Este método crea un formulario para insertar o editar datos
        en la tabla alumnos.

        El formulario es un QWidget que funciona como ventana. Por cada
        campo de la fila, agrega un entry (QLineEdit o QSpinBox) y un
        label descriptivo. Al confirmar los datos, ejecuta el método 
        confirmarModificacion.

        Parámetros
        ----------
            tipo : str
                el tipo de formulario.

        Ver también
        -----------
        confirmarModificacion: modifica los datos de la tabla alumnos.
        """
        # Se crea el widget que va a funcionar como ventana.
        ventanaModificar = qtw.QWidget()

        # Se le da el título a la ventana, que por defecto es agregar.
        # Método setWindowTitle: establece el título de la ventana.
        ventanaModificar.setWindowTitle("Agregar Alumno")

        # Se establece el ícono de la ventana.
        # Método setWindowIcon: establece el ícono de una ventana.
        # Recibe como parámetro un objeto QIcon.
        ventanaModificar.setWindowIcon(
            qtg.QIcon(
                f"{os.path.abspath(os.getcwd())}/duraam/images/logo.png"
            )
        )

        # Se crea el layout.
        layoutVentanaModificar = qtw.QGridLayout()

        # Por cada campo, crea un label y lo inserta en el formulario.
        for i in range(len(self.campos)-2):
            label = qtw.QLabel(f"{self.campos[i]}: ")
            label.setObjectName("modificar-label")
            # Parámetro alignment: controla el alineamiento del
            # elemento en el layout. Por defecto está centrado. Recibe
            # como valor una variable Qt de alineamiento. En este caso,
            # es alignRight, que siginifica que lo alineamos a la
            # derecha.
            # Variable AlingRight: variable que significa que el widget
            # debe alinearse a la derecha. Pertenece a la clase 
            # AlignmentFlag.
            # Clase AlignmentFlag: contiene las variables de
            # alineamiento de qt. Subclase de Qt.
            layoutVentanaModificar.addWidget(
                label, i, 0, alignment=qtc.Qt.AlignmentFlag.AlignRight)

        # Se crean los entries.
        self.entry1 = qtw.QLineEdit()

        # QSpinBox: un entry numérico entero.
        self.entry2 = qtw.QSpinBox()

        self.entry3 = qtw.QLineEdit()
        self.entry4 = qtw.QLineEdit()
        self.entry5 = qtw.QLineEdit()

        # Se aumenta el máximo valor que puede tener el entry2, ya que
        # por defecto es 99 y necesitamos tener 8 dígitos como mínimo.
        # Método setMaximum: establece el máximo valor que puede tener
        # un QSpinBox
        self.entry2.setMaximum(99999999)

        # Se establece el máximo de caracteres de los entries para que
        # no se ingresen datos demasiado largos.
        # setMaxLength: establece el máximo de caracteres de un
        # QLineEdit.
        self.entry1.setMaxLength(4)
        self.entry3.setMaxLength(50)
        self.entry4.setMaxLength(2)
        self.entry5.setMaxLength(320)

        # Si el tipo es editar, se cargan los datos por defecto.
        if tipo == "editar":
            # Se crea una lista de datos vacía en la que se introduciran
            # los valores que pasaran por defecto a la ventana.
            datos = []

            # Se obtiene la fila en la que estaba el botón de edición
            # clickeado:
            # primero se obtiene cual fue último widget clickeado (en
            # este caso el boton).
            # focusWidget: obtiene el boton que está seleccionado.
            # Pertenece a la clase QApplication.
            botonClickeado = qtw.QApplication.focusWidget()

            # luego se obtiene la posicion del boton.
            # Método indexAt: obtiene el índice de la posicion de un
            # elemento. Método pos: obtiene la posición del último
            # widget clickeado.
            posicion = self.tabla.indexAt(botonClickeado.pos())

            # Se añaden a la lista los valores de la fila, recorriendo
            # cada celda de la fila.
            # celda se refiere a la posición de cada celda en la fila.
            # posicion.sibling se refiere al item que está en la celda
            # el data al final devuelve el texto de la celda.
            for celda in range(0, 6):
                datos.append(posicion.sibling(posicion.row(), celda).data())

            # Se les añade a los entries sus valores por defecto.
            # Método setValue: establece el valor de un QSpinBox.
            # Método setText: establece el texto de un QLineEdit.
            self.entry1.setText(datos[0])
            self.entry2.setValue(int(datos[1]))
            self.entry3.setText(datos[2])
            self.entry4.setText(datos[3])
            self.entry5.setText(datos[4])

            # Se le da el título a la ventana de edición
            ventanaModificar.setWindowTitle("Editar")

        # Se añaden los entries al layout.
        # Para no añadir cada uno manualmente, se crea un bucle que
        # automatiza el proceso.
        # Primero, se crea una tupla con todos los entries.
        entries = (self.entry1, self.entry2,
                   self.entry3, self.entry4, self.entry5)

        # Luego se hace el bucle. A cada entry de la tupla se le pone
        # su objectName y se lo agrega al layout.
        for i in range(len(entries)):
            entries[i].setObjectName("modificar-entry")
            layoutVentanaModificar.addWidget(entries[i], i, 1)

        # Se crea el boton de confirmar, y se le da la función de confirmarModificacion
        botonConfirmar = qtw.QPushButton("Confirmar")
        botonConfirmar.setObjectName("confirmar")
        botonConfirmar.setWindowIcon(
            qtg.QIcon(
                f"{os.path.abspath(os.getcwd())}/duraam/images/logo.png"
            )
        )
        botonConfirmar.clicked.connect(
            lambda: self.confirmarModificacion(tipo)
        )
        botonConfirmar.setCursor(
            qtg.QCursor(qtc.Qt.CursorShape.PointingHandCursor)
        )

        layoutVentanaModificar.addWidget(botonConfirmar, i+1, 0, 1, 2,
                                         alignment=qtc.Qt.AlignmentFlag.AlignCenter)

        # Se le da el layout a la ventana.
        ventanaModificar.setLayout(layoutVentanaModificar)

        # Se muestra la ventana. Método show: muestra el widget.
        ventanaModificar.show()

    def confirmarModificacion(self, tipo: str, datosPorDefecto: list | None = None):
        """Este método modifica los datos de la tabla alumnos.

        Verifica que el id no esté repetido en alumnos históricos y que
        el curso sea correcto y luego intenta realizar los cambios, 
        registrarlos en el historial, notificar al usuario el éxito de
        la operacion, actualizar la tabla de la pantalla y cerrar el
        formulario. Si la base de datos arroja un 
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
                        en la tabla alumnos.
        """
        # Busca el id en la tabla alumnos_historicos. Si está
        # registrado, notifica al usuario y finaliza la ejecución del
        # método.
        db.cur.execute(
            "SELECT id FROM alumnos_historicos WHERE id = ?", (self.entry1.text(),))
        if db.cur.fetchall():
            return m.mostrarMensaje("Error", "Error",
                                    "El ID ingresado ya está registrado en la tabla alumnos históricos. Por favor, ingrese otro.")

        # Si el curso no es correcto, notifica al usuario y finaliza
        # la ejecución del método.
        if self.entry4.text() not in cursos:
            return m.mostrarMensaje("Error", "Error",
                                    "El curso es incorrecto. Por favor, verifique que el curso ingresado es correcto.")

        # Guarda los datos ingresados por el usuario en una tupla para
        # usarlos más tarde.
        datosNuevos = (
            self.entry1.text(), self.entry2.value(),
            self.entry3.text().upper(), self.entry4.text(),
            self.entry5.text()
        )

        # Si el tipo de modificación es editar, se actualizan los datos.
        if tipo == "editar":
            try:
                # Se actualizan los datos en la tabla alumnos.
                db.cur.execute(
                    """
                    UPDATE alumnos
                    SET id = ?, dni = ?, nombre_apellido = ?,
                    curso = ?, email = ?
                    WHERE id = ?
                    """,
                    (
                        datosNuevos[0], datosNuevos[1], datosNuevos[2],
                        datosNuevos[3], datosNuevos[4], datosPorDefecto[0],
                    )
                )

                # Como el id está relacionado con otras tablas, también
                # debe cambiar al cambiar en la tabla de alumnos. Por
                # eso, se modifica en las tablas con las que está
                # relacionada (movimientos_herramientas y grupos)
                db.cur.execute(
                    """
                    UPDATE movimientos_herramientas
                    SET id_persona = ? 
                    WHERE clase = 0 AND id_persona = ?
                    """,
                    (datosNuevos[0], datosPorDefecto[0],)
                )
                db.cur.execute(
                    """
                    UPDATE turno_panol
                    SET id_alumno = ? WHERE id_alumno = ?
                    """,
                    (datosNuevos[0], datosPorDefecto[0],)
                )

                # Se guardan los cambios en el historial.
                registrarCambios("Edicion", "Alumnos", datosPorDefecto[0],
                                 f"{datosPorDefecto}", f"{datosNuevos}")

                # Se hace un commit de la transacción.
                db.con.commit()

                # Se muestra el mensaje exitoso.
                m.mostrarMensaje("Information", "Aviso",
                                 "Se ha actualizado el alumno.")

            # Si hay un error en la base de datos porque el id se
            # repite, en vez de parar el programa, notifica al usuario
            # de que no puede registrar el mismo id.
            except sqlite3.IntegrityError:
                m.mostrarMensaje("Error", "Error",
                                 "El ID ingresado ya está registrado. Por favor, ingrese otro.")

        # Si el tipo es editar, se inserta la fila en la tabla de la
        # base de datos, se guarda la transacción en el historial, se
        # hace el commit y se notifica al usuario.
        elif tipo == "insertar":
            try:
                db.cur.execute(
                    "INSERT INTO alumnos VALUES(?, ?, ?, ?, ?) ", datosNuevos
                )
                registrarCambios("Insercion", "Alumnos",
                                 datosNuevos[0], None, f"{datosNuevos}")
                db.con.commit()
                return m.mostrarMensaje("Information", "Aviso",
                                        "Se ha ingresado un alumno.")

            # Si salta error, se notifica al usuario.
            except sqlite3.IntegrityError:
                return m.mostrarMensaje("Error", "Error",
                                        "El ID ingresado ya está registrado. Por favor, ingrese otro.")

        # Se actualizan los datos.
        self.mostrarDatos()

        # Se cierra la ventana.
        # Método close: cierra un widget ventana.
        self.ventanaEditar.close()

    def eliminar(self):
        """Este método elimina la fila de la tabla alumnos.

        Antes de eliminar, confirma la decisión del usuario.
        Si los datos están relacionados con otras tablas, vuelve a
        confirmar la decisión del usuario. Luego, elimina la fila de la
        tabla alumnos y las filas en donde los datos estaban
        relacionados. Por último, registra los cambios y actualiza la
        tabla.
        """
        # se le pregunta al usuario si desea eliminar la fila.
        respuesta = m.mostrarMensaje("Pregunta", "Advertencia",
                                     "¿Está seguro que desea eliminar estos datos?")

        # si pulsó el boton de sí, sigue el código.
        # Nota: el mensaje no devuelve un "true o false" sino el boton
        # al que el usuario le hizo click. Por eso, la comparación del
        # if es con el objeto del boton de QT y no con un valor normal.
        # Disculpas si no se entiende bien al principio.
        if respuesta == qtw.QMessageBox.StandardButton.Yes:
            # Obtiene la posición del boton. La lógica ya está
            # explicada en el método modificarLinea.
            botonClickeado = qtw.QApplication.focusWidget()
            posicion = self.tabla.indexAt(botonClickeado.pos())
            idd = posicion.sibling(posicion.row(), 0).data()

            # Guarda el tipo de modificación y la tabla para usarlos
            # más tarde para guardar en el historial.
            tipo = "Eliminacion simple"
            tablas = "Alumnos"

            # Busca si hay datos relacionados en otras tablas.
            db.cur.execute(
                "SELECT * FROM movimientos_herramientas WHERE clase=0 AND id_persona = ?",
                (idd,)
            )

            # Si hay datos relacionados, cambia el tipo de
            # modificación y la tabla. Se le vuelve a preguntar al
            # usuario si está seguro de su decisión.
            if db.cur.fetchall():
                tipo = "Eliminacion compleja"
                tablas = "Alumnos Movimientos de herramientas Turnos del pañol"
                respuesta = m.mostrarMensaje("Pregunta", "Advertencia",
                    """El alumno tiene movimientos registrados. 
                    Eliminarlo eliminará tambien TODOS los movimientos en los que está registrado,
                    por lo que sus registros de deudas se eliminarán y podría perderse información valiosa.
                    ¿Desea eliminarlo de todas formas?""")

            # Si vuelve a responder que si, elimina los datos.
            if respuesta == qtw.QMessageBox.StandardButton.Yes:
                # Guarda los datos por eliminar en una variable para
                # registrarlos en el historial.
                db.cur.execute("SELECT * FROM alumnos WHERE ID = ?", (idd,))
                datosEliminados = db.cur.fetchall()[0]

                # Se eliminan los datos de la tabla y los datos
                # relacionados en la otra tabla.
                db.cur.execute("DELETE FROM alumnos WHERE ID = ?", (idd,))
                db.cur.execute(
                    """
                    DELETE FROM movimientos_herramientas
                    WHERE clase=0
                    AND id_persona = ?
                    """,
                    (idd,)
                )

                # Se elimina la relación entre los datos de la tabla y
                # los datos del turno pañol, pero no se eliminan los
                # datos del turno pañol para guardarlos por si se
                # necesitan.
                db.cur.execute(
                    "UPDATE turno_panol SET id_alumno=NULL WHERE id_alumno = ?", (idd,))

                # Se guardan los cambios en el historial y bla bla bla.
                registrarCambios(tipo, tablas, idd, f"{datosEliminados}", None)
                db.con.commit()
                self.mostrarDatos()

    def realizarPaseAnual(self):
        """Este método crea un menú para realizar el pase anual de
        los alumnos de forma grupal.

        El menú es un QWidget, que contiene:
            \n- Una tabla, QTableWiget, que contiene los datos de los
              alumnos y un botón de check por cada fila para
              seleccionarlas para el pase. Por defecto viene checkeado.
            \n- Una barra de búsqueda para navegar por los datos.
            \n- Un botón para realizar el pase de las filas seleccionadas

        Ver también
        -----------
        mostrarDatosPase: obtiene los datos de los alumnos a pasar y
                          los introduce en la tabla del menú de pase 
                          anual.
        """
        # Se crea el widget que va a funcionar como ventana, se
        # establece el título y el ícono.
        self.menuPase = qtw.QWidget()
        self.menuPase.setWindowTitle("Realizar Pase Anual de Alumnos")
        self.menuPase.setWindowIcon(
            qtg.QIcon(f"{os.path.abspath(os.getcwd())}/duraam/images/logo.png"))

        # Se crea el título.
        titulo = qtw.QLabel("Seleccione los alumnos que desea pasar de año.")
        titulo.setObjectName("subtitulo")

        # Crea la barra de búsqueda, ya explicada en el constructor.
        self.barraBusquedaPase = qtw.QLineEdit()
        self.barraBusquedaPase.setObjectName("buscar")
        self.barraBusquedaPase.setClearButtonEnabled(True)
        self.barraBusquedaPase.setPlaceholderText("Buscar...")
        self.barraBusquedaPase.textEdited.connect(
            lambda: self.mostrarDatosPase("Buscar"))

        # Se crea el pixmap del ícono y su contenedor.
        iconoLupa = qtg.QPixmap(
            f"{os.path.abspath(os.getcwd())}/duraam/images/buscar.png")
        contenedorIconoLupa = qtw.QLabel()
        contenedorIconoLupa.setObjectName("lupa")
        contenedorIconoLupa.setPixmap(iconoLupa)

        # Se crea la tabla y se le da el tamaño.
        self.tablaListaAlumnos = qtw.QTableWidget()
        self.tablaListaAlumnos.setMaximumSize(400, 345)

        # Se crean los títulos de la tabla. El primero está vacio
        # porque ahí van los botones de check.
        self.camposPase = ("", "Nombre y Apellido", "DNI", "Curso")

        # Se termina de configurar la tabla y se muestran los datos.
        # Lógica ya explicada en el constructor.
        self.tablaListaAlumnos.setColumnCount(len(self.camposPase))
        self.tablaListaAlumnos.setColumnWidth(0, 15)
        self.tablaListaAlumnos.setColumnWidth(1, 125)
        self.tablaListaAlumnos.setHorizontalHeaderLabels(self.camposPase)
        self.tablaListaAlumnos.verticalHeader().hide()
        self.mostrarDatosPase()

        # Se crea el boton de confirmar, y se configura. Ya explicado.
        botonConfirmar = qtw.QPushButton("Confirmar")
        botonConfirmar.setObjectName("confirmar")
        botonConfirmar.clicked.connect(lambda: self.confirmarPase())
        botonConfirmar.setCursor(qtg.QCursor(
            qtc.Qt.CursorShape.PointingHandCursor))

        # Se crea el layout y se introducen los widgets.
        layoutMenuPase = qtw.QVBoxLayout()
        layoutMenuPase.addWidget(titulo)
        layoutMenuPase.addWidget(self.barraBusquedaPase)
        layoutMenuPase.addWidget(contenedorIconoLupa)
        layoutMenuPase.addWidget(self.tablaListaAlumnos)
        layoutMenuPase.addWidget(botonConfirmar)
        layoutMenuPase.addWidget(botonConfirmar)

        # Se establece el layout de la ventana y se muestra.
        self.menuPase.setLayout(layoutMenuPase)
        self.menuPase.show()

    def mostrarDatosPase(self):
        """Este método obtiene los datos de los alumnos a pasar
        y los introduce en la tabla del menú de pase anual.

        Ver también
        -----------
        realizarPaseAnual: crea un menú para realizar el pase anual de
                           los alumnos de forma grupal.
        """
        # Se selecciona el nombre, dni y curso de la tabla alumnos
        # donde el curso sea alguno de los cursos registrados en la
        # tupla cursos.
        db.cur.execute(
            f"""
            SELECT nombre_apellido, dni, curso
            FROM alumnos
            WHERE curso IN (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            AND (nombre_apellido LIKE ?
            OR dni LIKE ?
            OR curso LIKE ?)
            ORDER BY curso, id
            """,
            (cursos, self.barraBusquedaPase.text(),
             self.barraBusquedaPase.text(), self.barraBusquedaPase.text())
        )

        # Se guarda la consulta en una variable.
        consulta = db.cur.fetchall()
        # Se establece la cantidad de filas que va a tener la tabla
        self.tablaListaAlumnos.setRowCount(len(consulta))
        # Recorre los datos obtenidos con un bucle y los inserta en la
        # tabla del menú.
        for i in range(len(consulta)):
            # Se crea el botón de tick (checkbox)
            # QCheckBox: un botón de tick.
            check = qtw.QCheckBox()
            check.setObjectName("check")
            check.toggle()
            self.tablaListaAlumnos.setCellWidget(i, 0, check)
            for j in range(len(consulta[i])):
                self.tablaListaAlumnos.setItem(
                    i, j+1, qtw.QTableWidgetItem(str(consulta[i][j])))

            self.tablaListaAlumnos.setRowHeight(i, 35)

    def confirmarPase(self):
        """Este método actualiza los cursos en la tabla alumnos, 
        realizando el pase anual.

        Si hay, al menos, un alumno de séptimo año seleccionado,
        confirma la decisión del usuario.

        Ver también
        -----------
        realizarPaseAnual: crea un menú para realizar el pase anual de
                           los alumnos de forma grupal.
        """
        # Se le da un valor por defecto a la variable respuesta para
        # que, si la pregunta no se hace, la variable exista y el
        # código siga.
        respuesta = qtw.QMessageBox.StandardButton.Yes
        # Por cada fila en la tabla del menú, verifica si hay un alumno
        # seleccionado de séptimo. Si hay, confirma la decision del
        # usuario. Luego, elimina todos los alumnos de séptimo y
        # actualiza el resto de cursos.
        for i in range(self.tablaListaAlumnos.rowCount()):
            # Si la fila está checkeada y el primer dígito del curso es
            # 7, sigue con el código.
            if (self.tablaListaAlumnos.cellWidget(i, 0).isChecked()
                    and self.tablaListaAlumnos.item(i, 3).text()[0] == "7"):
                # Confirma la decisión del usuario y rompe el bucle.
                respuesta = m.mostrarMensaje("Pregunta", "Advertencia",
                                             """Hay alumnos de séptimo año seleccionados. Hacer el pase eliminará a estos alumnos.
                Si quiere conservar sus datos, haga un registro histórico grupal y páselos a no activos.
                ¿Desea seguir con el pase de todas formas y eliminarlos?""")
                break
        # Si la respuesta es sí (puede ser porque el usuario eligio si
        # o porque la pregunta nunca se hizo y entonces respuesta tiene
        # su valor por defecto), sigue con el código.
        if respuesta == qtw.QMessageBox.StandardButton.Yes:
            # Se crean las listas para registrar los cambios en el
            # historial, por defecto vacías.
            datosViejos = []
            datosNuevos = []

            # Por cada fila en la tabla, si el botón esta checkeado y
            # el curso es un séptimo, lo elimina. Sino, pasa el curso
            # al siguiente.
            for i in range(self.tablaListaAlumnos.rowCount()):
                # Si el botón esta checkeado, sigue con el código.
                if self.tablaListaAlumnos.cellWidget(i, 0).isChecked():
                    # Si el curso comienza con 7, elimina la fila.
                    if self.tablaListaAlumnos.item(i, 3).text()[0] == "7":
                        db.cur.execute(
                            "DELETE FROM alumnos WHERE dni = ?",
                            (int(self.tablaListaAlumnos.item(i, 2).text()),)
                        )
                    # Si no, obtiene el curso, lo actualiza y registra
                    # los cambios.
                    else:
                        # Guarda el número del curso como entero y la
                        # letra, por separado en una lista.
                        curso = [int(self.tablaListaAlumnos.item(i, 3).text()[0]),
                                 self.tablaListaAlumnos.item(i, 3).text()[1]]
                        # Le suma un dígito al número del curso.
                        curso[0] += 1
                        # Se actualiza la tabla.
                        db.cur.execute(
                            "UPDATE alumnos SET curso = ? WHERE dni = ?",
                            (f"{curso[0]}{curso[1]}",
                             int(self.tablaListaAlumnos.item(i, 2).text()))
                        )
                        # Se guarda el id en la lista de datos nuevos.
                        datosNuevos.append(
                            int(self.tablaListaAlumnos.item(i, 2).text())
                        )
                    # Se guarda el id en la lista de datos viejos.
                    datosViejos.append(
                        int(self.tablaListaAlumnos.item(i, 2).text())
                    )

            # Se guardan los cambios en el historial y bla bla bla.
            registrarCambios("Pase anual", "Alumnos", None,
                             f"{datosViejos}", f"{datosNuevos}")
            db.con.commit()
            self.mostrarDatos()
            m.mostrarMensaje("Aviso", "Aviso",
                             "El pase anual se ha realizado con éxito.")
            self.menuPase.close()
