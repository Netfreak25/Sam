#!/bin/bash
if [ "$1" != "" ]; then
        export mydir=$1
        cd $mydir
else
        export mydir="./"
fi

if [ "$2" = "sudo-test" ]; then
  exit 0
fi

sleep 0.5
if [ !  -f start-bot.py ]; then
    echo "Aborting!"
    echo "Working Directory is wrong! Please cd into the sam directory or provide the path as first input parameter!"
    exit 1
fi

export PORT=`cat config.ini | grep port | cut -b 16-`

chmod 777 /tmp/sam-gui.log
chmod 777 /tmp/sam.log
chmod 777 /tmp/sam-update.log
chmod 777 /tmp/sam-bot.pid
chmod 777 /tmp/sam-gui.pid

# setup restart button for gui
sudo -u nobody timeout --foreground 1 sudo --non-interactive ./start.sh $mydir sudo-test >/dev/null 2>&1 && touch htbin/.sudo >/dev/null 2>&1 || rm htbin/.sudo >/dev/null 2>&1

export username=`whoami`
chown -R nobody:$username ./*
chown -R nobody:$username .
if [ -f .autoupdate ]; then
	echo -ne "[0/4] Updating SAM via git pull"
	git pull > /tmp/sam-update.log 2>&1 && echo -ne "\\r[0/4] Updating SAM via git pull - SUCCESS" || echo -ne "\\r[0/4] Updating SAM via git pull - FAILED"
	echo
fi

echo -ne "[1/4] Killing old Bot Instance"
ps aux | grep start-bot.py | cut -b 10-14 | xargs -I {} kill -9 {} > /dev/null 2>&1
ps aux | grep start-bot.py | cut -b 10-14 | xargs -I {} kill -9 {} > /dev/null 2>&1
ps aux | grep start-bot.py | cut -b 10-14 | xargs -I {} kill -9 {} > /dev/null 2>&1
ps aux | grep start-bot.py | cut -b 10-14 | xargs -I {} kill -9 {} > /dev/null 2>&1

export pid=`cat /tmp/sam-bot.pid`
if ! kill -0 $pid > /dev/null 2>&1; then
    echo -ne "\\r[1/4] Killing old Bot Instance - SUCCESS"
else
    echo -ne "\\r[1/4] Killing old Bot Instance - FAILED"
fi
echo
echo -ne "[2/4] Starting Bot Instance"
`sudo -u nobody /usr/bin/python start-bot.py >> /tmp/sam.log 2>&1 & echo $! > /tmp/sam-bot.pid`

export pid=`sleep 2 && cat /tmp/sam-bot.pid`
if ! kill -0 $pid > /dev/null 2>&1; then
    echo -ne "\\r[2/4] Starting Bot Instance - FAILED"
else
	echo -ne "\\r[2/4] Starting Bot Instance - SUCCESS"
fi
echo
echo -ne "[3/4] Killing old WebGui Instance"
ps aux | grep start-gui.py | cut -b 10-14 | xargs -I {} kill -9 {} > /dev/null 2>&1
ps aux | grep start-gui.py | cut -b 10-14 | xargs -I {} kill -9 {} > /dev/null 2>&1
ps aux | grep start-gui.py | cut -b 10-14 | xargs -I {} kill -9 {} > /dev/null 2>&1
ps aux | grep start-gui.py | cut -b 10-14 | xargs -I {} kill -9 {} > /dev/null 2>&1

export pid=`cat /tmp/sam-gui.pid`
if ! kill -0 $pid > /dev/null 2>&1; then
    echo -ne "\\r[3/4] Killing old WebGui Instance - SUCCESS"
else
    echo -ne "\\r[3/4] Killing old WebGui Instance - FAILED"
fi
echo
echo -ne "[4/4] Starting WebGui Instance"

export check=`netstat -tulpen | grep $PORT`
export count=0

while [ "$check" != "" ]; do
  sleep 1
  fuser -k -n tcp $PORT > /dev/null 2>&1
  let "count=count+1"
  export check=`netstat -tulpen | grep $PORT`
  if [ "$count" -eq 10 ]; then
    break
  fi

done

`sudo -u nobody /usr/bin/python start-gui.py >> /tmp/sam-gui.log 2>&1 & echo $! > /tmp/sam-gui.pid`

export pid=`sleep 2 && cat /tmp/sam-gui.pid`
if ! kill -0 $pid > /dev/null 2>&1; then
    echo -ne "\\r[4/4] Staring WebGui Instance - FAILED"
else
    echo -ne "\\r[4/4] Staring WebGui Instance - SUCCESS"
fi
echo

echo
echo "SAM has been updated and restarted!"
