## Ecommerce-API

## Dependencias

'''bash
pip install Flask
pip install Flask-Cors
pip install Flask-SQLALchemy
pip install Flask-Migrate
pip install psycopg2-binary
pip install pydantic 
pip install bcrypt # para encriptar una contraseña
pip install pydantic[email] # verificar si es un correo
pip install Flask-JWT-Extended # para comprar con Json web token
pip install python-dotenv
pip install cloudinary # Un storage de archivos donde se guardara las imagenes

'''
# Flask-Migrate
'''
 Flask-Migrate, una extensión que integra Alembic (una herramienta de migración de bases de datos) con Flask y Flask-SQLAlchemy. Esto permite gestionar cambios en la estructura de la base de datos a lo largo del tiempo, como crear o modificar tablas, de manera ordenada y segura.
'''

## Migrar el modelo creado a la base de datos
'''bash
# Crear la carpeta migrations (Solo la primera vez)
flask db init

# Crear la migración (Cada vez que se modifique el modelo)
flask db migrate -m "Create tables"

# Aplicar la migración (Cada vez que se modifique el modelo)
flask db upgrade
'''