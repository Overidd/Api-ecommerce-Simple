from pydantic import BaseModel

class CreateProductSchema(BaseModel):
   name: str
   code: str
   brand: str
   description: str
   size: str
   price: float
   status: bool = True
   stock: int
   category_id: int

class UpdateProductSchema(CreateProductSchema):
   pass