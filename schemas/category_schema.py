from pydantic import BaseModel

class CreateCategorySchema(BaseModel):
   name: str
   status: bool = True
   

class UpdateCategorySchema(CreateCategorySchema):
   pass