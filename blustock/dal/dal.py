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
                # Si no...
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
        
    def saveStock(self, tabla: QtWidgets.QTableWidget, row: int,
                  user: int, datos: list | None = None):
        """Este método guarda los cambios de la gestión stock en la
        base de datos.

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
        """
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
                mensaje = "Hay campos en blanco que son obligatorios. Ingreselos e intente nuevamente."
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
        desc = tabla.item(row, 1).text()
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
            "-", None) else cell for cell in [desc, cond, rep, baja, prest, grupo, subgrupo, ubi]]
        try:
            idd = tabla.item(row, 0).text()
            if not idd:
                bdd.cur.execute(
                    "INSERT INTO stock VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)",
                    (desc, cond, rep, baja, prest,
                        idSubgrupo[0], idUbi[0],)
                )
                dal.insertarHistorial(
                    user, 'Inserción', 'Stock', desc, None, datosNuevos)
            else:
                idd = int(idd)
                # Guardamos los datos de la fila en
                bdd.cur.execute(
                    """UPDATE stock
                    SET descripcion = ?, cant_condiciones = ?, cant_reparacion=?,
                    cant_baja = ?, cant_prest=?, id_subgrupo = ?, id_ubi=?
                    WHERE id = ?""",
                    (desc, cond, rep, baja, prest,
                        idSubgrupo[0], idUbi[0], idd,)
                )
                datosViejos = [["" if cellData in (
                    "-", None) else cellData for cellData in fila] for fila in datos if fila[0] == idd][0]
                dal.insertarHistorial(
                    user, 'Edición', 'Stock', datosViejos[1], datosViejos[2:], datosNuevos)
        except sqlite3.IntegrityError:
            info = "La herramienta que desea ingresar ya está ingresada. Ingrese otra información o revise la información ya ingresada"
            return PopUp("Error", info).exec()

        bdd.con.commit()
        return True
    
    def saveAlumnos(self, tabla, row, user, datos: list | None = None):
        """Este método guarda los cambios hechos en la tabla de la ui
        en la tabla alumnos de la base de datos.

        Parámetros
        ----------
            datos: list | None = None
                Los datos de la tabla alumnos, que se usarán para
                obtener el id de la fila en la tabla.
        """
        iCampos = (1, 2, 3)

        for iCampo in iCampos:
            if iCampo == 2:
                texto = tabla.cellWidget(row, iCampo).text()
            else:
                texto = tabla.item(row, iCampo).text()
            if texto == "":
                mensaje = "Hay campos en blanco que son obligatorios. Ingreselos e intente nuevamente."
                return PopUp("Error", mensaje).exec()

        try:
            dni = int(tabla.item(row, 3).text())
        except:
            mensaje = "Los datos ingresados no son válidos. Por favor, ingreselos correctamente."
            return PopUp("Error", mensaje).exec()

        if dni > 10**8:
            mensaje = "El dni ingresado es muy largo. Por favor, reduzca los dígitos del dni ingresado."
            return PopUp("Error", mensaje).exec()

        nombre = tabla.item(row, 1).text()
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
                dal.insertarHistorial(
                    user, 'Inserción', 'Alumnos', nombre, None, datosNuevos[1:])
            else:
                idd = int(idd)
                bdd.cur.execute(
                    """UPDATE personal
                    SET nombre_apellido=?, id_clase=?, dni=?
                    WHERE id = ?""",
                    (nombre, idClase[0], dni, idd,)
                )
                datosViejos = [fila for fila in datos if fila[0] == idd][0]
                dal.insertarHistorial(
                    user, 'Edición', 'Alumnos', datosViejos[1], datosViejos[2:], datosNuevos)
        except sqlite3.IntegrityError:
            info = "El dni ingresado ya está registrado. Regístre uno nuevo o revise la información ya ingresada."
            return PopUp("Error", info).exec()

        bdd.con.commit()
        return True
    
    def saveGrupos(self, tabla, row, user, datos: list | None = None):
        """Este método guarda los cambios hechos en la tabla de la ui
        en la tabla grupos de la base de datos.

        Parámetros
        ----------
            datos: list | None = None
                Los datos de la tabla grupos, que se usarán para
                obtener el id de la fila en la tabla.
        """
        if tabla.item(row, 1).text() == "":
            mensaje = "Hay campos en blanco que son obligatorios. Ingreselos e intente nuevamente."
            return PopUp("Error", mensaje).exec()

        grupo = tabla.item(row, 1).text()
        try:
            idd = tabla.item(row, 0).text()
            if not idd.isnumeric():
                bdd.cur.execute(
                    "INSERT INTO grupos VALUES(NULL, ?)", (grupo,))
                dal.insertarHistorial(
                    user, 'Inserción', 'Grupos', grupo, None, None)
            else:
                idd = int(idd)
                bdd.cur.execute(
                    "UPDATE grupos SET descripcion = ? WHERE id = ?",
                    (grupo, idd,)
                )
                datosNuevos = [grupo]
                datosViejos = [fila for fila in datos if fila[0] == idd][0]
                dal.insertarHistorial(
                    user, 'Edición', 'Grupos', datosViejos[1], None, datosNuevos)
        except sqlite3.IntegrityError:
            mensaje = "El grupo que desea ingresar ya está ingresado. Ingrese otro grupo o revise los datos ya ingresados."
            return PopUp("Error", mensaje).exec()

        bdd.con.commit()
        return True
    
    def saveOtroPersonal(self, tabla, row, user, datos: list | None = None):
        """Este método guarda los cambios hechos en la tabla de la ui
        en la tabla personal de la base de datos.

        Parámetros
        ----------
            datos: list | None = None
                Los datos de la tabla personal, que se usarán para
                obtener el id de la fila en la tabla.
        """
        iCampos = (1, 2, 3)
        for iCampo in iCampos:
            if iCampo ==2:
                texto = tabla.cellWidget(row, iCampo).text()
            else:
                texto = tabla.item(row, iCampo).text()
            if texto == "":
                mensaje = "Hay campos en blanco que son obligatorios. Ingreselos e intente nuevamente."
                return PopUp("Error", mensaje).exec()

        try:
            dni = int(tabla.item(row, 3).text())
        except:
            mensaje = "Los datos ingresados no son válidos. Por favor, ingreselos correctamente."
            return PopUp("Error", mensaje).exec()

        if dni > 10**8:
            mensaje = "El dni ingresado es muy largo. Por favor, reduzca los dígitos del dni ingresado."
            return PopUp("Error", mensaje).exec()

        nombre = tabla.item(row, 1).text()
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
            if not datos:
                bdd.cur.execute(
                    "INSERT INTO personal VALUES(NULL, ?, ?, ?, NULL, NULL)",
                    (nombre, dni, idClase[0],)
                )
                dal.insertarHistorial(
                    user, 'Inserción', 'Personal', nombre, None, datosNuevos[1:])
            else:
                idd = int(idd)
                bdd.cur.execute(
                    """UPDATE personal
                    SET nombre_apellido=?, dni=?, id_clase=?
                    WHERE id = ?""",
                    (nombre, dni, idClase[0], idd,)
                )
                datosViejos = [fila for fila in datos if fila[0] == idd][0]
                dal.insertarHistorial(
                    user, 'Edición', 'Personal', datosViejos[1], datosViejos[2:], datosNuevos)
        except sqlite3.IntegrityError:
            info = "El dni ingresado ya está registrado. Ingrese uno nuevo o revise la información ya ingresada."
            return PopUp("Error", info).exec()

        bdd.con.commit()
        return True

    def saveSubgrupos(self, tabla, row, user, datos: list | None = None):
        """Este método guarda los cambios hechos en la tabla de la ui
        en la tabla subgrupos de la base de datos.

        Parámetros
        ----------
            datos: list | None = None
                Los datos de la tabla subgrupos, que se usarán para
                obtener el id de la fila en la tabla.
        """
        iCampos = (1, 2)
        for iCampo in iCampos:
            if iCampo == 2:
                texto = tabla.cellWidget(row, iCampo).text()
            else:
                texto = tabla.item(row, iCampo).text()
            if texto == "":
                mensaje = "Hay campos en blanco que son obligatorios. Ingreselos e intente nuevamente."
                return PopUp("Error", mensaje).exec()

        subgrupo = tabla.item(row, 1).text()
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
            if not datos or not idd.isnumeric():
                bdd.cur.execute(
                    "INSERT INTO subgrupos VALUES(NULL, ?, ?)",
                    (subgrupo, idGrupo[0])
                )
                dal.insertarHistorial(
                    user, 'Inserción', 'Subgrupos', subgrupo, None, datosNuevos[1:])
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
                dal.insertarHistorial(
                    user, 'Edición', 'Subgrupos', datosViejos[1], datosViejos[2:], datosNuevos)
        except sqlite3.IntegrityError:
            info = "El subgrupo ingresado ya está registrado en el grupo. Ingrese un subgrupo distinto, ingreselo en un grupo distinto o revise los datos ya ingresados."
            return PopUp("Error", info).exec()

        bdd.con.commit()
        return True
    
    def saveUsuarios(self, tabla, row, user, datos: list | None = None):
        """Este método guarda los cambios hechos en la tabla de la ui
        en la tabla alumnos de la base de datos.

        Parámetros
        ----------
            datos: list | None = None
                Los datos de la tabla alumnos, que se usarán para
                obtener el id de la fila en la tabla.
        """
        iCampos = (1, 2, 3, 4, 5)

        for iCampo in iCampos:
            if iCampo == 2:
                texto = tabla.cellWidget(row, iCampo).text()
            else:
                texto = tabla.item(row, iCampo).text()
            if texto == "":
                mensaje = "Hay campos en blanco que son obligatorios. Ingreselos e intente nuevamente."
                return PopUp("Error", mensaje).exec()

        try:
            dni = int(tabla.item(row, 3).text())
        except:
            mensaje = "Los datos ingresados no son válidos. Por favor, ingreselos correctamente."
            return PopUp("Error", mensaje).exec()

        if dni > 10**8:
            mensaje = "El dni ingresado es muy largo. Por favor, reduzca los dígitos del dni ingresado."
            return PopUp("Error", mensaje).exec()

        nombre = tabla.item(row, 1).text()
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
        # datosNuevos = [nombre, dni, clase, usuario]
        try:
            idd = tabla.item(row, 0).text()
            if not idd.isnumeric():
                bdd.cur.execute(
                    "INSERT INTO personal VALUES(NULL, ?, ?, ?, ?, ?)",
                    (nombre, dni, idClase[0], usuario, contrasena)
                )
                # dal.insertarHistorial(
                   # user, 'Inserción', 'Alumnos', nombre, None, datosNuevos)
            else:
                idd = int(idd)
                bdd.cur.execute(
                    """UPDATE personal
                    SET nombre_apellido=?, id_clase=?, dni=?
                    WHERE id = ?""",
                    (nombre, idClase[0], dni, idd,)
                )
                # datosViejos = [fila for fila in datos if fila[0] == idd][0]
                # dal.insertarHistorial(
                #     user, 'Edición', 'Alumnos', datosViejos[1], datosViejos[2:], datosNuevos)
        except sqlite3.IntegrityError:
            info = "El dni ingresado ya está registrado. Regístre uno nuevo o revise la información ya ingresada."
            return PopUp("Error", info).exec()

        bdd.con.commit()
        return True
    
    def saveUbis(self, tabla, row, user, datos: list | None = None):
        """Este método guarda los cambios hechos en la tabla de la ui
        en la tabla subgrupos de la base de datos.

        Parámetros
        ----------
            datos: list | None = None
                Los datos de la tabla subgrupos, que se usarán para
                obtener el id de la fila en la tabla.
        """
        if tabla.item(row, 1).text() == "":
            # Le pide al usuario que termine de llenar los campos
            # y corta la función.
            mensaje = "Hay campos en blanco que son obligatorios. Ingreselos e intente nuevamente."
            return PopUp("Error", mensaje).exec()

        ubicacion = tabla.item(row, 1).text()
        try:
            idd = tabla.item(row, 0).text()
            if not idd.isnumeric():
                bdd.cur.execute(
                    "INSERT INTO ubicaciones VALUES(NULL, ?)",
                    (ubicacion,)
                )
                dal.insertarHistorial(
                    user, 'Inserción', 'Ubicaciones', ubicacion, None, None)
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
                dal.insertarHistorial(
                    user, 'Edición', 'Ubicaciones', datosViejos[1], None, datosNuevos)
        except sqlite3.IntegrityError:
            info = "El subgrupo ingresado ya está registrado en ese grupo. Ingrese otro subgrupo, ingreselo en otro grupo o revise los datos ya ingresados."
            return PopUp("Error", info).exec()

        bdd.con.commit()
        return True

    def saveClases(self, tabla, row, user, datos: list | None = None):
        """Este método guarda los cambios hechos en la tabla de la ui
        en la tabla subgrupos de la base de datos.

        Parámetros
        ----------
            datos: list | None = None
                Los datos de la tabla subgrupos, que se usarán para
                obtener el id de la fila en la tabla.
        """
        iCampos = (1, 2,)
        for iCampo in iCampos:
            if tabla.item(row, iCampo) is not None:
                texto = tabla.item(row, iCampo).text()
            else:
                texto = tabla.cellWidget(row, iCampo).text()
            if texto == "":
                mensaje = "Hay campos en blanco que son obligatorios. Ingreselos e intente nuevamente."
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
            clase = tabla.item(row, 2).text()
            datosNuevos = [clase, cat,]
            try:
                idd = tabla.item(row, 0).text()
                if not idd.isnumeric():
                    bdd.cur.execute(
                        "INSERT INTO clases VALUES(NULL, ?, ?)",
                        (clase, idCat[0],)
                    )
                    dal.insertarHistorial(
                        user, 'Inserción', 'Clases', clase, None, datosNuevos[1:])
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
                    dal.insertarHistorial(
                        user, 'Edición', 'Clases', datosViejos[1], datosViejos[2:], datosNuevos)
            except sqlite3.IntegrityError:
                info = "La clase ingresada ya está registrada. Ingrese otra o revise los datos ya ingresados."
                return PopUp("Error", info).exec()

            bdd.con.commit()
            return True

# Se crea el objeto que será usado por los demás módulos para acceder
# a las funciones.
dal=DAL()