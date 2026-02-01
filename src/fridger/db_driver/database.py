from fridger.db_driver.config import engine, Base
from termcolor import colored


def init_db():
    Base.metadata.create_all(bind=engine)
    print(colored('DB is inizilised!', 'green'))

def drop_db():
    Base.metadata.drop_all(bind=engine)
    print(colored('DB is dropped!', 'green'))

# drop_db()