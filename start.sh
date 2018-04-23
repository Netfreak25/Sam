#!/bin/bash
echo "Updating SAM via git pull"
echo "(this may take a while)"
git pull > /tmp/sam-update.log 2>&1
echo
echo "Killing old Bot Instance"
ps aux | grep start-bot.py | cut -b 10-14 | xargs -I {} kill -9 {} > /dev/null 2>&1
ps aux | grep start-bot.py | cut -b 10-14 | xargs -I {} kill -9 {} > /dev/null 2>&1
echo "Starting Bot Instance"

/usr/bin/python start-bot.py >> /tmp/sam.log 2>&1 &
echo "Killing old WebGui Instance"

ps aux | grep start-gui.py | cut -b 10-14 | xargs -I {} kill -9 {} > /dev/null 2>&1
ps aux | grep start-gui.py | cut -b 10-14 | xargs -I {} kill -9 {} > /dev/null 2>&1
echo "Staring WebGui Instance"
/usr/bin/python start-gui.py >> /tmp/sam-gui.log 2>&1 &
echo "SAM has been updated and restarted"