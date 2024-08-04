from models.category_model import CategoryModel
from db import db
from pydantic import ValidationError
from schemas.category_schema import (
   CreateCategorySchema,
   UpdateCategorySchema
)

class CategoryController():
   def __init__(self):
      self.model = CategoryModel
      
   def get_all(self):
      try:
         categories = self.model.query.order_by(self.model.id.desc()).all()
         
         return {
            'message': 'Categories fetched successfully',
            'data': [
               category.to_dict() for category in categories
            ]
         }, 200
      except Exception as e:
         return {
            'message': 'An error occurred',
            'error': str(e)
         },500
         
   def get_all_for_clients(self):
      try:
         categories = self.model.query.filter_by(status=True).order_by(self.model.id.desc()).all()
         
         return {
            'message': 'Categorues fetched successfully',
            'data': [
               category.to_dict() for category in categories
            ]
         }, 200
         
      except Exception as e:
         return {
            'message': 'An error occurred',
            'error': str(e)
         }, 500
   
   def create(self, json:dict):
      try:
      
         validated_category = CreateCategorySchema(**json)
         
         new_category = self.model(**validated_category.model_dump())
         
         db.session.add(new_category)
         db.session.commit()
         
         return {
            'message': 'Category created successfully',
            'data': new_category.to_dict(),
         }
         
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
         
   def update(self, id:int, json:dict):
      try:
         validated_category = UpdateCategorySchema(**json)

         category = self.model.query.get(id)
         if category is None:
            return {
               'message': 'Category not found',
            }, 404
            
         category.name = validated_category.name
         category.status = validated_category.status
         db.session.commit()
         return {
            'message': 'Category updated successfully',
            'data': category.to_dict(),
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
         
         category = self.model.query.get(id)
         if category is None:
            return {
               'message': 'Category not found',
            }, 404
            
         category.status = False
         db.session.commit()
         
         return {
            'message': 'Category deleted successfully',
            'data': category.to_dict(),
         }, 200
   
      except Exception as e:
         return {
            'message': 'An error occurred',
            'error': str(e)
         }, 500