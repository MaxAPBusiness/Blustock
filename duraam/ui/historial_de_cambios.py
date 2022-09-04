# gestion_herramientas.py: la gestión de herramientas. Contiene una tabla, que muestra 
#                          la tabla de la base de datos; una barra de buscador; botones para 
#                          ordenar alfabéticamente la tabla por nombre, grupo y subgrupo de 
#                          herramientas; botones para editar y eliminar los datos; un botón
#                          para agregar herramientas. 
#                          Para editar y agregar, aparece un submenú con los datos a introducir.

# Se importan las librerías.
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import sqlite3 as db
import os

# Se importa la función mostrarMensaje.
from mostrar_mensaje import mostrarMensaje

# Se hace una conexión a la base de datos
os.chdir(f"{os.path.abspath(__file__)}/../../..")
con = db.Connection(f"{os.path.abspath(os.getcwd())}/duraam/db/duraam.sqlite3")
cur=con.cursor()


# clase GestiónHerramientas: ya explicada. Es un widget que después se ensambla en un stackwidget en main.py.
class HistorialDeCambios(qtw.QWidget):
    # Se hace el init en donde se inicializan todos los elementos. 
    def __init__(self):
        # Se inicializa la clase QWidget.
        super().__init__()

        # Se crea el título.
        self.titulo=qtw.QLabel("Historial de cambios")
        self.titulo.setObjectName("titulo")

        # Se crea la tabla.
        self.tabla = qtw.QTableWidget(self)
        self.tabla.setObjectName("tabla")

        # Se crean los títulos de las columnas de la tabla y se introducen en esta.
        self.campos = ["Nombre y apellido", "Usuario", "Fecha y hora", "Descripción del cambio"]      
                                
        # Se establece el número de columnas que va a tener. 
        self.tabla.setColumnCount(len(self.campos))
        # Se introducen los títulos en la tabla.
        self.tabla.setHorizontalHeaderLabels(self.campos)

        # Se esconden los números de fila de la tabla que vienen por defecto para evitar confusión con el campo ID.
        self.tabla.verticalHeader().hide()
        # Se cambia el ancho de las dos últimas columnas, porque son las que van a tener los botones de editar y eliminar.
        self.tabla.setColumnWidth(2, 400)

        # Se crea una barra de búsqueda
        self.buscar = qtw.QLineEdit()
        self.buscar.setObjectName("buscar")
        # Se introduce un botón a la derecha que permite borrar la busqueda con un click.
        self.buscar.setClearButtonEnabled(True)
        # Se le pone el texto por defecto a la barra de búsqueda
        self.buscar.setPlaceholderText("Buscar...")
        # Se importa el ícono de lupa para la barra.
        lupa=qtg.QPixmap(f"{os.path.abspath(os.getcwd())}/duraam/images/buscar.png")
        # Se crea un label que va a contener el ícono.
        icono=qtw.QLabel()
        icono.setObjectName("lupa")
        icono.setPixmap(lupa)

        # Se le da la función de buscar los datos introducidos.
        self.buscar.returnPressed.connect(lambda: self.mostrarDatos("Listado"))
        # Se crean 3 botones de radio y un label para dar contexto.
        self.label2= qtw.QLabel("Ordenar por: ")
        self.grupo1 = qtw.QButtonGroup(self)
        self.radio1 = qtw.QRadioButton("Usuario")
        self.radio2 = qtw.QRadioButton("Fecha")
        self.radio3 = qtw.QRadioButton("Tipo")
        self.radio4 = qtw.QRadioButton("Tabla")

        self.radio1.setObjectName("Radio1")
        self.radio2.setObjectName("Radio2")
        self.radio3.setObjectName("Radio3")
        self.radio3.setObjectName("Radio3")
        # Se le da a los botones de radio la función de mostrar datos en un orden específico.
        self.radio1.toggled.connect(lambda:self.mostrarDatos("Listado", 1))
        self.radio2.toggled.connect(lambda:self.mostrarDatos("Listado", 2))
        self.radio3.toggled.connect(lambda:self.mostrarDatos("Listado", 3))
        self.radio4.toggled.connect(lambda:self.mostrarDatos("Listado", 4))

        self.label3=qtw.QLabel("Usuario: ")
        self.usuario=qtw.QComboBox()

        self.label4=qtw.QLabel("Desde: ")
        self.date1=qtw.QDateEdit()
        self.date1.editingFinished.connect(lambda:self.mostrarDatos("Listado"))

        self.label5=qtw.QLabel("Hasta: ")
        self.date2=qtw.QDateEdit()
        self.date2.editingFinished.connect(lambda:self.mostrarDatos("Listado"))
        
        self.label6=qtw.QLabel("Tipo: ")
        self.tipo=qtw.QComboBox()
        self.tipo.addItem("Todos")
        self.tipo.addItem("Inserción")
        self.tipo.addItem("Edición")
        self.tipo.addItem("Eliminación")
        self.tipo.addItem("Pase anual")
        self.tipo.addItem("Pase histórico individual")
        self.tipo.addItem("Pase histórico grupal")
        self.tipo.addItem("Verificación de solicitud")
        self.tipo.addItem("Rechazo de solicitud")
        self.tipo.addItem("Ascenso")
        self.tipo.addItem("Descenso")
        self.tipo.currentIndexChanged.connect(lambda:self.mostrarDatos("Listado"))

        self.label7=qtw.QLabel("Tabla: ")
        self.seleccionarTabla=qtw.QComboBox()
        self.tipo.addItem("Todas")
        self.seleccionarTabla.addItem("Herramientas")
        self.seleccionarTabla.addItem("Movimientos de herramientas")
        self.seleccionarTabla.addItem("Turnos del pañol")
        self.seleccionarTabla.addItem("Alumnos")
        self.seleccionarTabla.addItem("Profesores")
        self.seleccionarTabla.addItem("Grupos")
        self.seleccionarTabla.addItem("Subgrupos")
        self.seleccionarTabla.addItem("Alumnos históricos")
        self.seleccionarTabla.addItem("Profesores históricos")
        self.seleccionarTabla.addItem("Usuarios")
        self.seleccionarTabla.addItem("Administradores")
        self.seleccionarTabla.currentIndexChanged.connect(lambda:self.mostrarDatos("Listado"))

        self.container1=qtw.QWidget()
        self.container1Layout=qtw.QGridLayout()
        self.container2=qtw.QWidget()
        self.container2Layout=qtw.QHBoxLayout()


        # Se crea el layout y se le añaden todos los widgets anteriores.
        layout = qtw.QVBoxLayout()
        layout.addWidget(self.titulo)

        self.container1Layout.addWidget(self.buscar, 0, 0)
        self.container1Layout.addWidget(icono, 0, 0)
        self.container1Layout.addWidget(self.label2, 0, 1)
        self.container1Layout.addWidget(self.radio1, 0, 2)
        self.container1Layout.addWidget(self.radio2, 0, 3)
        self.container1Layout.addWidget(self.radio3, 0, 4)
        self.container1Layout.addWidget(self.radio4, 0, 5)
        self.container1.setLayout(self.container1Layout)
        layout.addWidget(self.container1)

        self.container2Layout.addWidget(self.label3)
        self.container2Layout.addWidget(self.usuario)
        self.container2Layout.addWidget(self.label4)
        self.container2Layout.addWidget(self.date1)
        self.container2Layout.addWidget(self.label5)
        self.container2Layout.addWidget(self.date2)
        self.container2Layout.addWidget(self.label6)
        self.container2Layout.addWidget(self.tipo)
        self.container2Layout.addWidget(self.label7)
        self.container2Layout.addWidget(self.tabla)
        self.container2.setLayout(self.container2Layout)
        layout.addWidget(self.container2)

        layout.addWidget(self.tabla)

        # Se muestran los datos.
        self.mostrarDatos()
        self.setLayout(layout)



# Función mostrar datos: busca los datos de la tabla de la base de datos y los muestra en la tabla con la que el usuario puede interactuar. Parámetro:
    # - consulta: muestra los datos de forma distinta según el tipo de consulta. Es opcional y, si no se introduce, su valor por defecto es normal. Valores:
    # - - Normal: valor por defecto. Muestra todos los datos de la tabla de la base de datos.
    # - - Buscar: Busca en la tabla de la base de datos las filas que contengan lo buscado.
    # - - Nombre: Muestra todos los datos de la tabla de la base de datos ordenados por su nombre.
    # - - Grupo: Muestra todos los datos de la tabla de la base de datos ordenados por su grupo.
    # - - Subgrupo: Muestra todos los datos de la tabla de la base de datos ordenados por su subgrupo.
    def mostrarDatos(self, consulta="Normal", orden=""):
         # Si el tipo de consulta es buscar, muestra las filas que contengan lo buscado en la tabla de la base de datos.
        if consulta=="Listado":
            #Se hace la query: selecciona cada fila que cumpla con el requisito de que al menos una celda suya contenga el valor pasado por parámetro.
            if self.usuario.currentText() == "Todos":
                usuario=""
            else:
                usuario=self.usuario.currentText()
            
            if self.tipo.currentText() == "Todos":
                tipo=""
            else:
                tipo=self.tipo.currentText()
            
            if self.tabla.currentText() == "Todas":
                tabla=""
            else:
                tabla=self.tabla.currentText()
            
            ordenStatement=""

            if orden:
                if orden==1:
                    ordenStatement="ORDER BY H.DESC_LARGA"
                if orden==2:
                    ordenStatement="ORDER BY NOMBRE"
                if orden==3:
                    ordenStatement="ORDER BY M.FECHA"
 

            cur.execute(f"""
            SELECT (CASE WHEN H.ROL = 0 THEN U.NOMBRE_APELLIDO ELSE A.NOMBRE_APELLIDO END) AS NOMBRE,
            (CASE WHEN H.ROL = 0 THEN U.USUARIO ELSE A.USUARIO END) AS USUARIO,
            H.FECHA_HORA, H.TIPO, H.TABLA, H.ID_FILA, H.DATOS_VIEJOS, H.DATOS_NUEVOS
            FROM HISTORIAL_DE_CAMBIOS H
            LEFT JOIN USUARIOS U
            ON U.ID = H.ID_USUARIO
            LEFT JOIN ADMINISTRADORES A
            ON A.ID = H.ID_USUARIO
            WHERE (NOMBRE LIKE ? 
            OR USUARIO LIKE ? 
            OR H.FECHA_HORA LIKE ?
            OR H.TIPO LIKE ? 
            OR H.TABLA LIKE ? 
            OR H.ID_FILA LIKE ? 
            OR H.DATOS_VIEJOS LIKE ?
            OR H.DATOS_NUEVOS LIKE ?)
            AND USUARIO LIKE ?
            AND H.TIPO LIKE ?
            AND H.TABLA LIKE ?
            {ordenStatement}
            """, (f"%{self.buscar.text()}%", f"%{self.buscar.text()}%", f"%{self.buscar.text()}%", f"%{self.buscar.text()}%", f"%{self.buscar.text()}%", 
                    f"%{self.buscar.text()}%", f"%{self.buscar.text()}%", f"%{self.buscar.text()}%", f"%{usuario}%", f"%{tipo}%", f"%{tabla}%",))
            
            query = []
            fetch=cur.fetchall()
            for i in fetch:
                fecha = qtc.QDate.fromString(i[4], "dd/MM/yyyy")
                if fecha >= self.date1.date() and fecha <= self.date2.date():
                    query.append(i)
            

        # Si el tipo no se cambia o no se introduce, simplemente se seleccionan todos los datos como venian ordenados. 
        elif consulta=="Normal":
            cur.execute('''
            SELECT (CASE WHEN H.ROL = 0 THEN U.NOMBRE_APELLIDO ELSE A.NOMBRE_APELLIDO END) AS NOMBRE,
            (CASE WHEN H.ROL = 0 THEN U.USUARIO ELSE A.USUARIO END) AS USUARIO,
            H.FECHA_HORA, H.TIPO, H.TABLA, H.ID_FILA, H.DATOS_VIEJOS, H.DATOS_NUEVOS
            FROM HISTORIAL_DE_CAMBIOS H
            LEFT JOIN USUARIOS U
            ON U.ID = H.ID_USUARIO
            LEFT JOIN ADMINISTRADORES A
            ON A.ID = H.ID_USUARIO
            ''')
            # Se guarda la consulta en una variable.
            query = cur.fetchall()

        # Se establece la cantidad de filas que va a tener la tabla
        self.tabla.setRowCount(len(query))
        # Bucle: por cada fila de la consulta obtenida, se guarda su id y se genera otro bucle que inserta todos los datos en la fila de la tabla de la ui.
        # Además, se insertan dos botones al costado de cada tabla: uno para editarla y otro para eliminarla.
        for i in range(len(query)):
            self.tabla.setItem(i, 0, qtw.QTableWidgetItem(str(query[i][0])))
            self.tabla.setItem(i, 1, qtw.QTableWidgetItem(str(query[i][1])))
            self.tabla.setItem(i, 2, qtw.QTableWidgetItem(str(query[i][2])))
            if query[i][3]=="Inserción":
                if query[i][5]:
                    textoId=f" de id {query[i][5]}"
                else:
                    textoId=""
                descripcion=f"Agregó a la tabla {query[i][4]} la fila{textoId} con los datos {query[i][7]}."
                self.tabla.setItem(i, 3, qtw.QTableWidgetItem(descripcion))

            elif query[i][3]=="Edición":
                if query[i][5]:
                    textoId=f" de id {query[i][5]}"
                else:
                    textoId=""
                descripcion=f"Editó la fila{textoId} de la tabla {query[i][4]}, reemplazando los datos{query[i][6]} con los datos {query[i][7]}."
                self.tabla.setItem(i, 3, qtw.QTableWidgetItem(descripcion))

            elif query[i][3]=="Eliminación":
                if query[i][5]:
                    textoId=f" de id {query[i][5]}"
                else:
                    textoId=""
                descripcion=f"Eliminó de la tabla {query[i][4]} la fila{textoId} que tenía los datos {query[i][6]}."
                self.tabla.setItem(i, 3, qtw.QTableWidgetItem(descripcion))
            
            elif query[i][3]=="Pase Anual":
                descripcion=f"Realizó el pase anual de los alumnos de id: {query[i][6]}."
                self.tabla.setItem(i, 3, qtw.QTableWidgetItem(descripcion))
            
            elif query[i][3]=="Pase histórico individual":
                descripcion=f"Realizó el pase histórico individual de {query[i][4]} de la persona de id: {query[i][5]}."
                self.tabla.setItem(i, 3, qtw.QTableWidgetItem(descripcion))
            
            elif query[i][3]=="Pase histórico grupal":
                descripcion=f"Realizó el pase histórico grupal de {query[i][4]} de las personas de id: {query[i][5]}."
                self.tabla.setItem(i, 3, qtw.QTableWidgetItem(descripcion))

            elif query[i][3]=="Verificación de solicitud":
                descripcion=f"Aceptó la solicitud del usuario cuyos datos son: {query[i][7]}."
                self.tabla.setItem(i, 3, qtw.QTableWidgetItem(descripcion))
            
            elif query[i][3]=="Rechazo de solicitud":
                descripcion=f"Rechazó la solicitud del usuario cuyos datos eran: {query[i][6]}"
                self.tabla.setItem(i, 3, qtw.QTableWidgetItem(descripcion))

            elif query[i][3]=="Ascenso":
                descripcion=f"Ascendió al usuario con los datos: {query[i][7]} a administrador."
                self.tabla.setItem(i, 3, qtw.QTableWidgetItem(descripcion))
            
            elif query[i][3]=="Descenso":
                descripcion=f"Descendió al administrador con los datos: {query[i][7]} a usuario."
                self.tabla.setItem(i, 3, qtw.QTableWidgetItem(descripcion))
        
            self.tabla.setRowHeight(i, 35)