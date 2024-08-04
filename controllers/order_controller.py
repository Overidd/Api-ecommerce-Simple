from models.order_detail_model import OrderDetailModel
from models.order_model import OrderModel
from models.product_model import ProductModel
from schemas.order_schema import OrderSchem
from pydantic import ValidationError
from db import db

class OrderController:
   def __init__(self):
      self.model_product = ProductModel
      self.model_order = OrderModel
      self.model_order_detail = OrderDetailModel
   
   def create(self, json:dict):
      try:
         pass
         # Validar la data
         validated_order = OrderSchem(**json)
         details = validated_order.order_details
         # order = [dict( filter( lambda valor: valor !='order_details', validated_order))]
   
         # Validar el stock del product 
         new_order_details = []
         for detail in details:
            product = self.model_product.query.get(detail.product_id)

            if product is None:
               return {
                  'message': 'Product not found',
               }, 404
                
                # Validar el estado del producto
            if product.status == False:
               return {
                  'message': f'Product {product.name} is out of stock',
               }, 400
                
                # Validar el stock del producto
            if product.stock < detail.quantity:
               return {
                  'message': f'Product {product.name} is out of stock'
               }, 400

            product.stock -= detail.quantity
            
             # Crear el detalle de la orden
            new_order_detail = self.model_order_detail(
               quantity=detail.quantity,
               price=detail.price,
               subtotal=detail.subtotal,
               product_id=detail.product_id
            )
            new_order_details.append(new_order_detail)
            
         #* Crear codigo de product
         last_order = self.model_order.query.order_by(self.model_order.id.desc()).first()
         
         print('------',last_order.code)
         new_code = ''
         if last_order is None:
            new_code = 'C01-0001'
         else:
            num_order = int(last_order.code.split('-')[1])
            num_order += 1
            new_num_order = str(num_order).zfill(4)
            new_code = f'C01-{new_num_order}'
         
         # Crear la orden
         new_order = self.model_order(
            code = new_code,
            client_name = validated_order.client_name,
            client_last_name = validated_order.client_last_name,
            client_address = validated_order.client_address,
            client_documents_number = validated_order.client_documents_number,
            total = sum([detail.subtotal for detail in details]),
            order_details = new_order_details,
         )
         
         db.session.add(new_order)
         db.session.commit()
         
         # Guardar los cambios en la base de datos
         return {
            'message': 'Order created successfully',
            'data':new_order.to_dict(),
         }, 200
      
      except ValidationError as e:
         return {
            'message': 'An error ocurred',
            'error': e.errors(),
         }, 400
      
      except Exception as e:
         db.session.rollback()
         return {
            'message': 'An error occurred',
            'error': str(e)
         }, 500
         
         
   def get_all(self):
      try:
         orders = self.model_order.query.all()
         return {
            'message': 'Orders fetched successfully',
            'data': [order.to_dict() for order in orders]
         }, 200
         
      except Exception as e:
         return {
            'message': 'An error occurred',
            'error': str(e)
         }, 500
         
   def cancel(self, id:int):
      try:
         order = self.model_order.query.get(id)
         
         if order is None:
            return {
               'message': 'Order not found',
            }, 404
            
         order.status = False
         db.session.commit()
         
         return {
            'message': 'Order deleted successfully',
            'data': order.to_dict(),
         }, 200
         
      except Exception as e:
         return {
            'message': 'An error occurred',
            'error': str(e)
         }