import subprocess


subprocess.run(['systemctl', 'daemon-reload'])

subprocess.run(['systemctl', 'disable', 'fridge_tgbot'])
subprocess.run(['systemctl', 'disable', 'fridge_webviewer'])
subprocess.run(['systemctl', 'disable', 'fridge_cron'])

subprocess.run(['systemctl', 'stop', 'fridge_tgbot'])
subprocess.run(['systemctl', 'stop', 'fridge_webviewer'])
subprocess.run(['systemctl', 'stop', 'fridge_cron'])

subprocess.run(['rm', '/etc/systemd/system/fridge_tgbot.service'])
subprocess.run(['rm', '/etc/systemd/system/fridge_webviewer.service'])
subprocess.run(['rm', '/etc/systemd/system/fridge_cron.service'])