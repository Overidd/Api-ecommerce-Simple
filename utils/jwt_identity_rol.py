from flask_jwt_extended import (
   get_jwt_identity,
   verify_jwt_in_request
)

from functools import wraps
from models.user_model import UserModel

def role_required(role:str = None):
   def decorator(fn):
      
      # Para mantener los metadados de la funcion que recibe un metadado de los empods
      @wraps(fn)
      def wrapper(*args, **kwargs):
         
       #la función verify_jwt_in_request() de Flask-JWT-Extended se encarga de verificar que el token JWT (JSON Web Token) enviado sea válido y ha sido generado con la firma correcta en el backend.
         verify_jwt_in_request()
         
         # Obtiene la identidad del usuario que ha proporcionado el token JWT.
         identity = get_jwt_identity()
         user = UserModel.query.get(identity)
         
         if user is None or user.status == False:
            return {
               'error': 'Unauthorized'
            }, 401
            
         if role is not None: 
            if user.rol.name != role:
               return {
                  'error': 'No eres Admin crack'
               }, 401
            
         return fn(*args, **kwargs)
      return wrapper
   return decorator
