from models.user_model import UserModel
from pydantic import ValidationError
from schemas.user_schema import UserSchema,LoginSchema, UpdateUserSchema
from flask_jwt_extended import (
   create_access_token,
   create_refresh_token,
)

from db import db
import bcrypt

class UserController:
   def __init__(self) -> None:
      self.model = UserModel
   
   def create(self, json:dict):
      try:
         validated_user = UserSchema(**json)
         
         # Verificar si el usuario existe
         is_user_email = self.model.query.filter_by(email = validated_user.email).first()
         
         if is_user_email:
            return {
               'message': 'El usuario existe'
            }, 400
            
         # Encriptador la contraseña
         validated_user.password = self.__hash_password(validated_user.password) 
         
         # Crea un nuevo usuario
         new_user = self.model(**validated_user.model_dump())
         db.session.add(new_user)
         db.session.commit()
         
         return {
            "message": "Usuario creado exitosamente",
            "user": new_user.to_dict()
         }, 201
      
      except ValidationError as e:
         return {
            'message': 'Error a crear un nuevo user',
            'error': e.errors()
         }, 400
      except Exception as e:
         return {
            'message': 'Error Exception',
            'error': str(e)
         }, 500
   
   def get_all(self):
      try:
         users = self.model.query.all()
         
         return {
            'message': 'User fetched successfully',
            'data': [user.to_dict() for user in users]
         }
      
      except Exception as e:
         return {
            'message': 'Error al obtener usuarios',
            'error': str(e)
         }, 500
   
   def login(self, json:dict):
      try:
         validate_crendentials = LoginSchema(**json)
         
         user = self.model.query.filter_by(email = validate_crendentials.email).first()
         
         if user is None or user.status == False:
            return {
               'message': 'Unauthorized'
            }, 401
         
         pwd_valid = bcrypt.checkpw(validate_crendentials.password.encode('utf-8'),user.password.encode('utf-8'))
         
         if not pwd_valid:
            return {
               'message': 'Unauthorized'
            }, 401
            
         # Generamos el token JWT
         access_token = create_access_token(identity=user.id)
         refresh_token = create_refresh_token(identity=user.id)         
      
         return {
            'message': 'Login successfully',
               'data': {
                  'access_token': access_token,
                  'refresh_token': refresh_token
            }
         }, 200
         
      except ValidationError as e:
         return {
            'message': 'An error ocurred',
            'error': e.errors()
         }, 400
      
      except Exception as e:
         return {
            'message': 'error',
            'error': str(e)
         }, 500
         
   def update(self, id:int, json:dict):
      try:
         
         validated_user = UpdateUserSchema(**json)
         if validated_user.password != validated_user.password_confirm:
            return {
               'message': 'Password do not match',
            }, 400         
         
         user = self.model.query.get(id)
         
         if user is None:
            return {
               'message': 'User not found',
            }, 404
            
         user.name = validated_user.name
         user.last_name = validated_user.last_name
         user.email = validated_user.email
         user.status = validated_user.status
         user.rol_id = validated_user.rol_id
         
         if validated_user.password is not None and validated_user.password_confirm is not None:
            has_password = self.__hash_password(validated_user.password)
            user.password = has_password
         
         db.session.commit()
         
         return {
            'message': 'User updated successfully',
            'data': user.to_dict()
         }
        
      except ValidationError as e:
         return {
            'message': 'An error ocurred',
            'error': e.errors()
         }, 400
   
         
      except Exception as e:
         return {
            'message': 'Error',
            'error': str(e)
         }, 500
   
   def delete(self, id:int):
      try:
         user = self.model.query.get(id)
         
         if user is None:
            return {
               'message': 'User not found'
            }, 404
            
         user.status = False
         # db.session.delete(user)
         db.session.commit()
         
         return {
            'message': 'User deleted successfully'
         }
         
      except ValidationError as e:
         return {
            'message': 'An error ocurred',
            'error': e.errors()
         }, 400
         
      except Exception as e:
         return {
            'message': str(e)
         }, 500
   
   def __hash_password(self, password:str):
      # Convierte la contraseña en un binario, que acepta caracteres especiales
      pwd_bytes = password.encode('utf-8')
      
      # Hashea la contraseña utilizando bcrypt, generando una sal y devuelve la contraseña hasheada.      
      # gensalt(), hasheada por defecto 12 ronda la contraseña
      pwd_hashed = bcrypt.hashpw(pwd_bytes, bcrypt.gensalt())
      
      # Devuelve la contraseña hasheada como un string.
      return pwd_hashed.decode('utf-8')