# Este es el código inicial - Una ventana que permite que el usuario realize un CRUD de la base de datos.
# Se realizan las importaciones necesarias.
import sys
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import sqlite3 as db
import os

# Se hace la conexión. Si el primero no funciona, intenta la segunda opción.
try:
    con = db.Connection(f"{os.path.abspath(os.getcwd())}/duraam/db/duraam.sqlite3")
except:
    try:
        os.chdir(f"{os.path.abspath(os.getcwd())}/Documents/Duraam")
        con = db.Connection(f"{os.path.abspath(os.getcwd())}/duraam/db/duraam.sqlite3")
    except:
        os.chdir(f"{os.path.abspath(os.getcwd())}/Documents/Duraam")
# Se crea el cursor.
cur = con.cursor()

# Función mostrarMensaje: muestra un mensaje en la pantalla. Los argumentos son:
# - title: funciona como el título del mensaje y también se usa para identificar el tipo de mensaje. Los tipos son:
# - - Error: muestra un error.
# - - Advertencia: muestra una advertencia en la pantalla.
# - - Aviso / Information: muestra información al usuario.
# - - Pregunta: le pregunta algo al usuario. En este caso, también cambian los botones en relación al resto.
# - msg: el mensaje principal que se muestra.
# - info: la información adicional del mensaje.
def mostrarMensaje(title, msg, info):
    # Se crea el messagebox
    window = qtw.QMessageBox()

    # Dependiendo del valor de title, cambia el icono y sus botones correspondientes.
    if title == "Error":
        window.setIcon(qtw.QMessageBox.Icon.Critical)
        window.setStandardButtons(qtw.QMessageBox.StandardButton.Ok)
    elif title == "Advertencia" or title == "Warning":
        window.setIcon(qtw.QMessageBox.Icon.Warning)
        window.setStandardButtons(qtw.QMessageBox.StandardButton.Ok)
    elif title == "Aviso" or title == "Information":
        window.setIcon(qtw.QMessageBox.Icon.Information)
        window.setStandardButtons(qtw.QMessageBox.StandardButton.Ok)
    elif title == "Pregunta" or title == "Question":
        window.setIcon(qtw.QMessageBox.Icon.Warning)
        window.setStandardButtons(
            qtw.QMessageBox.StandardButton.No | qtw.QMessageBox.StandardButton.Yes)
    else:
        print("Error de titulo")
        return
    
    # Se le da el título, el mensaje y la información adicional respectivamente.
    window.setWindowTitle(title)
    window.setText(msg)
    window.setInformativeText(info)

    # La ventana se ejecuta. El return está para obtener la respuesta que el usuario dió en el caso de que algo se le preguntara.
    return window.exec()


# Ventana principal: contiene:
# - la barra superior, que por el momento tiene solo el logo (el ícono y el nombre de la app)
# - una tabla que muestra todos los datos de la tabla herramientas y un boton para mostrar los datos nuevamentee si se modifican.
# - botones para agregar, editar y eliminar campos de la base de datos.
# - botones para ordenar los elementos en orden alfabético segun su nombre, grupo o subgrupo.
# - una barra de búsqueda.
# Esta ventana hereda sus valores de una QMainWindow, funcionando como una ventana principal personalizada.
class GestionHerramientas(qtw.QWidget):
    # Se hace el init en donde se inicializan todos los elementos. 
    def __init__(self):
        # Se inicializa la clase QMainWindow.
        super().__init__()

        # Se crea el fondo de la barra superior
        self.fondo = qtw.QWidget()
        self.fondo.setObjectName("fondo")

        # Se crea un pixmap (algo que guarda una imagen para ponerla en la pantalla), se le da el ícono y se crea el label que tendra la imagen.
        pixmap = qtg.QPixmap(
            f"{os.path.abspath(os.getcwd())}/duraam/images/bitmap.png")
        label1 = qtw.QLabel("")
        label1.setPixmap(pixmap)
        # Esto le da un id a los elementos para poder personalizarlos luego con el archivo .qss.
        label1.setObjectName("icono")

        # Se crea el título (el nombre de la app que va al lado del logo en la barra superior).
        self.titulo = qtw.QLabel("DURAAM")
        self.titulo.setObjectName("titulo")

        # Se crea la tabla.
        self.tabla = qtw.QTableWidget(self)
        self.tabla.setObjectName("tabla")
        # Se establece el número de columnas que va a tener.
        self.tabla.setColumnCount(9)
        # Se crean los títulos de la tabla y se introducen en esta.
        self.campos = ["ID", "Descripción", "En condiciones",
                       "En reparación", "De baja", "Grupo", "SubGrupo", "", ""]
        self.tabla.setHorizontalHeaderLabels(self.campos)
        # Se esconden los números de fila de la tabla que vienen por defecto para evitar confusión con el campo ID.
        self.tabla.verticalHeader().hide()
        # Se muestran los datos en la tabla.
        self.mostrarDatos()

        # Se crean 3 botones de radio y un label para dar contexto.
        self.label2= qtw.QLabel("Ordenar por: ")
        self.radio1 = qtw.QRadioButton("Nombre")
        self.radio2 = qtw.QRadioButton("Grupo")
        self.radio3 = qtw.QRadioButton("Subgrupo")
        # Se le da a los botones de radio la función de mostrar datos en un orden específico.
        self.radio1.toggled.connect(lambda: self.mostrarDatos("Nombre"))
        self.radio2.toggled.connect(lambda: self.mostrarDatos("Grupo"))
        self.radio3.toggled.connect(lambda: self.mostrarDatos("Subgrupo"))

        # Se crea una barra de buscador.
        self.buscar = qtw.QLineEdit()
        self.buscar.setObjectName("buscar")
        # Se le da la función de buscar los datos introducidos.
        self.buscar.returnPressed.connect(lambda: self.mostrarDatos("Buscar"))

        # Se crea el boton de actualizar los campos mostrados en la tabla, por si algún cambio no se hizo bien.
        self.actualizar = qtw.QPushButton("actualizar")
        self.actualizar.setObjectName("actualizar")
        self.actualizar.clicked.connect(
            lambda: self.mostrarDatos())

        # Se crea el boton de agregar herramientas nuevas.
        self.agregar = qtw.QPushButton("Agregar")
        self.agregar.setObjectName("agregar")
        self.agregar.clicked.connect(
            lambda: self.modificarLinea('agregar'))

        # Se crea el layout y se le añaden todos los widgets anteriores.
        layout = qtw.QGridLayout()
        layout.addWidget(self.fondo, 1, 1, 1, 9)
        layout.addWidget(label1, 1, 1)
        layout.addWidget(self.titulo, 1, 2)
        layout.addWidget(self.label2, 3, 2)
        layout.addWidget(self.radio1, 3, 3)
        layout.addWidget(self.radio2, 3, 4)
        layout.addWidget(self.radio3, 3, 5)
        layout.addWidget(self.buscar, 3, 1)
        layout.addWidget(self.actualizar, 2, 1)
        layout.addWidget(self.agregar, 5, 1)
        layout.addWidget(self.tabla, 4, 1, 1, 9)
        layout.setSpacing(0)
        # Se le da el layout al widget central
        self.setLayout(layout)

        # Se crea este atributo para que exista en la pantalla y no se generen errores al abrir la ventana de edición. Explicado más adelante.
        self.edita = None

    # Función editar: muestra un mensaje con un formulario que permite editar los elementos de la tabla.
    # Parametros: tipo: pregunta de que tipo va a ser la edición. Valores posibles:
    # editar: se creará una ventana con un f0rmulario y al enviar los datos se modifican los datos de la fila en la que se pulsó el boton de edición.
    # crear / insertar / None: crea una ventana con un formulario que insertará los datos en la tabla. 
    # Identica a la de editar pero no viene con datos por defecto.
    def modificarLinea(self, tipo):
        # Se hace una referencia a la clase Editar. Esto lo hacemos porque las clases no reconocen las funciones y clases definidas fuera de la propia clase.

        # Se obtiene la posición del boton clickeado: 
        # primero se obtiene cual fue último widget clickeado (en este caso el boton)
        botonClickeado = qtw.QApplication.focusWidget()
        # luego se obtiene la posicion del boton.
        posicion = self.tabla.indexAt(botonClickeado.pos())

        layoutEditar = qtw.QGridLayout()

        self.entry1 = qtw.QLineEdit()
        self.entry2 = qtw.QSpinBox()
        self.entry3 = qtw.QSpinBox()
        self.entry4 = qtw.QSpinBox()
        self.entry5 = qtw.QLineEdit()
        self.entry6 = qtw.QLineEdit()

        self.edita = qtw.QWidget()

        for i in range(1, len(self.campos)):
            label = qtw.QLabel(self.campos[i])
            layoutEditar.addWidget(label, i, 0)
        datos = []
        # Si el tipo es editar, se crea la pantalla de editar.
        if tipo == 'editar':
            # Se crea una lista de datos vacía en la que se introduciran los valores que pasaran por defecto a la ventana.
            
            # Se añaden a la lista los valores de la fila, recorriendo cada celda de la fila. Cell se refiere a la posición de cada celda en la fila.
            for cell in range(0, 9):
                datos.append(posicion.sibling(posicion.row(), cell).data())
            # Se crea la ventana de edición, pasando como parámetros los títulos de los campos de la tabla y los datos por defecto para que se muestren
            # Si se ingresaron datos, se muestran por defecto. Además, se muestra el id.
                # Se les añade a los entries sus valores por defecto.
            self.entry1.setText(datos[1])
            self.entry2.setValue(int(datos[2]))
            self.entry3.setValue(int(datos[3]))
            self.entry4.setValue(int(datos[4]))
            self.entry5.setText(datos[5])
            self.entry6.setText(datos[6])

            # Se añaden los widgets al layout.
        layoutEditar.addWidget(self.entry1, 1, 1)
        layoutEditar.addWidget(self.entry2, 2, 1)
        layoutEditar.addWidget(self.entry3, 3, 1)
        layoutEditar.addWidget(self.entry4, 4, 1)
        layoutEditar.addWidget(self.entry5, 5, 1)
        layoutEditar.addWidget(self.entry6, 6, 1)

            # Se crea el boton de confirmar, y se le da la función de confirmarr.
        confirmar = qtw.QPushButton("Confirmar")
        confirmar.clicked.connect(lambda: self.confirmarr(datos))
        layoutEditar.addWidget(confirmar, 7, 0, 1, 2)

            # Se le da el layout a la ventana.
        self.edita.setLayout(layoutEditar)
        self.edita.show()

    # Función mostrar datos: busca los datos de la tabla de la base de datos y los muestra en la tabla con la que el usuario puede interactuar. Parámetro:
    # - consulta: muestra los datos de forma distinta según el tipo de consulta. Es opcional y, si no se introduce, su valor por defecto es normal. Valores:
    # - - Normal: valor por defecto. Muestra todos los datos de la tabla de la base de datos.
    # - - Buscar: Busca en la tabla de la base de datos las filas que contengan lo buscado.
    # - - Nombre: Muestra todos los datos de la tabla de la base de datos ordenados por su nombre.
    # - - Grupo: Muestra todos los datos de la tabla de la base de datos ordenados por su grupo.
    # - - Subgrupo: Muestra todos los datos de la tabla de la base de datos ordenados por su subgrupo.
    def mostrarDatos(self, consulta="Normal"):
        # Si el tipo de consulta es buscar, muestra las filas que contengan lo buscado en la tabla de la base de datos.
        if consulta=="Buscar":
            # Se crea una lista para pasar por parámetro lo buscado en la query de la tabla de la base de datos.
            busqueda=[]
            # Por cada campo de la tabla, se añade un valor con el que se comparará.
            for i in range(7): 
                # El valor añadido es el texto en la barra de búsqueda.
                busqueda.append(f"%{self.buscar.text()}%")
            #Se hace la query: selecciona cada fila que cumpla con el requisito de que al menos una celda suya contenga el valor pasado por parámetro.
            cur.execute("""
            SELECT * FROM HERRAMIENTAS 
            WHERE ID LIKE ? 
            OR DESC_LARGA LIKE ? 
            OR CANT_CONDICIONES LIKE ? 
            OR CANT_REPARACION LIKE ? 
            OR CANT_BAJA LIKE ? 
            OR ID_GRUPO LIKE ? 
            OR ID_SUBGRUPO LIKE ?""", busqueda)
        # Si el tipo es nombre, se hace una query que selecciona todos los elementos y los ordena por su nombre.
        elif consulta=="Nombre":
            cur.execute('SELECT * FROM HERRAMIENTAS ORDER BY DESC_LARGA')
        # Si el tipo es grupo, se hace una query que selecciona todos los elementos y los ordena por su grupo.
        elif consulta=="Grupo":
            cur.execute('SELECT * FROM HERRAMIENTAS ORDER BY ID_GRUPO')
        # Si el tipo es subgrupo, se hace una query que selecciona todos los elementos y los ordena por su subgrupo.
        elif consulta=="Subgrupo":
            cur.execute('SELECT * FROM HERRAMIENTAS ORDER BY ID_SUBGRUPO')
        # Si el tipo no se cambia o no se introduce, simplemente se seleccionan todos los datos como venian ordenados. 
        elif consulta=="Normal":
            cur.execute('SELECT * FROM HERRAMIENTAS')
        # Si la consulta es otra, se pasa por consola que un boludo escribió la consulta mal :) y termina la ejecución de la función.
        else:
            print("Error crítico: un bobi escribio la consulta mal.")
            return
        # Se guarda la consulta en una variable.
        query = cur.fetchall()
        # Se establece la cantidad de filas que va a tener la tabla
        self.tabla.setRowCount(len(query))
        # Bucle: por cada fila de la consulta obtenida, se guarda su id y se genera otro bucle que inserta todos los datos en la fila de la tabla de la ui.
        # Además, se insertan dos botones al costado de cada tabla: uno para editarla y otro para eliminarla.
        for i in range(len(query)):

            # Bucle: se introduce en cada celda el elemento correspondiente de la fila.
            for j in range(len(query[i])):
                self.tabla.setItem(i, j, qtw.QTableWidgetItem(str(query[i][j])))
            
            # Se crea el boton de editar, se le da la función de editar y se lo introduce después de introducir los datos.
            botonEditar = qtw.QPushButton("Editar")
            botonEditar.clicked.connect(lambda: self.modificarLinea('editar'))
            self.tabla.setCellWidget(i, 7, botonEditar)

            # Se crea el boton de eliminar, se le da la función de eliminar la tabla con su id correspondiente y se introduce el boton al final de la fila.
            botonEliminar = qtw.QPushButton("Eliminar")
            botonEliminar.clicked.connect(lambda: self.eliminar(query[i][0]))
            self.tabla.setCellWidget(i, 8, botonEliminar)

    # Función eliminar: elimina la fila de la tabla de la base de datos y de la tabla de la ui. Parámetro:
    # - idd: el id de la fila que se va a eliminar.
    def eliminar(self, idd):
        # se obtiene la función definida fuera de la clase.
        global mostrarMensaje
        # se le pregunta al usuario si desea eliminar la fila.
        resp = mostrarMensaje('Pregunta', 'Advertencia',
                              '¿Está seguro que desea eliminar estos datos?')
        # si pulsó el boton de sí:
        if resp == qtw.QMessageBox.StandardButton.Yes:
            # elimina la fila con el id correspondiente de la tabla de la base de datos.
            cur.execute('DELETE FROM HERRAMIENTAS WHERE ID=?', (idd,))
            con.commit()

            #elimina la fila de la tabla de la ui.
            boton = qtw.QApplication.focusWidget()
            i = self.tabla.indexAt(boton.pos())
            self.tabla.removeRow(i.row())

    # Función: closeEvent: funcion de qtmainwindow que se ejecuta automáticamente cuando se cierra la ventana principal. 
    # Cuando esto ocurra, también cerrara las demás ventanas que hayan quedado abiertas.
    def closeEvent(self, event):
        # Si hay una ventana de edición abierta, la cierra. 
        # Por esto estaba en el init la variable inicializada con None, porque si no se inicializa no existe y al no existir tira error.
        if self.edita:
            self.edita.close()
    
    def confirmarr(self, datos):
        # Se hace una referencia a la función de mensajes fuera de la clase y a la ventana principal.
        global mostrarMensaje

        # Si habían datos por defecto, es decir, si se quería editar una fila, se edita la fila en la base de datos y muestra el mensaje.
        if datos:
            # Se actualiza la fila con su id correspondiente en la tabla de la base de datos.
            cur.execute("""
            UPDATE HERRAMIENTAS 
            SET DESC_LARGA=?, CANT_CONDICIONES=?, CANT_REPARACION=?, CANT_BAJA=?,ID_GRUPO=?,ID_SUBGRUPO=? WHERE ID=?""", (
                self.entry1.text(), self.entry2.value(), self.entry3.value(
                ), self.entry4.value(), self.entry5.text(), self.entry6.text(), datos[0],
            ))
            con.commit()
            # Se muestra el mensaje exitoso.
            mostrarMensaje("Information", "Aviso",
                           "Se ha actualizado la herramienta.")
        else:
            # Se inserta la fila en la tabla de la base de datos.
            cur.execute("INSERT INTO HERRAMIENTAS VALUES(NULL, ?, ?, ?, ?, ?, ?) ", (
                self.entry1.text(), self.entry2.value(), self.entry3.value(
                ), self.entry4.value(), self.entry5.text(), self.entry6.text(),
            ))
            con.commit()

            mostrarMensaje("Information", "Aviso",
                           "Se ha ingresado una herramienta.")
        self.mostrarDatos()




