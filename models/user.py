import uuid
from datetime import datetime, timedelta
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy_utils import UUIDType
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from .base import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    role = Column(String(10), nullable=False, default='enduser')  # 'enduser' or 'admin'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_jwt(self, expiration=3600):
        payload = {
            'user_id': str(self.id),
            'exp': datetime.utcnow() + timedelta(seconds=expiration)
        }
        return jwt.encode(payload, 'your_secret_key', algorithm='HS256')