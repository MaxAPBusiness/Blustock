# Blustock

*Esta es la versión del README en inglés. Para ver la versión en español, ir al siguiente enlance (This is the english README translation. To see the spanish version, go to the following link):* [![es](https://img.shields.io/badge/lang-es-yellow.svg)](https://github.com/MaxAPBusiness/Blustock/blob/main/README.es.md)

Blustock is a desktop app designed for registering and managing a school warehouse's flow of elements.

The app also works as a **CRUD**, and it is composed of three layers: the UI, a DAL and the DB.

If the app receives support, I am going to explain specifically how the app works. For the moment, see the user guide (it is in spanish though, sorry) (TODO: put link here).

The app is designed specifically for registering and managing a school warehouse's flow of elements, but it can also be adapted to any workshop that needs registry and managing by playing with the code. The app is also currently in spanish only, though, if the project receives support, i could work in an english translation. 

The implemented framework is **PyQt**. The app languages are:
- **Python**, as general programming language.
- **Ui/xml**, as language for prebuilt ui files.
- **QSS**, as style language.
- **SQL**, as database query language.

The Python libraries used are:
- **PyQt**: the framework.
- **os**: for managing paths in a consistent and portable way.
- **datetime**: permite el manejo de datos de fecha.
- **dateutil**: permite, a una fecha, sumarle y restarle un tiempo específico relativo a ella.
- **textwrap**: permite quitar la identación a texto multilínea.
- **unidecode**
- **pandas**: permite manejar y crear archivos xlsx.
- **types**: permite añadir sugerencias de tipos de parámetro especiales.
- **sys**: Qt lo necesita para funcionar.
- **sqlite3**: permite crear la base de datos.

The project is structured in the following way:  *Notes are in spanish, I will later translate them into english.*
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

The project's collaborators are:
- **maxapbusiness**: the repository owner, project leader, made the CRUD (database, dal, connecting ui with the database), implemented the history functionality and documented all the project (the one who wrote this readme :p). Mail: mapellegrinobusiness@gmail.com
- **tbuda04**: project leader, implemented the movement and user functionality.
- **Maateoooo**: implemented ui structure and design and app icon.
- **valenbru**: implemented design.
- **s-anti**: helped with ui and coding.
- **Santy-git**: helped with ui and coding.

*This app uses icons8 content. Link to the official icons8 page:* https://icons8.com
