from db import db
from sqlalchemy import Column, String, Integer, Boolean, Text, Float,DateTime, ForeignKey
import datetime

import utils.config_cloudinary
import cloudinary.utils

class ProductModel(db.Model):
   __tablename__ = 'products'
   
   id = Column(Integer, primary_key=True)
   name = Column(String(200))
   code = Column(String(100))
   image = Column(Text)
   brand = Column(String(100))
   description = Column(Text)
   size = Column(String(100))
   price = Column(Float)
   status = Column(Boolean, default=True)
   stock = Column(Integer)
   created_at = Column(DateTime, default=datetime.datetime.now)
   updated_at = Column(DateTime, default=datetime.datetime.now, onupdate= datetime.datetime.now)
   category_id = Column(Integer, ForeignKey('category.id'))
   
   def to_dict(self):
      return {
         'id': self.id,
         'name': self.name,
         'code': self.code,
         'image': cloudinary.utils.cloudinary_url(self.image, secure=True)[0],
         'brand': self.brand,
         'description': self.description,
         'price': self.price,
         'status': self.status,
         'category_id': self.category_id,
         'created_at': str(self.created_at),
         'updated_at': str(self.updated_at),
      }
   