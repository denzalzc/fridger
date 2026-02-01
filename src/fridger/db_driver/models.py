from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from fridger.db_driver.config import Base
from fridger.db_driver.contrib_db import now

import secrets, string


def generate_password(length=8):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=1)
    telegram_id = Column(Integer, nullable=0, index=1, unique=1)
    username = Column(String(100), nullable=1)
    created_at = Column(DateTime, default=lambda: now())

    fridge_password = Column(String(100), default=generate_password)

    products = relationship('Product', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
            return f"<User(id={self.id}, telegram_id={self.telegram_id})>"         


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=1)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=0, index=1)
    user = relationship('User', back_populates='products')

    title = Column(Text, nullable=1)
    amount = Column(Float, nullable=0)

    created_at = Column(DateTime, default=now())
    

    best_before_date = Column(DateTime, default=now())

    def __repr__(self):
        return f"<Product(id={self.id}, bestbefore={self.amount})>"
    
    


    