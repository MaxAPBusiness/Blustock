"""Este módulo contiene una clase para gestionar el envío de datos
entre la base de datos y la IU.

Clases
------
    DAL():
"""
import os
from db.bdd import bdd
from ui.presets.popup import PopUp
from datetime import datetime
import sqlite3

class DAL():
    """Esta clase contiene métodos que gestionan el envío de datos
    entre la base de datos y la IU.
    
    Métodos
    ---------
        obtenerDatos(self, tabla: str, busqueda: str, 
        filtrosExtra: list | tuple | dict | None = None) -> list:
            Obtiene datos de la base de datos y los devuelve en forma
            de lista.
    """
    def obtenerDatos(self, tabla: str, busqueda: str | None = None, 
        filtrosExtra: list | tuple | None = None) -> list:
        """Este método obtiene y devuelve datos de la base de datos

        Parámetros
        ----------
            tabla: str
                La tabla de la base de datos de la que se obtendrán los
                datos.
            busqueda: str
                El texto ingresado en la barra de búsqueda de la ui,
                que se usará como filtro de los datos.
            filtrosExtra: list | tuple | dict | None = None
                Un objeto iterable (lista, tupla o diccionario) que 
                contendrá todos los filtros extra que se quieran usar
                para filtrar la obtención de los datos.
                Default: None.
        
        Devuelve
        --------
            list: los datos obtenidos organizados en una lista.
        """
        # Abriendo el archivo sql con la consulta usando la tabla
        # pedida...
        filtro = []
        
        if filtrosExtra:
            cantFiltrosExtra=len(filtrosExtra)
            # Insertamos los filtros extra en la lista de filtros
            for filtroExtra in filtrosExtra:
                if filtroExtra:
                    filtro.append(filtroExtra)
                else:
                    filtro.append('%%')
        else:
            cantFiltrosExtra=0
            
        with open(f"dal{os.sep}queries{os.sep}{tabla}.sql", 'r') as queryText:
            # Obtenemos y guardamos el código sql como texto
            query=queryText.read()
        # Cada "?" en el código sql indica que usaremos un dato de
        # python. Para aplicar la búsqueda en la obtención
        # correctamente, debemos ver si algún campo de la tabla 
        # contiene lo buscado. Por eso, por cada campo que queramos
        # comparar con la búsqeda debe haber un "?". Tenemos que
        # aportar una lista o tupla que contenga un elemento de
        # texto por cada "?". Por ejemplo, si queremos consultar
        # por 6 campos por cada fila, tendremos que pasar una lista
        # con 6 elementos iguales, todos siendo el texto de
        # búsqueda. El bucle de abajo mira cuantos "?" tiene la 
        # consulta y agrega a la lista filtro (que se va a pasar
        # como filtro en la obtención) la cantidad de textos de 
        # búsqueda adecuados. NOTA: Como también puede haber
        # filtros extra, y va a haber un "?" por cada filtro extra,
        # la cantidad de comparaciones de búsqueda se obtiene
        # contando los "?" y restando la cantidad de filtros extra.
        for i in range(query.count('?')-cantFiltrosExtra):
            filtro.append(f"%{busqueda}%")
                # Consulta los datos y los devuelve.
        datos = bdd.cur.execute(query, filtro).fetchall()
        return [["-" if cellData == None else cellData for cellData in rowData] for rowData in datos]

    def insertarHistorial(self, usuario: int, tipo: str, gestion: str,
                          fila: int, listaDatosViejos: list | None = None,
                          listaDatosNuevos: list | None = None):
        """Este método inserta información sobre cambios realizados a
        la base de datos en la tabla historial.

        Parámetros
        ----------
            usuario: int
                El id del usuario que realizó el cambio.
            tipo: str
                El tipo de cambio.
            tabla: str
                La tabla donde se realizó el cambio.
            fila: int
                El número de la fila que se modificó.
            datosViejos: str | None = None
                Los datos que fueron eliminados o reemplazados.
                Default: None
            datosNuevos: str | None = None
                Los datos que se añadieron o reemplazaron otros datos.
                Default: None
        """
        idTipo=bdd.cur.execute('SELECT id FROM tipos_cambio WHERE descripcion=?', (tipo,)).fetchone()[0]
        idGestion=bdd.cur.execute('SELECT id FROM gestiones WHERE descripcion=?', (gestion,)).fetchone()[0]
        if not idTipo or not idGestion:
            info="ERROR DE PROGRAMACION: SE PASARON DATOS EQUIVOCADOS EN LA LLAMADA AL HISTORIAL"
            return PopUp('Error', info).exec()
        if listaDatosViejos:
            datosViejos=''
            for datoViejo in listaDatosViejos:
                datosViejos += f'{datoViejo};'
        else:
            datosViejos=None
        if listaDatosNuevos:
            datosNuevos=''
            for datoNuevo in listaDatosNuevos:
                datosNuevos += f'{datoNuevo};'
        else:
            datosNuevos=None
        
        idUsuario=bdd.cur.execute('SELECT id FROM personal WHERE dni = ?', (usuario,)).fetchone()[0]
        datos=(idUsuario, datetime.now().strftime("%Y/%m/%d %H:%M:%S"), idTipo, idGestion, fila, datosViejos, datosNuevos,)
        bdd.cur.execute('INSERT INTO historial VALUES(?,?,?,?,?,?,?)', datos)
        bdd.con.commit()
    
    def verifElimStock(self, idd: int) -> bool:
        """Esta función verifica si la PK de una fila de la tabla stock
        está relacionada con otras tablas.
        
        Parámetros
        ----------
            idd: int
                El id de la fila que queremos verificar
        
        Devuelve
        --------
            bool: si encontró o no una relación.
        """
        movsRel=bdd.cur.execute(
            "SELECT * FROM movimientos WHERE id_elem = ?", (idd,)).fetchone()
        repRel=bdd.cur.execute(
            "SELECT * FROM reparaciones WHERE id_herramienta = ?", (idd,)).fetchone()
        if movsRel or repRel:
            return True
        else:
            return False
    
    def verifElimSubgrupos(self, idd: int) -> bool:
        """Este método verifica si la PK de una fila de la tabla
        subgrupos está relacionada con otras tablas.
        
        Parámetros
        ----------
            idd: int
                El id de la fila que queremos verificar.
        
        Devuelve
        --------
            bool: si encontró o no una relación.
        """
        stockRel=bdd.cur.execute(
            "SELECT * FROM stock WHERE id_subgrupo = ?", (idd,)).fetchone()
        if stockRel:
            return True
        else:
            return False
    
    def verifElimGrupos(self, idd: int) -> bool:
        """Este método verifica si la PK de una fila de la tabla grupos
        está relacionada con otras tablas.
        
        Parámetros
        ----------
            idd: int
                El id de la fila que queremos verificar.
        
        Devuelve
        --------
            bool: si encontró o no una relación.
        """
        subgruposRel=bdd.cur.execute(
            "SELECT * FROM subgrupos WHERE id_grupo = ?", (idd,)).fetchone()
        if subgruposRel:
            return True
        else:
            return False
    
    def verifElimClases(self, idd: int) -> bool:
        """Este método verifica si la PK de una fila de la tabla
        clases está relacionada con otras tablas.
        
        Parámetros
        ----------
            idd: int
                El id de la fila que queremos verificar.
        
        Devuelve
        --------
            bool: si encontró o no una relación.
        """
        personalRel=bdd.cur.execute(
            "SELECT * FROM personal WHERE id_clase = ?", (idd,)).fetchone()
        if personalRel:
            return True
        else:
            return False
    
    def verifElimUbi(self, idd: int) -> bool:
        """Este método verifica si la PK de una fila de la tabla
        ubicaciones está relacionada con otras tablas.
        
        Parámetros
        ----------
            idd: int
                El id de la fila que queremos verificar
        
        Devuelve
        --------
            bool: si encontró o no una relación.
        """
        turnosRel=bdd.cur.execute(
            "SELECT * FROM turnos WHERE id_ubi = ?", (idd,)).fetchone()
        stockRel=bdd.cur.execute(
            "SELECT * FROM stock WHERE id_ubi = ?", (idd,)).fetchone()
        if turnosRel or stockRel:
            return True
        else:
            return False
    
    def verifElimAlumnos(self, idd: int) -> bool:
        """Este método verifica si la PK de una fila (que represente un
        alumno) de la tabla personal está relacionada con otras tablas.
        
        Parámetros
        ----------
            idd: int
                El id de la fila que queremos verificar
        
        Devuelve
        --------
            bool: si encontró o no una relación.
        """
        turnosRel=bdd.cur.execute(
            "SELECT * FROM turnos WHERE id_panolero = ?", (idd,)).fetchone()
        movsRel=bdd.cur.execute(
            "SELECT * FROM movimientos WHERE id_persona = ?", (idd,)).fetchone()
        if turnosRel or movsRel:
            return True
        else:
            return False
    
    def verifElimUsuario(self, idd: int) -> bool:
        """Este método verifica si la PK de una fila (que represente un
        usuario) de la tabla personal está relacionada con otras
        tablas.
        
        Parámetros
        ----------
            idd: int
                El id de la fila que queremos verificar.
        
        Devuelve
        --------
            bool: si encontró o no una relación.
        """
        turnosPanoleroRel=bdd.cur.execute(
            "SELECT * FROM turnos WHERE id_panolero = ?", (idd,)).fetchone()
        turnosProfIngRel=bdd.cur.execute(
            "SELECT * FROM turnos WHERE id_prof_ing = ?", (idd,)).fetchone()
        turnosProfEgRel=bdd.cur.execute(
            "SELECT * FROM turnos WHERE id_prof_egr = ?", (idd,)).fetchone()
        movsRel=bdd.cur.execute(
            "SELECT * FROM movimientos WHERE id_persona = ?", (idd,)).fetchone()
        repRel=bdd.cur.execute(
            "SELECT * FROM reparaciones WHERE id_usuario = ?", (idd,)).fetchone()
        if (turnosPanoleroRel or turnosProfIngRel or turnosProfEgRel
            or movsRel or repRel):
            return True
        else:
            return False
    
    def verifElimOtroPersonal(self, idd: int) -> bool:
        """Esta función verifica si la PK de una fila (que represente 
        personal que no sea alumno ni usuario) de la tabla personal
        está relacionada con otras tablas.
        
        Parámetros
        ----------
            idd: int
                El id de la fila que queremos verificar
        
        Devuelve
        --------
            bool: si encontró o no una relación.
        """
        movsRel=bdd.cur.execute(
            "SELECT * FROM movimientos WHERE id_persona = ?", (idd,)).fetchone()
        if movsRel:
            return True
        else:
            return False
    
    def eliminarDatos(self, tabla: str, idd: str):
        """Esta función elimina datos de una tabla.
        
        Parámetros
        ----------
            tabla: str
                La tabla en la que los datos se van a eliminar.
            idd: str
                El id de la fila que se va a eliminar.
        """
        bdd.cur.execute(f"DELETE FROM {tabla} WHERE id = ?", (idd,))
        bdd.con.commit()
    
    def cargarPlanilla(self, datos: list, actualizarCursos: bool):
        for n, fila in enumerate(datos):
            if not actualizarCursos:
                datos[n][1]=f'{fila[1][0]}{fila[1][-1]}'
                
            if isinstance(fila[2], int):
                if fila[2] > 10**8:
                    info = 'Un dni proporcionado en la planilla es demasiado largo. Revise los dni de la plantilla e intente nuevamente.'
                    return PopUp('Error', info).exec()
                continue
            elif isinstance(fila[2], str):
                dni = ''.join(fila[2].split("."))
                if dni.isnumeric():
                    dni = int(dni)
                    if dni > 10**8:
                        info = 'Un dni proporcionado en la planilla es demasiado largo. Revise los dni de la plantilla e intente nuevamente.'
                        return PopUp('Error', info).exec()
                    datos[n][2] = dni
                    continue
            info = 'Un dni proporcionado en la planilla no es válido. Revise los dni de la plantilla e intente nuevamente.'
            return PopUp('Error', info).exec()
                
        cursos=set([fila[1] for fila in datos])
        for curso in cursos:
            try:
                bdd.cur.execute('INSERT INTO clases VALUES(NULL, ?, 1)', (curso,))
            except sqlite3.IntegrityError:
                pass
        
        bdd.cur.execute('''CREATE TABLE alumnos_nuevos(
                           nombre_apellido VARCHAR(100) NOT NULL,
                           id_curso INTEGER NOT NULL,
                           dni INTEGER UNIQUE NOT NULL);''')
        for fila in datos:
            idCurso=bdd.cur.execute('SELECT id FROM clases WHERE descripcion LIKE ?', (fila[1],)).fetchone()[0]
            try:
                bdd.cur.execute('INSERT INTO alumnos_nuevos VALUES(?, ?, ?)',
                                (fila[0], idCurso, fila[2],))
            except sqlite3.IntegrityError:
                pass
                
        with open(f"dal{os.sep}queries{os.sep}merge_alumnos.sql", 'r') as queryText:
            sql=queryText.read()
        mergeSelect = bdd.cur.execute(sql).fetchall()
        for mergeRow in mergeSelect:
            if mergeRow[2] is None:
                bdd.cur.execute('''
                    UPDATE personal SET id_clase = (
                        SELECT id FROM clases
                        WHERE descripcion LIKE 'Egresado'
                    ) WHERE dni = ?''', (mergeRow[1],))
            else:
                if mergeRow[0] is None:
                    bdd.cur.execute('''
                        INSERT INTO personal VALUES (NULL, ?, ?, (
                            SELECT id FROM clases WHERE descripcion = ?
                        ), NULL, NULL)''', (mergeRow[2], mergeRow[1], mergeRow[3],))
                else:
                    bdd.cur.execute('''
                        UPDATE personal SET nombre_apellido = ?, id_clase = (
                            SELECT id FROM clases WHERE descripcion = ?
                        ) WHERE dni = ?''', (mergeRow[2], mergeRow[3], mergeRow[1],))
        egresados=bdd.cur.execute('''SELECT * FROM personal WHERE id_clase IN (
                SELECT id FROM clases WHERE descripcion='Egresado');''').fetchall()
        for egresado in egresados:
            if not self.verifElimAlumnos(egresado[0]):
                bdd.cur.execute('DELETE FROM personal WHERE id=?', (egresado[0],))
        bdd.cur.execute('DROP TABLE alumnos_nuevos')
        bdd.con.commit()


# Se crea el objeto que será usado por los demás módulos para acceder
# a las funciones.
dal=DAL()