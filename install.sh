#!/bin/bash
set -euo pipefail
cd ~

# 1. system deps
sudo apt-get update
sudo apt-get install -y python3-venv python3-pip chromium-browser unzip

# 2. python venv
python3 -m venv gymbot-env
source gymbot-env/bin/activate
pip install -U pip wheel
pip install -r requirements.txt

# 3. systemd service
sudo cp gym-bot.service /etc/systemd/system/
sudo cp gym-bot.timer   /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now gym-bot.timer

# 4. log file
sudo touch /var/log/gym-bot.log
sudo chown $USER /var/log/gym-bot.log

echo "Install complete.  Timer will trigger at 11:00 AM daily."