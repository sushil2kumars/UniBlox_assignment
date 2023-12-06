
from sqlalchemy import Column, String, Float, ForeignKey
from datetime import datetime, timedelta
from sqlalchemy import Column, String, Float, DateTime, ForeignKey,Integer
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
import uuid

from .base import Base
class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUIDType(binary=False), ForeignKey('users.id'), nullable=False)
    total_amount = Column(Float, nullable=False)
    discount_code = Column(String(20), ForeignKey('coupons.code'), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    products = relationship('OrderProduct', back_populates='order')

class OrderProduct(Base):
    __tablename__ = 'product_orders'
    id = Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    order_id = Column(UUIDType(binary=False), ForeignKey('orders.id'))
    product_id = Column(UUIDType(binary=False), ForeignKey('products.id'))
    quantity = Column(Integer, default=1)
    order = relationship('Order', back_populates='products')
    product = relationship('Product')

