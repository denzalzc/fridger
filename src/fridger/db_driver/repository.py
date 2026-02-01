from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from datetime import datetime, UTC, timezone

from fridger.db_driver.models import User, Product
from fridger.db_driver.contrib_db import now
from termcolor import colored


class UserRepository:

    @staticmethod
    def get_or_create(db: Session, telegram_id: int, **kwargs):
        user = db.query(User).filter(User.telegram_id == telegram_id).first()

        if not user:
            user_data = {
                'telegram_id': telegram_id,
                'created_at': now(),
                **kwargs
            }
            user = User(**user_data)
            db.add(user)
            db.commit()
            db.refresh(user)
        return user
    
    @staticmethod
    def get_user(db: Session, telegram_id: int):
        return db.query(User).filter(User.telegram_id == telegram_id).first()
        

class ProductRepository:

    @staticmethod
    def add_product(db: Session, telegram_id: int, amount: float, title: str, best_before_date):
        user = UserRepository.get_user(db, telegram_id)

        if not user:
            raise ValueError(f"User with t-id {telegram_id} not exists")

        product = Product(
            user_id=user.id,
            amount=amount,
            title=title,
            best_before_date=best_before_date,
        )

        db.add(product)
        db.commit()
        db.refresh(product)

        return product

    @staticmethod
    def get_products(db: Session, telegram_id: int, limit: int = 10) -> list:
        user = UserRepository.get_user(db, telegram_id)

        if not user:
            return []


        products = db.query(Product)\
            .filter(Product.user_id == user.id)\
            .order_by(Product.created_at)\
            .limit(limit)\
            .all()

        return products
    
    @staticmethod
    def delete(db: Session, telegram_id: int, product_id: int) -> bool:
        try:
            user = UserRepository.get_user(db=db, telegram_id=telegram_id)

            if not(user):
                print(colored((f'User with t-id {telegram_id} not exists'), 'red'))
                return 0

            product = db.query(Product)\
                .filter(Product.id == product_id)\
                .filter(Product.user_id == user.id)\
                .first()
            if not (product):
                print(colored((f'Product with ID {product_id} not found in user with t-id {telegram_id}'), 'red'))
                return 0
        
            db.delete(product)
            db.commit()
            return True
        
        except Exception as e:
            print(e)
            print(colored((f'Error on deleting product(id={product_id}, user_id={user.id})'), 'red'))
            db.rollback()
            return 0
        