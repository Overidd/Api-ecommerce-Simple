from db import db
from sqlalchemy import Column, String, Integer, Boolean, DateTime
import datetime
class CategoryModel(db.Model):
   
   __tablename__ = 'category'
   id = Column(Integer, primary_key=True)
   name = Column(String(100))
   status = Column(Boolean, default=True)
   created_at = Column(DateTime, default=datetime.datetime.now)
   updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
   
   def to_dict(self):
      return {
         'id': self.id,
         'name': self.name,
         'status': self.status,
         'created_at': str(self.created_at),
         'updated_at': str(self.updated_at),
      }