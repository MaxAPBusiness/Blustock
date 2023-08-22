# Blustock

*This is the spanish README translation. To see the english version, go to the following link (Esta es la versión del README en español. Para ver la versión inglesa, ir al siguiente enlance):* [![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/MaxAPBusiness/Blustock/blob/main/README.md)

Blustock es una aplicación de escritorio diseñada para gestionar la entrada y salida de herramientas de un taller de un colegio.

La aplicación también funciona como un **CRUD**, compuesta de tres capas:
- La interfaz de usuario.
- La capa de acceso de datos.
- La base de datos.

Funciona de la siguiente manera:  
1. Un usuario (normal o admin) inicia sesión. La diferencia de privilegios está en que el admin puede acceder a la gestión de ubicaciones y el admin no.  
2. Una vez dentro, pueden:  
2. 1. Gestionar datos: se puede ver, modificar y eliminar datos.  
2. 2. Ver listados: solo se pueden ver datos.  
2. 3. Realizar movimientos: proximamente se explicará.  
2. 4. Cargar turnos: proximamente se explicará.  

Para ver como funciona la app en profundidad, leer la guía de usuario (https://docs.google.com/document/d/1PsNRFtbi3YwYBC2aCry-U-qTe4iRChxhenEuYK33EQ4/edit).

Para ver cómo funciona cada función, clase, método y módulo, leer la documentación.

Hay cosas en el programa que quedaron pendientes y estaría bueno que lo hagan ustedes, estas son:  
1. Cambiar el motor de base de datos. Esto es debido a que el motor actual no soporta el dato fecha (lo guardamos como texto y eso genera un peso extra que sería innecesario con otro motor). Además, podrían adaptar el merge rudimentario que hicimos en el sqlite con un merge verdadero de un motor de base de datos pulido. Recomiendo personalmente PostgreSQL, aunque pueden usar cualquier otro motor. Cuando lo cambien, adapten los campos fecha y el merge.  
2. Añadir gestiones de lugares de reparación. En la gestión debería estar el nombre del lugar e info de referencia (mail, telefono, etc.). Luego, relacionar esa gestión con el listado de seguimientos de reparación.  
3. Encriptar los archivos del programa para que no puedan acceder asi nomás. Como esta hecha la app y como la distribuimos, esta abierta para que cualquiera que sepa un cachitin de programación pueda entrar, leer y entender el código (eso incluye la base de datos). Vean la forma de encriptarlo y que no se pueda entrar desde afuera.  
4. Encriptar contraseñas: las contraseñas de los usuarios no están encriptadas. Pueden usar una librería (fernet, por ejemplo) para encriptarlas con Python facilmente.  
5. Que, en el resumen del día, las deudas en el día se sume la cantidad si la persona y la herramienta y la ubicación son las mismas. Como está hecho ahora, se muestra cada movimiento por separado, vcuando estaría mejor mostrar las deudas agrupadas por herramienta y ubicación y persona.  

**Ojito con querer vender el programa, porque está prohibido por licencia. No se hagan los vivos 👀**  
Link de la licencia en español: https://github.com/MaxAPBusiness/Blustock/blob/main/LICENCIA.es

Está diseñada específicamente para gestionar la entrada y salida de herramientas de un taller de un colegio, pero puede ser adaptada a cualquier taller que tenga pañoleros y requiera gestionar la entrada y salida de herramientas si se cambia mediante código.

El framework implementado es **PyQt**. Los lenguajes de la app son:
- **Python**, como lenguaje de programación general.
- **Ui/xml**, como lenguaje especial para diseño de ui prehecha.
- **QSS**, como lenguaje de estilos.
- **SQL**, como lenguaje de consultas de base de datos.

Las librerías de Python usadas son:
- **PyQt**: el framework.
- **os**: para manejar las rutas de archivo de forma estable y portable.
- **datetime**: para el manejo de datos de fecha.
- **dateutil**: permite, a una fecha, sumarle y restarle un tiempo específico relativo a ella.
- **textwrap**: permite quitar la identación a texto multilínea.
- **unidecode**
- **pandas**: permite manejar y crear archivos xlsx.
- **types**: permite añadir sugerencias de tipos de parámetro especiales.
- **sys**: Qt lo necesita para funcionar.
- **sqlite3**: permite crear la base de datos.

El proyecto se estructura de la siguiente forma:  

Blustock/                        > raíz  
├── .git                         > archivo automático de git  
├── blustock/                    > carpeta principal del proyecto  
│   ├── dal/                     > contiene todos los archivos de la capa de acceso de datos  
│   │   ├── queries/             > contiene todas las consultas del DAL  
│   │   │   ├── merge/           > contiene todas las consultas del merge  
│   │   │   │   ├── alumnos.sql  > la consulta de merge de alumnos  
│   │   │   │   └── personal.sql > la consulta de merge de personal  
│   │   │   ├── resumen/         > contiene todas las consultas de la pantalla resumen  
│   │   │   │   ├── baja.sql     > la consulta de elementos dados de baja  
│   │   │   │   └── deudas.sql   > la consulta de elementos adeudados  
│   │   │   ├── alumnos.sql  
│   │   │   ├── clases.sql  
│   │   │   ├── deudas.sql  
│   │   │   ├── estados.sql  
│   │   │   ├── grupos.sql  
│   │   │   ├── historial.sql  
│   │   │   ├── movimientos.sql  
│   │   │   ├── otro_personal.sql  
│   │   │   ├── reparaciones.sql  
│   │   │   ├── stock.sql  
│   │   │   ├── subgrupos.sql  
│   │   │   ├── tipos_mov.sql  
│   │   │   ├── turnos.sql  
│   │   │   ├── ubicaciones.sql  
│   │   │   └── usuarios.sql  
│   │   └── dal.py               > contiene una clase para gestionar el flujo de datos entre la base de datos y la IU  
│   ├── db/                      > contiene todos los archivos relacionados con la base de datos  
│   │   ├── bdd.py               > contiene una clase que crea la conexión y el cursor de la base de datos  
│   │   └── blustock.sqlite3     > la base de datos  
│   ├── ui/                      > contiene todos los archivos relacionados exclusivamente con la IU  
│   │   ├── presets/             > contiene todos los widgets prehechos con código  
│   │   │   ├── boton.py         > contiene una clase que crea botones preconfigurados.  
│   │   │   ├── param_edit.py    > contiene una clase para crear lineEdits con campos de sugerencia  
│   │   │   ├── popup.py         > contiene una clase que genera un mensaje emergente.  
│   │   │   ├── Toolbotoon.py  
│   │   │   └── turnos.py  
│   │   └── rsc/                 > contiene todos los archivos que se usarán como recursos para la IU.  
│   │       ├── fonts/           > contiene todas las fuentes.  
│   │       │   ├── marlett.ttf  
│   │       │   ├── Oswald-VariableFont_wght.ttf  
│   │       │   ├── Righteous-Regular.ttf  
│   │       │   └── Slabo27px-Regular.ttf  
│   │       ├── icons/           > contiene todos los íconos.  
│   │       │   ├── buscar.png  
│   │       │   ├── eliminar.png  
│   │       │   ├── esconder.png  
│   │       │   ├── flecha.png  
│   │       │   ├── guardar.png  
│   │       │   ├── mostrar.png  
│   │       │   └── usuario.png  
│   │       ├── screens_uis/     > contiene todos los archivos ui de las pantallas. Cada archivo ui es un preset de una pantalla.  
│   │       │   ├── alumnos.ui  
│   │       │   ├── cargar_turno.ui  
│   │       │   ├── clases.ui  
│   │       │   ├── deudas.ui  
│   │       │   ├── finalizar_turno.ui  
│   │       │   ├── grupos.ui  
│   │       │   ├── historial.ui  
│   │       │   ├── login.ui  
│   │       │   ├── main.ui      > este contiene la ventana principal con un menú  
│   │       │   ├── movimientos.ui  
│   │       │   ├── n-movimiento.ui  
│   │       │   ├── otro_personal.ui  
│   │       │   ├── reparaciones.ui  
│   │       │   ├── resumen.ui  
│   │       │   ├── stock.ui  
│   │       │   ├── subgrupos.ui  
│   │       │   ├── turnos.ui  
│   │       │   ├── ubicaciones.ui  
│   │       │   └── usuarios.ui  
│   │       └── styles.qss       > la página de estilos de todo el programa  
│   ├── core.py                  > contiene funciones varias útiles para el programa  
│   └── main.py                  > el archivo principal. Genera la ventana principal y ejecuta la aplicación.  
├── build                        > las distribuciones  
├── dist                         > las distribuciones  
├── pyproject.toml               > las especificaciones del proyecto  
├── README.es.md                 > 📍 Usted está aquí.  
└── README.MD                    > El README que estás leyendo, pero en inglés.  

Los colaboradores del proyecto son:
- **maxapbusiness**: El dueño del repositorio, jefe de proyecto, encargado del CRUD (base de datos, dal, conectar ui con la base de datos), implementó la funcionalidad del historial y documentó todo el projecto (escribió este readme :p). Mail: mapellegrinobusiness@gmail.com
- **tbuda04**: Jefe de proyecto, encargado de integrar la funcionalidad de usuarios y de registro de movimientos.
- **Maateoooo**: Encargado de la ui y del diseño general del programa, diseñó el logo.
- **valenbru**: Encargada de la ui y del diseño general del programa.
- **s-anti**: Ayudante en la ui y en código.
- **Santy-git**: Ayudante en la ui y en código.

*Esta aplicación usa contenido de icons8. Link a la página oficial de icons8:* https://icons8.com