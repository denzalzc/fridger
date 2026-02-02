import subprocess


subprocess.run(['systemctl', 'disable', 'fridge_tgbot'], shell=True)
subprocess.run(['systemctl', 'disable', 'fridge_webviewer'], shell=True)
subprocess.run(['systemctl', 'disable', 'fridge_cron'], shell=True)

subprocess.run(['systemctl', 'stop', 'fridge_tgbot'], shell=True)
subprocess.run(['systemctl', 'stop', 'fridge_webviewer'], shell=True)
subprocess.run(['systemctl', 'stop', 'fridge_cron'], shell=True)

subprocess.run(['rm', '/etc/systemd/system/fridge_tgbot.service'], shell=True)
subprocess.run(['rm', '/etc/systemd/system/fridge_webviewer.service'], shell=True)
subprocess.run(['rm', '/etc/systemd/system/fridge_cron.service'], shell=True)