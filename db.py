from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

'''
Configuración inicial para utilizar SQLAlchemy con Flask, un framework web en Python:

from flask_sqlalchemy import SQLAlchemy: Esta línea importa la clase SQLAlchemy del módulo flask_sqlalchemy. Flask-SQLAlchemy es una extensión de Flask que facilita la integración de SQLAlchemy, un ORM (Object-Relational Mapping) en proyectos Flask. ORM es una técnica que permite interactuar con bases de datos utilizando objetos de Python, en lugar de escribir directamente consultas SQL.

db = SQLAlchemy(): Aquí se crea una instancia de SQLAlchemy. Esta instancia, db, es el objeto que se usará para interactuar con la base de datos a través de SQLAlchemy. Se utiliza para definir modelos, manejar la conexión a la base de datos, realizar consultas, y más.
'''