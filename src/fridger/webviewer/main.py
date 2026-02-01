from flask import Flask, render_template, request
from fridger.db_driver.config import SessionLocal
from fridger.db_driver.database import init_db
from fridger.db_driver.repository import UserRepository, ProductRepository
from fridger.logger import FridgeLogger


action_logger = FridgeLogger('webviewer_action.log')
running_logger = FridgeLogger('webviewer_running.log')


init_db()
db = SessionLocal()
running_logger.info('DB is inited')


app = Flask(__name__)
running_logger.info('Flask App is inited')

@app.route('/fridge')
def hello():
    tgid = request.args.get('tgid')
    secret = request.args.get('secret')

    user = UserRepository.get_or_create(
        db=db,
        telegram_id=int(tgid),
    )

    if not user:
        running_logger.warn(f'Got: tg_id{tgid} No User Found!')
        return "Permission denied"
    
    if not secret == user.fridge_password:
        running_logger.warn('Got: tg_id{tgid} Wrong creds!')
        return "Permission denied"
    
    products = ProductRepository.get_products(
        db=db,
        telegram_id=user.telegram_id,
        limit=99999
    )

    running_logger.info('Got: tg_id{tgid} Return page')
    return render_template('index.html', products=products)


if __name__ == '__main__':
    running_logger.info('Staring Flask App')
    app.run(host='0.0.0.0', port=5000, debug=True)