#!/bin/bash
echo "[1/5] Updating SAM via git pull"
echo "(this may take a while)"
git pull > /tmp/sam-update.log 2>&1

echo "[2/5] Killing old Bot Instance"
ps aux | grep start-bot.py | cut -b 10-14 | xargs -I {} kill -9 {} > /dev/null 2>&1
ps aux | grep start-bot.py | cut -b 10-14 | xargs -I {} kill -9 {} > /dev/null 2>&1

echo "[3/5] Starting Bot Instance"
/usr/bin/python start-bot.py >> /tmp/sam.log 2>&1 &

echo "[4/5] Killing old WebGui Instance"
ps aux | grep start-gui.py | cut -b 10-14 | xargs -I {} kill -9 {} > /dev/null 2>&1
ps aux | grep start-gui.py | cut -b 10-14 | xargs -I {} kill -9 {} > /dev/null 2>&1

echo "[5/5] Staring WebGui Instance"
/usr/bin/python start-gui.py >> /tmp/sam-gui.log 2>&1 &

echo
echo "SAM has been updated and restarted!"