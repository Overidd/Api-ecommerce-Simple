from db import db
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey

# es sqlalchemy.orm
   # es un framework para mapear objetos de Python a tablas de una base de datos relacional.
   # Se utiliza para relacionar tablas y permitir que las operaciones de base de datos sean más fácilmente realizadas con Python.
   
from sqlalchemy.orm import relationship
# from rol_model import RolModel
import datetime

class UserModel(db.Model):
   __tablename__ = 'users'
   id = Column(Integer, primary_key = True)
   name = Column(String(200))
   last_name = Column(String(200))
   
   #Unique es para que no se pueda insertar un email duplicado en la base de datos
   email = Column(String(200), unique=True)
   password = Column(Text)
   status = Column(Boolean, default=True)
   created_at = Column(DateTime, default = datetime.datetime.now)
   
   # onupdate es una función que se ejecuta cuando se actualiza un registro en la tabla.
   updated_at = Column(DateTime, default = datetime.datetime.now, onupdate = datetime.datetime.now)
   
   
   rol_id =  Column(Integer, ForeignKey('roles.id'))   
   # Agrega la relacion con el modelo RolModel
   # Los objetos RolModel se relacionan a través de la columna rol_id
   # Esto permite acceder a los datos del rol asociado a cada usuario con el método rol.to_dict()
   rol = relationship('RolModel')
   
   def to_dict(self):
      return {
         'id': self.id,
         'name': self.name,
         'last_name': self.last_name,
         'email': self.email,
         'status': self.status,
         'created_at': str(self.created_at),
         'updated_at': str(self.updated_at),
         'rol_id': self.rol_id
      }