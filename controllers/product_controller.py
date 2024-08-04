from models.product_model import ProductModel
from pydantic import ValidationError
from schemas.product_schema import (
   CreateProductSchema,
   UpdateProductSchema
)
from typing import Union
from werkzeug.datastructures import FileStorage, MultiDict

from db import db
import uuid

import utils.config_cloudinary
import cloudinary.uploader

class ProductController():
   def __init__(self):
      self.model = ProductModel
      
      
   def get_all(self):
      try:
         products = self.model.query.all()
         return {
            'message': 'Products fetched successfully',
            'data': [product.to_dict() for product in products]
         }, 200
      
      except Exception as e:
         return {
            'message': 'An error ocurred',
            'error': str(e)
         }, 500
      
   def get_all_client(self):
      try:
         products = self.model.query.filter_by(status=True).all()
         return {
            'message': 'Products fetched successfully',
            'data': [product.to_dict() for product in products]
         }, 200
      
      except Exception as e:
         return {
            'message': 'An error ocurred',
            'error': str(e)
         }, 500
   
   def create(self, form:MultiDict, image: Union[FileStorage, None]):
      try: 
         
         if image is None:
            return {
               'message': 'Image is not found',
            }, 400
         
         validated_product = CreateProductSchema(**form)  
         
         # cagar la imagen en cloudinary
         filename = image.filename.split('.')[0]
         upload_response = cloudinary.uploader.upload(image.stream, public_id =f'{uuid.uuid4()}-{filename}')
         # ' image.stream es un tipo de dato bafer'
         # print(image.stream, '---')
         print(upload_response)
         
         new_product = self.model(**validated_product.model_dump())
         new_product.image = upload_response['public_id']
         db.session.add(new_product)
         db.session.commit()
         
         return {
            'message': 'Product created successfully',
            'product': new_product.to_dict(),
         }, 201
      
      except ValidationError as e:
         return {
            'message': 'An error ocurred',
            'error': e.errors(),
         }, 400
      except Exception as e:
         print(e)
         return {
            'message': 'An error occurred',
            'error': str(e)
         }, 500
   
   def update(self, id:int, form:MultiDict, image:FileStorage):
      try:
         validated_product = UpdateProductSchema(**form)
         
         product = self.model.query.get(id)
         if product is None:
            return {
               'message': 'Product not found',
            }, 404
      
         product.name = validated_product.name
         product.description = validated_product.description
         product.price = validated_product.price
         product.size = validated_product.size
         product.code = validated_product.code
         product.brand = validated_product.brand
         product.status = validated_product.status
         product.stock = validated_product.stock
         product.category_id = validated_product.category_id
         
         if image is not None:
            # cagar la imagen en cloudinary
            filename = image.filename.split('.')[0]
            upload_response = cloudinary.uploader.upload(image.stream, image_public_id =f'{uuid.uuid4()}-{filename}')
            
            #Eliminamos la imagen pasada
            cloudinary.uploader.destroy(product.image)
            
            product.image = upload_response['public_id']
         
         db.session.commit()
         return {
            'message': 'Product updated successfully',
            'data': product.to_dict(),
         }, 200
      
      except ValidationError as e:
         return {
            'message': 'An error ocurred',
            'error': e.errors(),
         }, 400
      
      except Exception as e:
         return {
            'message': 'An error occurred',
            'error': str(e)
         }, 500
         
   def delete(self, id:int):
      try:
         product = self.model.query.get(id)
         if product is None:
            return {
               'message': 'Product not found',
            }, 404
            
         product.status = False
         db.session.commit()
         
         return {
            'message': 'Product deleted successfully',
            'data': product.to_dict(),
         }, 200
      except Exception as e:
         return {
            'message': 'An error occurred',
            'error': str(e)
         }, 500
         
   def get_by_id(self, id:int):
      try:
         product = self.model.query.get(id)
         if product is None:
            return {
               'message': 'Product not found',
            }, 404
            
         return {
            'message': 'Product fetched successfully',
            'data': product.to_dict(),
         }, 200
         
      except Exception as e:
         return {
            'message': 'An error occurred',
            'error': str(e)
         }, 500
      