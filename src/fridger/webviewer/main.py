from flask import Flask, render_template, request
from fridger.db_driver.config import SessionLocal
from fridger.db_driver.database import init_db
from fridger.db_driver.repository import UserRepository, ProductRepository


init_db()
db = SessionLocal()


app = Flask(__name__)

@app.route('/fridge')
def hello():
    tgid = request.args.get('tgid')
    secret = request.args.get('secret')

    user = UserRepository.get_or_create(
        db=db,
        telegram_id=int(tgid),
    )

    if not user:
        return "Permission denied"
    
    if not secret == user.fridge_password:
        return "Permission denied"
    
    products = ProductRepository.get_products(
        db=db,
        telegram_id=user.telegram_id,
        limit=99999
    )

    return render_template('index.html', products=products)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)