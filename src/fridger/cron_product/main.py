from fridger.db_driver.config import SessionLocal
from fridger.db_driver.database import init_db
from fridger.db_driver.repository import UserRepository, ProductRepository
from fridger.db_driver.models import User, Product
from fridger.logger import FridgeLogger

from datetime import datetime

import requests
import os
import time
import schedule


action_logger = FridgeLogger('cron_action.log')
running_logger = FridgeLogger('cron_running.log')


current_dir = current_dir = os.path.dirname(os.path.abspath(__file__))
path_to_apikey = os.path.join(current_dir, '../tgbot/apikey.txt')

if os.path.exists(path_to_apikey):
    with open(path_to_apikey, 'r') as file:
        APIKEY = file.read().strip()
        running_logger.info('Got APIKEY for bot')
else:
    running_logger.fatal(f'No apikey file at {path_to_apikey}. Aborting')
    raise f'No apikey file at {path_to_apikey}'

def send_message_to_user(telegram_id: int, message: str):
    url = f"https://api.telegram.org/bot{APIKEY}/sendMessage"
    payload = {
        'chat_id': telegram_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        action_logger.info(f"Expire info sent to {telegram_id}")
    except requests.exceptions.RequestException as e:
        action_logger.fatal(f"Error on sending expired date to {telegram_id}: {e}")


def notif_user(db, product: Product, message: str):
    user = UserRepository.get_or_create(
        db=db,
        telegram_id=product.user.telegram_id
    )

    send_message_to_user(
        telegram_id=user.telegram_id,
        message=f"Product ID[{product.id}]: {product.title}\n{message}"
    )
    
    return True

def check_products():
    db = SessionLocal()
    running_logger.info('DB is inited')

    time.sleep(5)
    all = db.query(Product).all()

    today = datetime.now()

    for product in all:
        bbd = product.best_before_date

        days_left = (bbd.date() - today.date()).days

        if days_left == 1:
            notif_user(
                db,
                product,
                f"\n{"!"*40}\nwill expire tomorrow\n{"!"*40}"
            )
        elif days_left == 2:
            notif_user(db, product, 'will expire the day after tomorrow')
        elif days_left < 1:
            notif_user(db, product, 'is EXPIRED')
        
    db.close()

def main():
    schedule.every().day.at("11:55").do(check_products)
    running_logger.info('Cron is ran.')

    while True:
        schedule.run_pending()
        print('peng')
        time.sleep(5)


if __name__ == "__main__":
    main()