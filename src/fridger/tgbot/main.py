import telebot
import re
import os

from datetime import datetime
from termcolor import colored

from telebot.types import Message

from fridger.db_driver.repository import UserRepository, ProductRepository
from fridger.db_driver.config import SessionLocal
from fridger.db_driver.database import init_db

from fridger.logger import FridgeLogger


action_logger = FridgeLogger('tgbot_action.log')
running_logger = FridgeLogger('tgbot_running.log')


current_dir = os.path.dirname(os.path.abspath(__file__))
init_db()
db = SessionLocal()
running_logger.info('DB is inited')

def get_api_key() -> str:
    with open(os.path.join(current_dir, 'apikey.txt'), 'r') as file:
        return str(file.read()).strip()
    
    
def send_to_src(message_src: telebot.types.Message, text: str) -> None:
    bot.send_message(message_src.chat.id, text, parse_mode='html')

def reply_to_src(message_src: telebot.types.Message, text: str) -> None:
    bot.reply_to(message_src, text, parse_mode='html')

def get_user_from_message(m: Message):
    up = m.from_user

    user = UserRepository.get_or_create(
        db=db,
        telegram_id=up.id,
        username=up.username
    )
    return user

def parse_add_command(m: Message) -> dict:
    pattern = r'/add\s+(\S+(?:\s+\S+)*?)\s+([\d.]+)\s+(\d{2}\.\d{2}\.\d{2})'
    user_text = m.text

    match = re.match(pattern, user_text)

    if match:
        title = match.group(1).strip()
        amount = float(match.group(2).strip())
        best_before_date = datetime.strptime(match.group(3).strip(), '%d.%m.%y')


        return {'title': title, 'amount': amount, 'best_before_date': best_before_date}
    
    else: return False

def parse_del_command(m: Message) -> dict:
    pattern = r'/del\s+(\d+)'
    user_text = m.text

    match = re.match(pattern, user_text)

    if match:
        product_id = match.group(1).strip()

        return product_id
    
    else: return False


def simular_to_real(m):
    user = get_user_from_message(m)

    products = ProductRepository.get_products(
        db=db,
        telegram_id=user.telegram_id,
        limit=99999
    )

    number_to_id = {i+1: product.id for i, product in enumerate(products)}

    return number_to_id

def real_to_simular(m):
    user = get_user_from_message(m)

    products = ProductRepository.get_products(
        db=db,
        telegram_id=user.telegram_id,
        limit=99999
    )

    id_to_number = {product.id: i+1 for i, product in enumerate(products)}

    return id_to_number


    

bot = telebot.TeleBot(get_api_key())
print(colored('Bot is UP.', 'green'))
running_logger.info('Bot is inited')


@bot.message_handler(commands=['start'])
def start_command(m: Message):
    user = get_user_from_message(m)
    send_to_src(m, user.id)

    action_logger.info(f"tg_user {user.telegram_id} Start command")


@bot.message_handler(commands=['show'])
def show_command(m: Message):
    user = get_user_from_message(m)

    if not user:
        action_logger.warn(f"tg_user {user.telegram_id} Show command No user user_id:{user.id} tgid:{user.telegram_id}")
        return 0 # TODO:default No user user_id:{user.id} tgid:{user.telegram_id}
    
    products = ProductRepository.get_products(
        db=db,
        telegram_id=user.telegram_id,
    )

    if not products:
        send_to_src(m, 'No products')
        action_logger.info(f"tg_user {user.telegram_id} Show command No products")
        return 0

    real_ids_to_simular = real_to_simular(m)
    
    send_to_src(
        message_src=m,
        text=''.join([f"[{real_ids_to_simular[product.id]}] Title: {product.title} | Count: {product.amount} | BBD: {product.best_before_date.strftime("%d.%m.%Y")}\n" for product in products])
    )

    action_logger.info(f"tg_user {user.telegram_id} Show command succ")
    
@bot.message_handler(commands=['add'])
def add_command(m: Message):
    user = get_user_from_message(m)

    if not user:
        action_logger.warn(f"tg_user {user.telegram_id} Add command No user user_id:{user.id} tgid:{user.telegram_id}")
        return 0 # TODO:default No user user_id:{user.id} tgid:{user.telegram_id}
    

    product_data = parse_add_command(m)
    
    if not product_data:
        send_to_src(m, 'Wrong format. Right: /add milk 1 23.09.26')
        action_logger.info(f"tg_user {user.telegram_id} Add command Wrong /add command format")
        return
    
    product = ProductRepository.add_product(
        db=db,
        telegram_id=user.telegram_id,
        **product_data
    )

    if product:
        send_to_src(m, 'Product added.')

    action_logger.info(f"tg_user {user.telegram_id} Add command succ | Product.id = {product.id}")


@bot.message_handler(commands=['del'])
def delete_command(m: Message):
    user = get_user_from_message(m)

    if not user:
        action_logger.warn(f"tg_user {user.telegram_id} Del command No user user_id:{user.id} tgid:{user.telegram_id}")
        return 0 # TODO:default No user user_id:{user.id} tgid:{user.telegram_id}

    product_id = parse_del_command(m)
    real_id = simular_to_real(m)[int(product_id)]

    if not product_id:
        action_logger.info(f"tg_user {user.telegram_id} Del command Wrong /del command format")
        send_to_src(m, 'Wrong format. Right: /del 23(id)')
        return
    
    delete_product = ProductRepository.delete(
        db=db,
        telegram_id=user.telegram_id,
        product_id=int(real_id)
    )

    if not delete_product:
        action_logger.info(f"tg_user {user.telegram_id} Del command Non-existing product ID")
        send_to_src(m, 'This ID not exists, try again and user /show command to lookup')
        return
    
    send_to_src(m, f'Product {product_id} deleted')
    action_logger.info(f"tg_user {user.telegram_id} Del command Succ | product.id = {real_id}")


@bot.message_handler(commands=['web'])
def web_command(m: Message):
    user = get_user_from_message(m)

    if not user:
        action_logger.warn(f"tg_user {user.telegram_id} Web command No user user_id:{user.id} tgid:{user.telegram_id}")
        return 0 # TODO:default No user user_id:{user.id} tgid:{user.telegram_id} user_id:{user.id} tgid:{user.telegram_id}


    send_to_src(
        message_src=m,
        text=f"http://77.222.63.95:5000/fridge?tgid={user.telegram_id}&secret={user.fridge_password}"
    )
    
    action_logger.info(f"tg_user {user.telegram_id} Web command Succ")


bot.infinity_polling()