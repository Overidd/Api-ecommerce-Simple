from pydantic import BaseModel, Field

class OrderDetailSchema(BaseModel):
   # Verifcamos que sea mayor a 0 con Field
   quantity: int = Field(gt=0)
   price: float = Field(gt=0)
   subtotal: float = Field(gt=0)
   product_id: int
   

class OrderSchem(BaseModel):
   client_name: str
   client_last_name: str
   client_address: str
   client_documents_number: str
   total: float = Field(gt=0)
   order_details: list[OrderDetailSchema]