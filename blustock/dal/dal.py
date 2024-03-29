"""Este módulo contiene una clase para gestionar el envío de datos
entre la base de datos y la IU.

Clases
------
    DAL():
        Contiene métodos que gestionan el envío de datos entre la base
        de datos y la IU.
"""
import os
from db.bdd import bdd
from ui.presets.popup import PopUp
from datetime import datetime
import sqlite3
from PyQt6 import QtWidgets

class DAL():
    """Esta clase contiene métodos que gestionan el envío de datos
    entre la base de datos y la IU.
    
    Métodos
    ---------
        obtenerDatos(self, tabla: str, busqueda: str, 
        filtrosExtra: list | tuple | dict | None = None) -> list:
            Obtiene datos de la base de datos y los devuelve en forma
            de lista.
        
        insertarHistorial(self, usuario: int, tipo: str, gestion: str,
                          fila: int,
                          listaDatosViejos: list | None = None,
                          listaDatosNuevos: list | None = None):
            Inserta información sobre cambios realizados a la base de
            datos en la tabla historial.
        
        verifElimStock(self, idd: int) -> bool:
            Verifica si una fila de la tabla de la gestión stock tiene
            relaciones en la base de datos.
        
        verifElimStock(self, idd: int) -> bool:
            Verifica si una fila de la tabla de la gestión stock tiene
            relaciones en la base de datos.
        
        verifElimSubgrupos(self, idd: int) -> bool:
            Verifica si una fila de la tabla de la gestión subgrupos
            tiene relaciones en la base de datos.
        
        verifElimGrupos(self, idd: int) -> bool:
            Verifica si una fila de la tabla de la gestión grupos tiene
            relaciones en la base de datos.
        
        verifElimAlumnos(self, idd: int) -> bool:
            Verifica si una fila de la tabla de la gestión alumnos
            tiene relaciones en la base de datos.
        
        verifElimOtroPersonal(self, idd: int) -> bool:
            Verifica si una fila de la tabla de la gestión otro
            personal tiene relaciones en la base de datos.
        
        verifElimClases(self, idd: int) -> bool:
            Verifica si una fila de la tabla de la gestión clases tiene
            relaciones en la base de datos.
        
        verifElimUsuarios(self, idd: int) -> bool:
            Verifica si una fila de la tabla de la gestión usuarios
            tiene relaciones en la base de datos.
        
        verifElimUbi(self, idd: int) -> bool:
            Verifica si una fila de la tabla de la gestión ubicaciones
            tiene relaciones en la base de datos.
        
        eliminarDatos(self, tabla: str, idd: str):
            Elimina datos de una tabla.
        
        cargarPlanillaAlumnos(self, datos: list,
                              actualizarCursos: bool):
            Carga los datos de una lista en la base de datos de alumnos
        
        saveStock(self, tabla: QtWidgets.QTableWidget, row: int,
                  user: int, datos: list | None = None) -> bool:
            Guarda los cambios de la gestión stock.
        
        saveSubgrupos(self, tabla: QtWidgets.QTableWidget, row: int,
                  user: int, datos: list | None = None) -> bool:
            Guarda los cambios de la gestión subgrupos.
        
        saveGrupos(self, tabla: QtWidgets.QTableWidget, row: int,
                  user: int, datos: list | None = None) -> bool:
            Guarda los cambios de la gestión grupos.
        
        saveAlumnos(self, tabla: QtWidgets.QTableWidget, row: int,
                  user: int, datos: list | None = None) -> bool:
            Guarda los cambios de la gestión alumnos.
        
        saveOtroPersonal(self, tabla: QtWidgets.QTableWidget, row: int,
                  user: int, datos: list | None = None) -> bool:
            Guarda los cambios de la gestión otropersonal.
        
        saveClases(self, tabla: QtWidgets.QTableWidget, row: int,
                  user: int, datos: list | None = None) -> bool:
            Guarda los cambios de la gestión clases.
        
        saveUsuario(self, tabla: QtWidgets.QTableWidget, row: int,
                  user: int, datos: list | None = None) -> bool:
            Guarda los cambios de la gestión usuario.
        
        saveUbi(self, tabla: QtWidgets.QTableWidget, row: int,
                  user: int, datos: list | None = None) -> bool:
            Guarda los cambios de la gestión ubicaciones.
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
        
        # Si se pasaron filtros extra por parámetro...
        if filtrosExtra:
            # Se obtiene la cantidad
            cantFiltrosExtra=len(filtrosExtra)
            # Por cada filtro extra...
            for filtroExtra in filtrosExtra:
                # Si no es None...
                if filtroExtra:
                    # Lo agregamos al filtro final
                    filtro.append(filtroExtra)
                # Si es None...
                else:
                    #...se pasa el filtro pero vacío.
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
        # Consultamos los datos
        datos = bdd.cur.execute(query, filtro).fetchall()
        # Los datos none los reemplazamos con un guión "-".
        return [["-" if cellData == None else cellData
                 for cellData in rowData] for rowData in datos]

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

            gestion: str
                La gestión donde se realizó el cambio.

            fila: int
                El número de la fila que se modificó.

            listaDatosViejos: str | None = None
                Los datos que fueron eliminados o reemplazados.
                Default: None

            listaDatosNuevos: str | None = None
                Los datos que se añadieron o reemplazaron otros datos.
                Default: None
        """
        # Obtenemos el tipo de cambio y la gestión.
        idTipo=bdd.cur.execute('SELECT id FROM tipos_cambio WHERE descripcion=?', (tipo,)).fetchone()[0]
        idGestion=bdd.cur.execute('SELECT id FROM gestiones WHERE descripcion=?', (gestion,)).fetchone()[0]
        # Si no están, entonces cometimos un error de programación.
        if not idTipo or not idGestion:
            info="ERROR DE PROGRAMACION: SE PASARON DATOS EQUIVOCADOS EN LA LLAMADA AL HISTORIAL"
            return PopUp('Error', info).exec()
        # Si se pasó la lista de datos viejos...
        if listaDatosViejos:
            # Lo guardamos como texto como si fuera csv
            # Inicializamos la variable
            datosViejos=''
            # Por cada dato en la lista de datos viejos
            for datoViejo in listaDatosViejos:
                # Lo añadimos al texto con el separador ";"
                datosViejos += f'{datoViejo};'
        # Si no, el texto de datos viejos lo dejamos como None
        else:
            datosViejos=None
        # Hacemos lo mismo con datos nuevos
        if listaDatosNuevos:
            datosNuevos=''
            for datoNuevo in listaDatosNuevos:
                datosNuevos += f'{datoNuevo};'
        else:
            datosNuevos=None
        
        # Obtenemos el usuario
        idUsuario=bdd.cur.execute('SELECT id FROM personal WHERE dni = ?',
                                  (usuario,)).fetchone()[0]
        # Obtenemos los datos a insertar en el historial
        datos=(idUsuario, datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
               idTipo, idGestion, fila, datosViejos, datosNuevos,)
        bdd.cur.execute('INSERT INTO historial VALUES(?,?,?,?,?,?,?)', datos)
        bdd.con.commit()
    
    def verifElimStock(self, idd: int) -> bool:
        """Este método verifica si una fila de la tabla de la gestión
        stock tiene relaciones en la base de datos.
        
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
        """Este método verifica si una fila de la tabla de la gestión
        subgrupos tiene relaciones en la base de datos.
        
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
        """Este método verifica si una fila de la tabla de la gestión
        grupos tiene relaciones en la base de datos.
        
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
        """Este método verifica si una fila de la tabla de la gestión
        clases tiene relaciones en la base de datos.
        
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
        """Este método verifica si una fila de la tabla de la gestión
        ubicaciones tiene relaciones en la base de datos.
        
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
        """Este método verifica si una fila de la tabla de la gestión
        alumnos tiene relaciones en la base de datos.
        
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
        """Este método verifica si una fila de la tabla de la gestión
        usuarios tiene relaciones en la base de datos.
        
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
        """Este método verifica si una fila de la tabla de la gestión
        del personal tiene relaciones en la base de datos.
        
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
        """Este método elimina datos de una tabla.
        
        Parámetros
        ----------
            tabla: str
                La tabla en la que los datos se van a eliminar.
            idd: str
                El id de la fila que se va a eliminar.
        """
        bdd.cur.execute(f"DELETE FROM {tabla} WHERE id = ?", (idd,))
        bdd.con.commit()
    
    def cargarPlanillaAlumnos(self, datos: list, actualizarCursos: bool):
        """Este método carga los datos de una lista en la base de datos
        de alumnos"""
        # Por el numero de fila y el contenido de esta en la lista...
        for n, fila in enumerate(datos):
            # Si los cursos no se reemplazan, se entiende que los
            # cursos usados son en el formato de tutorvip.
            if not actualizarCursos:
                datos[n][1]=f'{fila[1][0]}{fila[1][-1]}'
                
            # Si se pasó un dni que es solo número...
            if isinstance(fila[2], int):
                # Si el largo del dni supera el máximo, corta.
                if fila[2] > 10**8:
                    info = 'Un dni proporcionado en la planilla es demasiado largo. Revise los dni de la plantilla e intente nuevamente.'
                    return PopUp('Error', info).exec()
                # Si no, continua.
                else:
                    continue
            # Si se pasó un dni que es texto...
            elif isinstance(fila[2], str):
                # ... se quitan los puntos del dni.
                dni = ''.join(fila[2].split("."))
                # Si, al quitar los puntos, queda un número...
                if dni.isnumeric():
                    # transformamos el dni a int
                    dni = int(dni)
                    # checkeamos si supera la longitud que queremos
                    if dni > 10**8:
                        info = 'Un dni proporcionado en la planilla es demasiado largo. Revise los dni de la plantilla e intente nuevamente.'
                        return PopUp('Error', info).exec()
                    # Reemplazamos el dni viejo con el dni hecho número
                    datos[n][2] = dni
                    continue
            # Si el dni no era entero ni numero, no es válido.
            info = 'Un dni proporcionado en la planilla no es válido. Revise los dni de la plantilla e intente nuevamente.'
            return PopUp('Error', info).exec()
                
        # Obtenemos todos los cursos distintos nuevos
        cursos=set([fila[1] for fila in datos])
        # Intentamos agregarlos a la base de datos.
        for curso in cursos:
            try:
                bdd.cur.execute('INSERT INTO clases VALUES(NULL, ?, 1)', (curso,))
            # Si ya estaban en la base de datos, ignoramos el error y no lo
            # agregamos
            except sqlite3.IntegrityError:
                pass
        
        # Creamos una tabla e ingresamos todos los alumnos nuevos acá
        # Esto podría hacerse super facil con un merge, pero sqlite no
        # lo soporta. Por esto recomiendo cambiar de motor de base de
        # datos.
        bdd.cur.execute('''CREATE TABLE alumnos_nuevos(
                           nombre_apellido VARCHAR(100) NOT NULL,
                           id_curso INTEGER NOT NULL,
                           dni INTEGER UNIQUE NOT NULL);''')
        for fila in datos:
            idCurso=bdd.cur.execute('SELECT id FROM clases WHERE descripcion LIKE ?', (fila[1],)).fetchone()[0]
            try:
                bdd.cur.execute('INSERT INTO alumnos_nuevos VALUES(?, ?, ?)',
                                (fila[0], idCurso, fila[2],))
            # Si el curso está repetido, ignoramos ingresarlo.
            except sqlite3.IntegrityError:
                pass

        # Acá hacemos un 'merge' hecho código:
        # Verificamos la tabla vieja con la nueva, si el alumno esta en
        # la nueva, se reemplazan los datos viejos con los nuevos, si
        # no, se inserta el alumno nuevo. Si el alumno no está en la
        # lista nueva, se deja como 'egresado' del sistema.     
        with open(f"dal{os.sep}queries{os.sep}merge{os.sep}alumnos.sql", 'r') as queryText:
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
        # Los alumnos egresados sin relaciones en el sistema son
        # eliminados para no ocupar espacio innecesario.
        for egresado in egresados:
            if not self.verifElimAlumnos(egresado[0]):
                bdd.cur.execute('DELETE FROM personal WHERE id=?', (egresado[0],))
        # Eliminamos la tabla que hicimos para el ingreso.
        bdd.cur.execute('DROP TABLE alumnos_nuevos')
        bdd.con.commit()
        
    def cargarPlanillaPersonal(self, datos: list):
        """Este método carga los datos de una lista en la base de datos
        de personal"""
        # Por el numero de fila y el contenido de esta en la lista...
        for n, fila in enumerate(datos):                
            # Si se pasó un dni que es solo número...
            if isinstance(fila[2], int):
                # Si el largo del dni supera el máximo, corta.
                if fila[2] > 10**8:
                    info = 'Un dni proporcionado en la planilla es demasiado largo. Revise los dni de la plantilla e intente nuevamente.'
                    return PopUp('Error', info).exec()
                # Si no, continua.
                else:
                    continue
            # Si se pasó un dni que es texto...
            elif isinstance(fila[2], str):
                # ... se quitan los puntos del dni.
                dni = ''.join(fila[2].split("."))
                # Si, al quitar los puntos, queda un número...
                if dni.isnumeric():
                    # transformamos el dni a int
                    dni = int(dni)
                    # checkeamos si supera la longitud que queremos
                    if dni > 10**8:
                        info = 'Un dni proporcionado en la planilla es demasiado largo. Revise los dni de la plantilla e intente nuevamente.'
                        return PopUp('Error', info).exec()
                    # Reemplazamos el dni viejo con el dni hecho número
                    datos[n][2] = dni
                    continue
            # Si el dni no era entero ni numero, no es válido.
            info = 'Un dni proporcionado en la planilla no es válido. Revise los dni de la plantilla e intente nuevamente.'
            return PopUp('Error', info).exec()
                
        # Obtenemos todas las clases distintas nuevas
        clases=set([fila[1] for fila in datos])
        # Intentamos agregarlos a la base de datos.
        for clase in clases:
            try:
                bdd.cur.execute('INSERT INTO clases VALUES(NULL, ?, 1)', (clase,))
            # Si ya estaban en la base de datos, ignoramos el error y no lo
            # agregamos
            except sqlite3.IntegrityError:
                pass
        
        # Creamos una tabla e ingresamos todos los alumnos nuevos acá
        # Esto podría hacerse super facil con un merge, pero sqlite no
        # lo soporta. Por esto recomiendo cambiar de motor de base de
        # datos.
        bdd.cur.execute('''CREATE TABLE personal_nuevo(
                           nombre_apellido VARCHAR(100) NOT NULL,
                           id_clase INTEGER NOT NULL,
                           dni INTEGER UNIQUE NOT NULL);''')
        for fila in datos:
            idCurso=bdd.cur.execute('SELECT id FROM clases WHERE descripcion LIKE ?', (fila[1],)).fetchone()[0]
            try:
                bdd.cur.execute('INSERT INTO personal_nuevo VALUES(?, ?, ?)',
                                (fila[0], idCurso, fila[2],))
            # Si el curso está repetido, ignoramos ingresarlo.
            except sqlite3.IntegrityError:
                pass

        # Acá hacemos un 'merge' hecho código:
        # Verificamos la tabla vieja con la nueva, si el alumno esta en
        # la nueva, se reemplazan los datos viejos con los nuevos, si
        # no, se inserta el alumno nuevo. Si el alumno no está en la
        # lista nueva, se deja como 'egresado' del sistema.     
        with open(f"dal{os.sep}queries{os.sep}merge{os.sep}personal.sql", 'r') as queryText:
            sql=queryText.read()
        mergeSelect = bdd.cur.execute(sql).fetchall()
        for mergeRow in mergeSelect:
            if mergeRow[2] is None:
                bdd.cur.execute('''
                    UPDATE personal SET id_clase = (
                        SELECT id FROM clases
                        WHERE descripcion LIKE 'Destituído'
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
        destituidos=bdd.cur.execute('''SELECT * FROM personal WHERE id_clase IN (
                SELECT id FROM clases WHERE descripcion='Destituído');''').fetchall()
        # Los alumnos egresados sin relaciones en el sistema son
        # eliminados para no ocupar espacio innecesario.
        for destituido in destituidos:
            if not self.verifElimOtroPersonal(destituido):
                bdd.cur.execute('DELETE FROM personal WHERE id=?', (destituido[0],))
        # Eliminamos la tabla que hicimos para el ingreso.
        bdd.cur.execute('DROP TABLE personal_nuevo')
        bdd.con.commit()
    
    def saveStock(self, tabla: QtWidgets.QTableWidget, row: int,
                  user: int, datos: list | None = None) -> bool:
        """Este método guarda los cambios de la gestión stock.

        Parámetros
        ----------
            tabla: QtWidgets.QTableWidget
                La tabla de la gestión stock.
            row: int
                La fila que fue modificada de la tabla.
            datos: list | None = None
                Datos por defecto que se usarán para guardar registro
                en el historial.
                Default: None.
        
        Devuelve
        --------
            bool: si guardó exitosamente o no.
        """
        desc = tabla.item(row, 1).text()
        iCampos = (1, 2, 7, 8, 9)
        # Por cada campo que no debe ser nulo...
        for iCampo in iCampos:
            # Si el campo está vacio...
            if tabla.item(row, iCampo) is not None:
                texto = tabla.item(row, iCampo).text()
            else:
                texto = tabla.cellWidget(row, iCampo).text()
            if texto == "":
                # Le pide al usuario que termine de llenar los campos
                # y corta la función.
                mensaje = f"El registro {desc} tiene campos en blanco que son obligatorios. Ingreselos e intente nuevamente."
                return PopUp("Error", mensaje).exec()

        try:
            cond = int(tabla.item(row, 2).text())
            rep = int(tabla.item(row, 3).text())
            baja = int(tabla.item(row, 4).text())
            prest = int(tabla.item(row, 5).text())
        except:
            mensaje = "Los datos ingresados no son válidos. Por favor, ingrese los datos correctamente."
            return PopUp("Error", mensaje).exec()

        # Se obtiene el texto de todas las celdas.
        grupo = tabla.cellWidget(row, 7).text()
        subgrupo = tabla.cellWidget(row, 8).text()
        ubi = tabla.cellWidget(row, 9).text()

        # Verificamos que el grupo esté registrado.
        idGrupo = bdd.cur.execute(
            "SELECT id FROM grupos WHERE descripcion LIKE ?", (grupo,)
        ).fetchone()
        # Si no lo está...
        if not idGrupo:
            # Muestra un mensaje de error al usuario y termina la
            # función.
            info = "El grupo ingresado no está registrado. Regístrelo e ingrese nuevamente"
            return PopUp("Error", info).exec()

        # Verificamos que el subgrupo esté registrado y que
        # coincida con el grupo ingresado.
        idSubgrupo = bdd.cur.execute(
            "SELECT id FROM subgrupos WHERE descripcion LIKE ? AND id_grupo = ?",
            (subgrupo, idGrupo[0],)
        ).fetchone()
        if not idSubgrupo:
            info = "El subgrupo ingresado no está registrado o no pertenece al grupo ingresado. Regístrelo o asegúrese que esté relacionado al grupo e ingrese nuevamente."
            return PopUp("Error", info).exec()

        idUbi = bdd.cur.execute("SELECT id FROM ubicaciones WHERE descripcion LIKE ?",
                                (ubi,)).fetchone()
        if not idUbi:
            info = "La ubicación ingresada no está registrada. Regístrela e intente nuevamente."
            return PopUp("Error", info).exec()

        datosNuevos = ["" if cell in (
            "-", None) else cell for cell in [desc, cond, baja, grupo, subgrupo, ubi]]
        try:
            idd = tabla.item(row, 0).text()
            if not idd.isnumeric():
                bdd.cur.execute(
                    "INSERT INTO stock VALUES(NULL, ?, ?, 0, ?, 0, ?, ?)",
                    (desc, cond, baja,
                        idSubgrupo[0], idUbi[0],)
                )
                self.insertarHistorial(
                    user, 'Inserción', 'Stock', f'{desc} {ubi}', None, datosNuevos)
                sql='SELECT id FROM stock WHERE descripcion = ? AND id_ubi = ?'
                a = bdd.cur.execute(sql, (desc, idUbi[0],)).fetchone()
                tabla.item(row, 0).setData(0, a[0])
            else:
                idd = int(idd)
                # Guardamos los datos de la fila en la base de datos
                bdd.cur.execute(
                    """UPDATE stock
                    SET descripcion = ?, cant_condiciones = ?,
                    cant_baja = ?, id_subgrupo = ?, id_ubi=?
                    WHERE id = ?""",
                    (desc, cond, baja,
                        idSubgrupo[0], idUbi[0], idd,)
                )
                datosViejos = [["" if cellData in (
                    "-", None) else cellData for cellData in fila] for fila in datos if fila[0] == idd][0]
                self.insertarHistorial(
                    user, 'Edición', 'Stock', f'{datosViejos[1]} {datosViejos[9]}', datosViejos[2:], datosNuevos)
        except sqlite3.IntegrityError:
            info = "La herramienta que desea ingresar ya está ingresada. Ingrese otra información o revise la información ya ingresada"
            return PopUp("Error", info).exec()

        bdd.con.commit()
        return True
    
    def saveAlumnos(self, tabla: QtWidgets.QTableWidget, row: int,
                  user: int, datos: list | None = None) -> bool:
        """Este método guarda los cambios de la gestión alumnos.

        Parámetros
        ----------
            tabla: QtWidgets.QTableWidget
                La tabla de la gestión stock.
            row: int
                La fila que fue modificada de la tabla.
            datos: list | None = None
                Datos por defecto que se usarán para guardar registro
                en el historial.
                Default: None.
        
        Devuelve
        --------
            bool: si guardó exitosamente o no.
        """
        iCampos = (1, 2, 3)
        nombre = tabla.item(row, 1).text()

        for iCampo in iCampos:
            if iCampo == 2:
                texto = tabla.cellWidget(row, iCampo).text()
            else:
                texto = tabla.item(row, iCampo).text()
            if texto == "":
                mensaje = f"El registro {nombre} tiene campos en blanco que son obligatorios. Ingreselos e intente nuevamente."
                return PopUp("Error", mensaje).exec()

        try:
            dni = int(tabla.item(row, 3).text())
        except:
            mensaje = "Los datos ingresados no son válidos. Por favor, ingreselos correctamente."
            return PopUp("Error", mensaje).exec()

        if dni > 10**8:
            mensaje = "El dni ingresado es muy largo. Por favor, reduzca los dígitos del dni ingresado."
            return PopUp("Error", mensaje).exec()

        clase = tabla.cellWidget(row, 2).text()

        idClase = bdd.cur.execute(
            "SELECT id FROM clases WHERE descripcion LIKE ? AND id_cat=1", (
                clase,)
        ).fetchone()
        if not idClase:
            info = "El curso ingresado no está registrado o no está vinculado correctamente a la categoría alumno. Regístrelo o revise los datos ya ingresados."
            return PopUp("Error", info).exec()
        datosNuevos = [nombre, clase, dni]
        try:
            idd = tabla.item(row, 0).text()
            if not idd.isnumeric():
                bdd.cur.execute(
                    "INSERT INTO personal VALUES(NULL, ?, ?, ?, NULL, NULL)",
                    (nombre, dni, idClase[0],)
                )
                self.insertarHistorial(
                    user, 'Inserción', 'Alumnos', nombre, None, datosNuevos[1:])
                sql='''SELECT id FROM personal WHERE dni=?'''
                a = bdd.cur.execute(sql, (dni,)).fetchone()
                tabla.item(row, 0).setData(0, a[0])
            else:
                idd = int(idd)
                bdd.cur.execute(
                    """UPDATE personal
                    SET nombre_apellido=?, id_clase=?, dni=?
                    WHERE id = ?""",
                    (nombre, idClase[0], dni, idd,)
                )
                datosViejos = [fila for fila in datos if fila[0] == idd][0]
                self.insertarHistorial(
                    user, 'Edición', 'Alumnos', datosViejos[1], datosViejos[2:], datosNuevos)
        except sqlite3.IntegrityError:
            info = "El dni ingresado ya está registrado. Regístre uno nuevo o revise la información ya ingresada."
            return PopUp("Error", info).exec()

        bdd.con.commit()
        return True
    
    def saveGrupos(self, tabla: QtWidgets.QTableWidget, row: int,
                  user: int, datos: list | None = None) -> bool:
        """Este método guarda los cambios de la gestión grupos.

        Parámetros
        ----------
            tabla: QtWidgets.QTableWidget
                La tabla de la gestión stock.
            row: int
                La fila que fue modificada de la tabla.
            datos: list | None = None
                Datos por defecto que se usarán para guardar registro
                en el historial.
                Default: None.
        
        Devuelve
        --------
            bool: si guardó exitosamente o no.
        """
        grupo = tabla.item(row, 1).text()
        if tabla.item(row, 1).text() == "":
            mensaje = f"El registro {grupo} tiene campos en blanco que son obligatorios. Ingreselos e intente nuevamente."
            return PopUp("Error", mensaje).exec()

        try:
            idd = tabla.item(row, 0).text()
            if not idd.isnumeric():
                bdd.cur.execute(
                    "INSERT INTO grupos VALUES(NULL, ?)", (grupo,))
                self.insertarHistorial(
                    user, 'Inserción', 'Grupos', grupo, None, None)
                sql='''SELECT id FROM grupos WHERE descripcion=?'''
                a = bdd.cur.execute(sql, (grupo,)).fetchone()
                tabla.item(row, 0).setData(0, a[0])
            else:
                idd = int(idd)
                bdd.cur.execute(
                    "UPDATE grupos SET descripcion = ? WHERE id = ?",
                    (grupo, idd,)
                )
                datosNuevos = [grupo]
                datosViejos = [fila for fila in datos if fila[0] == idd][0]
                self.insertarHistorial(
                    user, 'Edición', 'Grupos', datosViejos[1], None, datosNuevos)
        except sqlite3.IntegrityError:
            mensaje = "El grupo que desea ingresar ya está ingresado. Ingrese otro grupo o revise los datos ya ingresados."
            return PopUp("Error", mensaje).exec()

        bdd.con.commit()
        return True
    
    def saveOtroPersonal(self, tabla: QtWidgets.QTableWidget, row: int,
                  user: int, datos: list | None = None) -> bool:
        """Este método guarda los cambios de la gestión del personal.

        Parámetros
        ----------
            tabla: QtWidgets.QTableWidget
                La tabla de la gestión stock.
            row: int
                La fila que fue modificada de la tabla.
            datos: list | None = None
                Datos por defecto que se usarán para guardar registro
                en el historial.
                Default: None.
        
        Devuelve
        --------
            bool: si guardó exitosamente o no.
        """
        nombre = tabla.item(row, 1).text()
        iCampos = (1, 2, 3)
        for iCampo in iCampos:
            if iCampo ==2:
                texto = tabla.cellWidget(row, iCampo).text()
            else:
                texto = tabla.item(row, iCampo).text()
            if texto == "":
                mensaje = f"El registro {nombre} tiene campos en blanco que son obligatorios. Ingreselos e intente nuevamente."
                return PopUp("Error", mensaje).exec()

        try:
            dni = int(tabla.item(row, 3).text())
        except:
            mensaje = "Los datos ingresados no son válidos. Por favor, ingreselos correctamente."
            return PopUp("Error", mensaje).exec()

        if dni > 10**8:
            mensaje = "El dni ingresado es muy largo. Por favor, reduzca los dígitos del dni ingresado."
            return PopUp("Error", mensaje).exec()

        clase = tabla.cellWidget(row, 2).text()

        idClase = bdd.cur.execute(
            "SELECT id FROM clases WHERE descripcion = ? AND id_cat=2", (
                clase,)
        ).fetchone()
        if not idClase:
            info = 'La clase ingresada no está registrada o no está vinculada a la categoría "Personal". Regístrela o revise los datos ya ingresados.'
            return PopUp("Error", info).exec()

        datosNuevos = [nombre, clase, dni,]
        try:
            idd = tabla.item(row, 0).text()
            if not idd.isnumeric():
                bdd.cur.execute(
                    "INSERT INTO personal VALUES(NULL, ?, ?, ?, NULL, NULL)",
                    (nombre, dni, idClase[0],)
                )
                self.insertarHistorial(
                    user, 'Inserción', 'Personal', nombre, None, datosNuevos[1:])
                sql='''SELECT id FROM personal WHERE dni=?'''
                a = bdd.cur.execute(sql, (dni,)).fetchone()
                tabla.item(row, 0).setData(0, a[0])
            else:
                idd = int(idd)
                bdd.cur.execute(
                    """UPDATE personal
                    SET nombre_apellido=?, dni=?, id_clase=?
                    WHERE id = ?""",
                    (nombre, dni, idClase[0], idd,)
                )
                datosViejos = [fila for fila in datos if fila[0] == idd][0]
                self.insertarHistorial(
                    user, 'Edición', 'Personal', datosViejos[1], datosViejos[2:], datosNuevos)
        except sqlite3.IntegrityError:
            info = "El dni ingresado ya está registrado. Ingrese uno nuevo o revise la información ya ingresada."
            return PopUp("Error", info).exec()

        bdd.con.commit()
        return True

    def saveSubgrupos(self, tabla: QtWidgets.QTableWidget, row: int,
                  user: int, datos: list | None = None) -> bool:
        """Este método guarda los cambios de la gestión stock.

        Parámetros
        ----------
            tabla: QtWidgets.QTableWidget
                La tabla de la gestión stock.
            row: int
                La fila que fue modificada de la tabla.
            datos: list | None = None
                Datos por defecto que se usarán para guardar registro
                en el historial.
                Default: None.
        
        Devuelve
        --------
            bool: si guardó exitosamente o no.
        """
        iCampos = (1, 2)
        subgrupo = tabla.item(row, 1).text()
        for iCampo in iCampos:
            if iCampo == 2:
                texto = tabla.cellWidget(row, iCampo).text()
            else:
                texto = tabla.item(row, iCampo).text()
            if texto == "":
                mensaje = f"El registro {subgrupo} tiene campos en blanco que son obligatorios. Ingreselos e intente nuevamente."
                return PopUp("Error", mensaje).exec()

        grupo = tabla.cellWidget(row, 2).text()

        idGrupo = bdd.cur.execute(
            "SELECT id FROM grupos WHERE descripcion LIKE ?", (grupo,)
        ).fetchone()
        if not idGrupo:
            info = "El grupo ingresado no está registrado. Regístrelo e ingrese nuevamente"
            return PopUp("Error", info).exec()

        datosNuevos = [subgrupo, grupo]

        try:
            idd = tabla.item(row, 0).text()
            if not idd.isnumeric():
                bdd.cur.execute(
                    "INSERT INTO subgrupos VALUES(NULL, ?, ?)",
                    (subgrupo, idGrupo[0])
                )
                self.insertarHistorial(
                    user, 'Inserción', 'Subgrupos', subgrupo, None, datosNuevos[1:])
                sql='''SELECT id FROM subgrupos
                       WHERE descripcion = ? AND id_grupo = ?'''
                a = bdd.cur.execute(sql, (subgrupo, idGrupo[0])).fetchone()
                tabla.item(row, 0).setData(0, a[0])
            else:
                idd = int(idd)
                # Guardamos los datos de la fila en
                bdd.cur.execute(
                    """UPDATE subgrupos
                    SET descripcion=?, id_grupo=?
                    WHERE id = ?""",
                    (subgrupo, idGrupo[0], idd)
                )
                datosViejos = [fila for fila in datos if fila[0] == idd][0]
                self.insertarHistorial(
                    user, 'Edición', 'Subgrupos', datosViejos[1], datosViejos[2:], datosNuevos)
        except sqlite3.IntegrityError:
            info = "El subgrupo ingresado ya está registrado en el grupo. Ingrese un subgrupo distinto, ingreselo en un grupo distinto o revise los datos ya ingresados."
            return PopUp("Error", info).exec()

        bdd.con.commit()
        return True
    
    def saveUsuarios(self, tabla: QtWidgets.QTableWidget, row: int,
                  user: int, datos: list | None = None) -> bool:
        """Este método guarda los cambios de la gestión stock.

        Parámetros
        ----------
            tabla: QtWidgets.QTableWidget
                La tabla de la gestión stock.
            row: int
                La fila que fue modificada de la tabla.
            datos: list | None = None
                Datos por defecto que se usarán para guardar registro
                en el historial.
                Default: None.
        
        Devuelve
        --------
            bool: si guardó exitosamente o no.
        """
        iCampos = (1, 2, 3, 4, 5)
        nombre = tabla.item(row, 1).text()

        for iCampo in iCampos:
            if iCampo == 2:
                texto = tabla.cellWidget(row, iCampo).text()
            else:
                texto = tabla.item(row, iCampo).text()
            if texto == "":
                mensaje = f"El registro {nombre} tiene campos en blanco que son obligatorios. Ingreselos e intente nuevamente."
                return PopUp("Error", mensaje).exec()

        try:
            dni = int(tabla.item(row, 3).text())
        except:
            mensaje = "Los datos ingresados no son válidos. Por favor, ingreselos correctamente."
            return PopUp("Error", mensaje).exec()

        if dni > 10**8:
            mensaje = "El dni ingresado es muy largo. Por favor, reduzca los dígitos del dni ingresado."
            return PopUp("Error", mensaje).exec()

        clase = tabla.cellWidget(row, 2).text()
        usuario = tabla.item(row, 4).text()
        contrasena = tabla.item(row, 5).text()

        idClase = bdd.cur.execute(
            "SELECT id FROM clases WHERE descripcion LIKE ? AND id_cat=3", (
                clase,)
        ).fetchone()
        if not idClase:
            info = "La clase ingresada no está registrada o no está vinculada correctamente a la categoría usuario. Regístrela o revise los datos ya ingresados."
            return PopUp("Error", info).exec()
        datosNuevos = [nombre, dni, clase, usuario]
        try:
            idd = tabla.item(row, 0).text()
            if not idd.isnumeric():
                bdd.cur.execute(
                    "INSERT INTO personal VALUES(NULL, ?, ?, ?, ?, ?)",
                    (nombre, dni, idClase[0], usuario, contrasena)
                )
                self.insertarHistorial(
                   user, 'Inserción', 'Alumnos', nombre, None, datosNuevos)
                sql='''SELECT id FROM personal WHERE dni=?'''
                a = bdd.cur.execute(sql, (dni,)).fetchone()
                tabla.item(row, 0).setData(0, a[0])
            else:
                idd = int(idd)
                bdd.cur.execute(
                    """UPDATE personal
                    SET nombre_apellido=?, id_clase=?, dni=?
                    WHERE id = ?""",
                    (nombre, idClase[0], dni, idd,)
                )
                datosViejos = [fila for fila in datos if fila[0] == idd][0]
                self.insertarHistorial(
                    user, 'Edición', 'Alumnos', datosViejos[1], datosViejos[2:], datosNuevos)
        except sqlite3.IntegrityError:
            info = "El dni ingresado ya está registrado. Regístre uno nuevo o revise la información ya ingresada."
            return PopUp("Error", info).exec()

        bdd.con.commit()
        return True
    
    def saveUbis(self, tabla: QtWidgets.QTableWidget, row: int,
                  user: int, datos: list | None = None) -> bool:
        """Este método guarda los cambios de la gestión ubicaciones.

        Parámetros
        ----------
            tabla: QtWidgets.QTableWidget
                La tabla de la gestión stock.
            row: int
                La fila que fue modificada de la tabla.
            datos: list | None = None
                Datos por defecto que se usarán para guardar registro
                en el historial.
                Default: None.
        
        Devuelve
        --------
            bool: si guardó exitosamente o no.
        """
        ubicacion = tabla.item(row, 1).text()
        if tabla.item(row, 1).text() == "":
            # Le pide al usuario que termine de llenar los campos
            # y corta la función.
            mensaje = f"El registro {ubicacion} tiene campos en blanco que son obligatorios. Ingreselos e intente nuevamente."
            return PopUp("Error", mensaje).exec()

        try:
            idd = tabla.item(row, 0).text()
            if not idd.isnumeric():
                bdd.cur.execute(
                    "INSERT INTO ubicaciones VALUES(NULL, ?)",
                    (ubicacion,)
                )
                self.insertarHistorial(
                    user, 'Inserción', 'Ubicaciones', ubicacion, None, None)
                sql='''SELECT id FROM ubicaciones WHERE descripcion = ?'''
                a = bdd.cur.execute(sql, (ubicacion,)).fetchone()
                tabla.item(row, 0).setData(0, a[0])
            else:
                idd = int(idd)
                bdd.cur.execute(
                    """UPDATE ubicaciones
                    SET descripcion=?
                    WHERE id = ?""",
                    (ubicacion, idd)
                )
                datosNuevos = [ubicacion,]
                datosViejos = [fila for fila in datos if fila[0] == idd][0]
                self.insertarHistorial(
                    user, 'Edición', 'Ubicaciones', datosViejos[1], None, datosNuevos)
        except sqlite3.IntegrityError:
            info = "El subgrupo ingresado ya está registrado en ese grupo. Ingrese otro subgrupo, ingreselo en otro grupo o revise los datos ya ingresados."
            return PopUp("Error", info).exec()

        bdd.con.commit()
        return True

    def saveClases(self, tabla: QtWidgets.QTableWidget, row: int,
                  user: int, datos: list | None = None) -> bool:
        """Este método guarda los cambios de la gestión stock.

        Parámetros
        ----------
            tabla: QtWidgets.QTableWidget
                La tabla de la gestión stock.
            row: int
                La fila que fue modificada de la tabla.
            datos: list | None = None
                Datos por defecto que se usarán para guardar registro
                en el historial.
                Default: None.
        
        Devuelve
        --------
            bool: si guardó exitosamente o no.
        """
        iCampos = (1, 2,)
        clase = tabla.item(row, 2).text()
        for iCampo in iCampos:
            if tabla.item(row, iCampo) is not None:
                texto = tabla.item(row, iCampo).text()
            else:
                texto = tabla.cellWidget(row, iCampo).text()
            if texto == "":
                mensaje = f"El registro {clase} tiene campos en blanco que son obligatorios. Ingreselos e intente nuevamente."
                return PopUp("Error", mensaje).exec()
        cat = tabla.cellWidget(row, 1).text()
        idCat = bdd.cur.execute(
            'SELECT id FROM cats_clase WHERE descripcion LIKE ?', (cat,)).fetchone()
        if not idCat:
            mensaje = "La categoría ingresada no está registrada. Ingresela e intente nuevamente."
            return PopUp("Error", mensaje).exec()

        info = "Esta acción no se puede deshacer. ¿Desea guardar los cambios en la base de datos?"
        popup = PopUp("Pregunta", info).exec()
        if popup == QtWidgets.QMessageBox.StandardButton.Yes:
            datosNuevos = [clase, cat,]
            try:
                idd = tabla.item(row, 0).text()
                if not idd.isnumeric():
                    bdd.cur.execute(
                        "INSERT INTO clases VALUES(NULL, ?, ?)",
                        (clase, idCat[0],)
                    )
                    self.insertarHistorial(
                        user, 'Inserción', 'Clases', clase, None, datosNuevos[1:])
                    sql='''SELECT id FROM clases
                    WHERE descripcion = ? AND id_cat = ?'''
                    a = bdd.cur.execute(sql, (clase, idCat[0])).fetchone()
                    tabla.item(row, 0).setData(0, a[0])
                else:
                    idd = int(idd)
                    datosViejos = [fila for fila in datos if fila[0] == idd][0]
                    if cat != datosViejos[2] and dal.verifElimClases(idd):
                        mensaje = "La clase que desea cambiar de categoría tiene personal relacionado. Por motivos de seguridad, debe eliminar primero el personal relacionado antes de modificar la categoría de la clase."
                        return PopUp("Advertencia", mensaje).exec()
                    bdd.cur.execute(
                        """UPDATE clases
                        SET descripcion=?,
                        id_cat=?
                        WHERE id = ?""",
                        (clase, idCat[0], idd)
                    )
                    self.insertarHistorial(
                        user, 'Edición', 'Clases', datosViejos[1], datosViejos[2:], datosNuevos)
            except sqlite3.IntegrityError:
                info = "La clase ingresada ya está registrada. Ingrese otra o revise los datos ya ingresados."
                return PopUp("Error", info).exec()

            bdd.con.commit()
            return True

# Se crea el objeto que será usado por los demás módulos para acceder
# a las funciones.
dal=DAL()