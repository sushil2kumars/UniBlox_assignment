


from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
import uuid

from .base import Base

class Cart(Base):
    __tablename__ = 'cart'
    id = Column(String(36), default=str(uuid.uuid4()), primary_key=True)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    

class CartProduct(Base):
    __tablename__ = 'cart_product'
    cart_id = Column(String(36), ForeignKey('cart.id'), primary_key=True)
    product_id = Column(String(36), ForeignKey('products.id'), primary_key=True)
    quantity = Column(Float, default=1.0)
    product = relationship('Product')
    cart = relationship('Cart')