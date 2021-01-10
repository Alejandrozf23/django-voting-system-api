# TT 2020-A060
_Aplicación web de apoyo para la jornada electoral_

## Comenzando 🚀
_Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas, es importante recordar que los cambios nunca deben hacerse directamente en Master y siempre crear una rama por cada cambio._

## Pre-requisitos 📋
_Versiones de software_

* [Python 3.8.6](https://www.python.org/downloads/release/python-386/) - Versión de Python
* [Django 3.1.3](https://www.djangoproject.com/download/) - Framework web
* [MySQL 5.7.32](https://dev.mysql.com/downloads/mysql/) - Gestor de base de datos
* [Postman 7.36.1](https://www.postman.com/downloads/) - Gestor de pruebas
* [Visual Studio Code 1.52.1](https://code.visualstudio.com/download) - Editor de texto

## Despliege 🛠️
_Crear base de datos_
* Es importante tener la base de datos creada **(sin tablas)** al momento del despliegue

_Configuración Backend/settings.py_
* Modificar la sección **DATABASES** de acuerdo a su instalación de MySQL

_Migraciones_
* Las migraciones, son el mapeo de los modelos de Django a tablas en MySQL
* Creación de migraciones: **python manage.py makemigrations**
* Mapeo de migraciones: **python manage.py migrate**

_Servidor Django_
* Ejecución: **python manage.py runserver**

## Autor ✒️
* **Alejandro Zepeda** - *Back End* - [Alejandrozf23](https://github.com/Alejandrozf23)