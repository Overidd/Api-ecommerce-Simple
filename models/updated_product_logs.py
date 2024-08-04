from db import db
from sqlalchemy import Column, Integer, DateTime, ForeignKey
import datetime
class updateProductLogs(db.Model):
   __tablename__ = 'update_product_logs'
   
   user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
   product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
   created_at = Column(DateTime, default=datetime.datetime.now)