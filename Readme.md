## Proyect Back End
Para la realizacion de este proyecto se utilizo el siguiente framework: FlaskAPI de Python

## Requesistos
Se requere tener instalado en el equipo el siguiente software:

- Python 3.8
- MySQL

## Instalacion
Para instalar el proyecto se debe ejecutar el siguiente comando en la consola:
```
pip install -r requirements.txt
```

Además se debe de crear una base de datos en MySQL con el siguiente script:
```
CREATE DATABASE STOREDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## Migración

```
flask db init
flask db migrate -m "tablas con relaciones"
flask db upgrade
```

## Ejecucion
Para ejecutar el proyecto se debe ejecutar el siguiente comando en la consola:

```
flask run
```