from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy_utils import UUIDType
import uuid
from .base import Base

class Coupon(Base):
    __tablename__ = 'coupons'
    id = Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    code = Column(String(20), unique=True, nullable=False)
    nth_order = Column(Float, unique=False, nullable=False)
    discount_percent = Column(Float, nullable=False)