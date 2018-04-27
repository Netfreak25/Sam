#!/bin/bash
sleep 0.5
cd /sam/
if [ !  -f start-bot.py ]; then
    echo "Aborting!"
    echo "Working Directory is wrong! Please modify start.sh and correct the second line!"
    exit 1
fi
chmod 777 /tmp/sam-gui.log
chmod 777 /tmp/sam.log
chmod 777 /tmp/sam-update.log

export username=`whoami`
chown -R nobody:$username ./*

echo -ne "[1/5] Updating SAM via git pull"
git pull > /tmp/sam-update.log 2>&1
echo -ne "\\r[1/5] Updating SAM via git pull - DONE"
echo
echo -ne "[2/5] Killing old Bot Instance"
ps aux | grep start-bot.py | cut -b 10-14 | xargs -I {} kill -9 {} > /dev/null 2>&1
ps aux | grep start-bot.py | cut -b 10-14 | xargs -I {} kill -9 {} > /dev/null 2>&1
ps aux | grep start-bot.py | cut -b 10-14 | xargs -I {} kill -9 {} > /dev/null 2>&1
ps aux | grep start-bot.py | cut -b 10-14 | xargs -I {} kill -9 {} > /dev/null 2>&1

export pid=`cat /tmp/sam-bot.pid` 
if ! kill $pid > /dev/null 2>&1; then
    echo -ne "\\r[2/5] Killing old Bot Instance - SUCCESS"
else
    echo -ne "\\r[2/5] Killing old Bot Instance - FAILED"
fi
echo
echo -ne "[3/5] Starting Bot Instance"
`sudo -u nobody /usr/bin/python start-bot.py >> /tmp/sam.log 2>&1 & echo $! > /tmp/sam-bot.pid`

export pid=`cat /tmp/sam-bot.pid` 
if ! kill $pid > /dev/null 2>&1; then
    echo -ne "\\r[3/5] Starting Bot Instance - FAILED"
else
	echo -ne "\\r[3/5] Starting Bot Instance - SUCCESS"
fi
echo
echo -ne "[4/5] Killing old WebGui Instance"
ps aux | grep start-gui.py | cut -b 10-14 | xargs -I {} kill -9 {} > /dev/null 2>&1
ps aux | grep start-gui.py | cut -b 10-14 | xargs -I {} kill -9 {} > /dev/null 2>&1
ps aux | grep start-gui.py | cut -b 10-14 | xargs -I {} kill -9 {} > /dev/null 2>&1
ps aux | grep start-gui.py | cut -b 10-14 | xargs -I {} kill -9 {} > /dev/null 2>&1

export pid=`cat /tmp/sam-gui.pid` 
if ! kill $pid > /dev/null 2>&1; then
    echo -ne "\\r[4/5] Killing old WebGui Instance - SUCCESS"
else
    echo -ne "\\r[4/5] Killing old WebGui Instance - FAILED"
fi
echo
echo -ne "[5/5] Staring WebGui Instance"
`sudo -u nobody /usr/bin/python start-gui.py >> /tmp/sam-gui.log 2>&1 & echo $! > /tmp/sam-gui.pid`
export pid=`cat /tmp/sam-gui.pid` 
if ! kill $pid > /dev/null 2>&1; then
    echo -ne "\\r[5/5] Staring WebGui Instance - FAILED"
else
    echo -ne "\\r[5/5] Staring WebGui Instance - SUCCESS"
fi
echo

echo
echo "SAM has been updated and restarted!"