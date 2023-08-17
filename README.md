# Blustock

Blustock es una aplicación de escritorio diseñada para gestionar el stock de un taller.

La aplicación funciona como un **CRUD**, compuesta de tres capas:
- La interfaz de usuario.
- La capa de acceso de datos.
- La base de datos.

El framework usado es **PyQt**, una adaptación del framwork **Qt** de **c++** para Python.

Los lenguajes usados son:
- **Python**, como lenguaje de programación general.
- **Ui**/xml, como lenguaje especial para diseño de ui prehecha.
- **QSS**, como lenguaje de estilos.
- **SQL**, como lenguaje de consultas de base de datos.

Las librerías de Python usadas son:
- **PyQt**: el framework.
- **os**: permite manejar las rutas de archivo de forma estable y portable.
- **datetime**: permite el manejo de datos de fecha.
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
├── build
├── dist
├── pyproject.toml
├── README.es.md
└── README.MD
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/jonatasemidio/multilanguage-readme-pattern/blob/master/README.md)

TODO: Añadir los links de los iconos a icons8 por el tema de la licencia.
