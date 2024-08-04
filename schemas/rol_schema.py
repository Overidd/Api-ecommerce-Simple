from pydantic import BaseModel

# se crea una clase que hereda de BaseModel y define los atributos y tipos de datos que se esperan en la clase  
class RolSchema(BaseModel):
   name: str
   status: bool = True

class RolUpdateSchema(BaseModel):
   name: str
   status: bool = True # opcional, si no se envia, toma el valor por defecto. Por eso es opcional en la clase RolUpdateSchema.
   
   
   