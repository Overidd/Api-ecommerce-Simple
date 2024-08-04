from models.rol_model import RolModel
from models.user_model import UserModel
from models.rol_model import RolModel
from schemas.rol_schema import RolSchema, RolUpdateSchema
from flask_jwt_extended import get_jwt_identity
from pydantic import ValidationError
from db import db

class RolController:
   def __init__(self) -> None:
      self.model = RolModel
      self.user_model = UserModel
      
   def create(self, json:dict):
      try:
         # enviar por parametro con **, que convierte en datos separados, en pocas palabras, distribuye los datos del diccionario
         validated_rol = RolSchema(**json)
         
         # con ** distribuye los datos de la instancia validate_rol y con model_dump() crea un nuevo diccionario con los valores distribuido de los atributos de la clase RolSchema
         # y los devuelve.         
         new_rol = self.model(**validated_rol.model_dump())
         db.session.add(new_rol)
         db.session.commit()
         
         return {
            "message": "Rol creado exitosamente",
            "rol": new_rol.to_dict(),
         }, 201          
      except ValidationError as e:
         return {
            "detail": e.errors(),
            "code": "ValidationError"
         }, 400         
         
      except Exception as e:
         return {
            'message': 'Error al crear rol: {str(e)}',
            'error': str(e)
         }, 500
   
   def get_all(self):
      try:
         # self.is_rol_admin()
         # query.all() devuelve todos los objetos de la clase RolModel que se encuentran en la base de datos.
         roles = self.model.query.all()
         
         return {
            'message': 'Roles fetched succcessfully',
            'data': [rol.to_dict() for rol in roles]
         }
      except Exception as e:
         return {
            'message': 'Error al obtener roles: {str(e)}',
            'error': str(e)
         }, 500
   
   def update(self, id:int, json:dict):
      try: 
         rol = self.model.query.get(id)
         
         if rol is None: 
            return {
               'message': 'Rol no encontrado'
            }, 404
         
         update_rol = RolUpdateSchema(**json)   
         rol.name = update_rol.name
         rol.status = update_rol.status
         
         db.session.commit()
         
         return {
            'message': 'Rol actualizado correctamente',
            'data': rol.to_dict()
         }
      except ValidationError as e:
         return {
            'message': 'ValidationError',
            'error': e.errors(),
         }, 400
      except Exception as e:
         return {
            'message': 'Error al actualizar rol',
            'error': str(e)
         }, 500
   def delete(self, id:int):
      try:
         rol = self.model.query.get(id)
         
         if rol is None:
            return {
               'message': 'Rol no encontrado'
            }, 404
         
         db.session.delete(rol)
         db.session.commit()
         
         return {
            'message': 'Rol eliminado correctamente'
         }, 200
      
      except Exception as e:
         return {
            'message': 'Error al buscar rol',
            'error': str(e)
         }, 500
         
   def is_rol_admin(self):
      identity = get_jwt_identity()
      user = self.user_model.query.get(identity)  
          
      if user is None or user.status == False:
         return {
            'error': 'Unauthorized'
         }, 401
      
      if user.rol.name != 'ADMIN':
          return {
            'error': 'no es admin'
         }, 401
          