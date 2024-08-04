from db import db
from sqlalchemy import Column, String, Integer, Boolean, Float, DateTime
from sqlalchemy.orm import relationship
import datetime

class OrderModel(db.Model):
   __tablename__ = 'orders'
   id = Column(Integer, primary_key=True)
   code = Column(String(100))
   client_name = Column(String(200))
   client_last_name = Column(String(200))
   client_address = Column(String(200))
   client_documents_number = Column(String(100))
   total = Column(Float)
   status = Column(Boolean, default=True)
   created_at = Column(DateTime, default=datetime.datetime.now)
   updated_at = Column(DateTime, default=datetime.datetime.now, onupdate= datetime.datetime.now)
   
   order_details = relationship('OrderDetailModel')
                             
                             
   def to_dict(self):
      return {
         'id': self.id,
         'code': self.code,
         'client_name': self.client_name,
         'client_last_name': self.client_last_name,
         'client_address': self.client_address,
         'client_documents_number': self.client_documents_number,
         'total': self.total,
         'status': self.status,
         'created_at': str(self.created_at),
         'updated_at': str(self.updated_at),
         'order_details': [detail.to_dict() for detail in self.order_details]
      }