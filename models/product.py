
from sqlalchemy import Column, String, Float
from sqlalchemy_utils import UUIDType
import uuid

from .base import Base

class Product(Base):
    __tablename__ = 'products'
    id = Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)