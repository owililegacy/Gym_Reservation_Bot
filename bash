#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

sudo apt-get update
sudo apt-get install -y firefox-esr python3-venv python3-pip cron

python3 -m venv venv
source venv/bin/activate
pip install -U pip wheel
pip install -r requirements.txt

# add cron job for 11:00 AM every day
(crontab -l 2>/dev/null; echo "0 11 * * * cd $(pwd) && ./venv/bin/python $(pwd)/bot.py >> ~/gym-bot-cron.log 2>&1") | crontab -

echo "Installed.  Cron will run the bot at 11:00 AM daily."
echo "Logs: ~/gym-bot.log (bot)  &  ~/gym-bot-cron.log (cron wrapper)"


Quick start guide:
git clone <your-repo> gym-bot
cd gym-bot
chmod +x install.sh
./install.sh

# test manually once
source venv/bin/activate
python bot.py


cheetsheet for cron syntax:
# see cron jobs
crontab -l

# run right now for a test
cd ~/gym-bot && ./venv/bin/python bot.py

# live logs
tail -f ~/gym-bot.log
tail -f ~/gym-bot-cron.log