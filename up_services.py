import os
import subprocess

'''
Auto deploy componetns on linux machine
'''

def gen_service(service_name, work, bin, exec):
    with open(f'services/{service_name}', 'r') as serv_file:
        text = serv_file.read()
        
        work_dir = os.path.abspath(work)
        python_bin = os.path.abspath(bin)
        exec_file = os.path.abspath(exec)

        text = text \
        .replace('%workdir%', work_dir) \
        .replace('%pythonbin%', python_bin) \
        .replace('%execfile%', exec_file)

        return text

tg_bot = gen_service(
    'fridge_tgbot.service',
    'src/fridger/tgbot',
    'venv/bin/python',
    'src/fridger/tgbot/main.py'
)
with open('/etc/systemd/system/fridge_tgbot.service', 'w') as file:
    file.write(tg_bot)
web_viever = gen_service(
    'fridge_webviewer.service',
    'src/fridger/webviewer',
    'venv/bin/python',
    'src/fridger/webviewer/main.py'
)
with open('/etc/systemd/system/fridge_webviewer.service', 'w') as file:
    file.write(web_viever)
cron = gen_service(
    'fridge_cron.service',
    'src/fridger/cron_product',
    'venv/bin/python',
    'src/fridger/cron/main.py'
)
with open('/etc/systemd/system/fridge_cron.service', 'w') as file:
    file.write(cron)


subprocess.run(['cp', '/home/apikey.txt', f'{os.path.abspath('src/fridger/tgbot')}/apikey.txt'])

subprocess.run(['systemctl', 'start', 'fridge_tgbot'])
subprocess.run(['systemctl', 'enable', 'fridge_tgbot'])

subprocess.run(['systemctl', 'start', 'fridge_webviewer'])
subprocess.run(['systemctl', 'enable', 'fridge_webviewer'])

subprocess.run(['systemctl', 'start', 'fridge_cron'])
subprocess.run(['systemctl', 'enable', 'fridge_cron'])
