import datetime as dt
from main import cur

def registrarCambios(tipo, tablas, idd, datosViejos, datosNuevos):
    global userInfo
    if userInfo[1]:
        cur.execute('SELECT ID FROM ADMINISTRADORES WHERE USUARIO=?',(userInfo[0]))
    else:
        cur.execute('SELECT ID FROM USUARIOS WHERE USUARIO=?',(userInfo[0]))
    userId=cur.fetchall()[0][0]
    cur.execute('INSERT INTO HISTORIAL_DE_CAMBIOS VALUES(?, ?, ?, ?, ?, ?, ?, ?)', 
    (userId, userInfo[1], dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 
    "Inserción", "Subgrupos", idd, datosViejos, datosNuevos,))
