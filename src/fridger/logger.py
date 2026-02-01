import os
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(current_dir, '..', '..', 'logs')

if not os.path.exists(LOGS_DIR):
    os.mkdir(LOGS_DIR)


class FridgeLogger:
    def __init__(self, filename):
        self.filename = filename

        log_file_path = os.path.join(LOGS_DIR, self.filename)
        if not os.path.exists(log_file_path):
            with open(f"{LOGS_DIR}/{self.filename}", 'w') as file:
                file.close()

    

    def info(self, text):
        with open(f"{LOGS_DIR}/{self.filename}", 'a') as file:
            file.write(f"[INFO] [{datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}]: {text}\n")

    def warn(self, text):
        with open(f"{LOGS_DIR}/{self.filename}", 'a') as file:
            file.write(f"[WARN] [{datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}]: {text}\n")

    def fatal(self, text):
        with open(f"{LOGS_DIR}/{self.filename}", 'a') as file:
            file.write(f"[FATAL] [{datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}]: {text}\n")

    def debug(self, text):
        with open(f"{LOGS_DIR}/{self.filename}", 'a') as file:
            file.write(f"[DEBUG] [{datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}]: {text}\n")

