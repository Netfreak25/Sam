
# SAM - Eine Telegram Schnitzeljagd

![Python 2.7](https://img.shields.io/badge/python-2.7-blue.svg)

A Telegram Game Bot that lets you create a paper chase game for your friends and family

## Features:
* Creating Waypoints
* Set distance radius per Waypoint
* Creating seperated Item Waypoints
* Set distance radius per Item
* Set Pickup Chance per Item
* Waypoint Interaction (Questions, Picture, Video, Audio, Voice)
* Name Waypoints
* Save/load your Paper Chase
* Invincible Mode (you can't die)
* Android Trigger App available, to trigger remote sounds
* German language
* Customize most of the Text via DB
* Finding a lot of useless Items
* Showing Inventory
* Finding Revive Items
* Finding Traps (which kill you)
* Dropping Items on death
* Dropping Items from Inventory
* Showing Stats (Points in Invincible Mode)
* Telegram Location manipulation prevented

## Installation:
### Ubuntu/Debian:
* Clone SAM
```
git clone https://github.com/Netfreak25/Sam.git
```

* Change Directory
```
cd Sam
```

* Install Ubuntu/debian Dependencies
```
apt-get install python python-pip mysql-server python-mysqldb curl sudo net-tools
```

* Update pip via pip
```
pip install --upgrade pip
```

* Install python dependencies via pip
```
pip install -r requirements.txt
```

* Create your Database and User

* Table Structure and Data will be imported on first run, don't care about that!

## Configuration:
* Copy config.ini.example to config.ini

* Configure your DB credentials in the config.ini

* Make sure you have setup a telegram bot in botfather @BotFather and you got the access token for the config

* Make sure you have got a google maps api key (You can get it here: https://developers.google.com/maps/documentation/javascript/get-api-key?hl=de)

* Enable the Google JavaScript API for your API-Key (Here: https://console.developers.google.com/apis/library/maps-backend.googleapis.com/?q=java&id=fd73ab50-9916-4cde-a0f6-dc8be0a0d425)

* Configure the rest of the config.ini later via the config.ini overwrite in the web gui!

## Config.ini / Config.ini overwrite
* You can set the following option directly within the config.ini
* But if you set a variable in the gui it will overwrite the one read from config.ini
```

advanced = 0
# Shows Trigger Settings - 0,1

botname = SamsqueshBot
# Name of the Bot in Telegram
cheat_detection = 0
# Only for Android - 0,1

extra_distance_m = 20
# Default Item Radius (m) - 10,20,30,40,50...

gmaps_key = AIzaSyB6zX4HGU0VAVulNasdadssadasdasdasda
# Your Gmaps API Key

invincible = 1
# Defines if you can die - 0,1

pagename = Schnitzeljagdt
# WebGui Title (No spaces allowed)

reset_minutes = 1
# Time until the Trigger can be retriggered - 1+

telegram_token = 78954796:AGHJSGAJHSGGJHGJIOPHJ-787987sad
# Your Telegram Bot Token

trigger_distance_m = 30
# Default Waypoint Radius (m) - 10,20,30,40,50...

zoom_koordinaten = 50.099570,8.675232
# Default coordinates for the map to center (no spaces allowed)

zoom_level = 16
# Default zoom level for the map - 1+
```
* Variables saved in the gui will be saved per Project

## Optional
* If you want to use the restart function from within the gui please also follow the next step

* In Order to be able to use the restart function you have to adjust your /etc/sudoers file
```
nobody ALL=(ALL:ALL) NOPASSWD: /YOURPATH/start.sh
```



## Usage for Bot:
python start-bot.py

## Usage for Gui:
python start-gui.py

## Quick and dirty usage (background bot and gui):
./start.sh

## F.A.Q.
* If your output of start.sh looks like this, make sure you have setup a correct Telegram Bot Token

```
[1/4] Killing old Bot Instance - SUCCESS
[2/4] Starting Bot Instance - FAILED
[3/4] Killing old WebGui Instance - SUCCESS
[4/4] Staring WebGui Instance - SUCCESS
```

* If the Map does not display, make sure you have setup a correct google api key and that the javascript api has been enabled

* If the restart Button does not work in the GUI make sure you updated /etc/sudoers

* If you messed up the project or the config.ini overwrite you can clean the database
```
python start-bot.py -cd
```


## General Informations:
* No guaranteed Support
* Things might break due to changes in the Telegram API