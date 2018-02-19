#!/bin/bash
ps aux | grep schnitzelstart.py | cut -b 10-14 | xargs -I {} kill -9 {} > /dev/null 2>&1
ps aux | grep schnitzelstart.py | cut -b 10-14 | xargs -I {} kill -9 {} > /dev/null 2>&1
/usr/bin/python schnitzelstart.py >> /tmp/schnitzel.log 2>&1 &
