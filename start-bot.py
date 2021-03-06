#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author: Moritz Kuhn

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import telegram, json
import logging, MySQLdb, time, os, math, random, sys, emoji
from datetime import datetime, timedelta
from s2sphere import LatLng
from emoji import emojize


### Konfiguration laden / do not change
configfile = "./config.ini"
f = open(configfile, 'r')
configdb = {}

def getconfig(a):
    if len(configdb) == 0:
        for i in f:
            if i[0] != "#":
                x = i[:-1]
                y = x.split()
                if len(y) > 0:
                    configdb[y[0]] = y[2]
        return configdb[a]
    else:
        return configdb[a]

sam_host = str(getconfig('sam_host'))
sam_db = str(getconfig('sam_db'))
sam_db_user = str(getconfig('sam_db_user'))
sam_db_pw = str(getconfig('sam_db_pw'))


def cleanDatabase():
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = "DELETE FROM config WHERE 1;"
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e:
        print e
        try:
            db6.close()
        except:
            pass
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = "DELETE FROM waypoints WHERE 1;"
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e:
        print e
        try:
            db6.close()
        except:
            pass
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = "DELETE FROM extra_waypoints WHERE 1;"
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e:
        print e
        try:
            db6.close()
        except:
            pass

    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = "DELETE FROM user WHERE 1;"
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e:
        print e
        try:
            db6.close()
        except:
            pass

    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = "DELETE FROM trigger_clients WHERE 1;"
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e:
        print e
        try:
            db6.close()
        except:
            pass

try:
    for i in sys.argv:
        if (str(i) == "--clean-database") or (str(sys.argv[1]) == "-cd"):
            cleanDatabase()
            print "Database has been cleanen. Please restart without -cd/--clean-database parameter"
            sys.exit()
except Exception, e:
    print e

def importDBfromFile(filename):
    db = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
    cursor = db.cursor()
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            cursor.execute(command)
        except Exception, msg:
            print "Command skipped: ", msg
    db.close()

def verifyDB():
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """SELECT text FROM deathreason WHERE id = 0"""
        cursor6.execute(command6)
        data = cursor6.fetchall()
        db6.close()
    except Exception, e:
        importDBfromFile("structure.sql")


verifyDB()

def addDBConfig():
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """SELECT * FROM config"""
        cursor6.execute(command6)
        data = cursor6.fetchall()
        db6.close()
        for i in data:
            configdb.update({str(i[0].encode('utf-8')): str(i[1].encode('utf-8'))})
    except Exception, e:
        print e

addDBConfig()

telegram_token = str(getconfig('telegram_token'))


try:
    waypoint_radius_m = int(getconfig('waypoint_radius_m'))
except:
    waypoint_radius_m = 30

try:
    invincible = int(getconfig('invincible'))
except:
    invincible = 0

try:
    item_radius_m = int(getconfig('item_radius_m'))
except:
    item_radius_m = 20

try:
    cheat_detection = int(getconfig('cheat_detection'))
except:
    cheat_detection = 0

try:
    broadcast_death = int(getconfig('broadcast_death'))
except:
    broadcast_death = 1


try:
    temp_admin_chatids = str(getconfig('admin_chatids'))
    admin_chatids = []
    for i in temp_admin_chatids.split(","):
        admin_chatids.append(str(i).strip())
except:
    admin_chatids = [ ]


try:
# Load Telegram Token
    updater = Updater(token=telegram_token)
    dispatcher = updater.dispatcher
except:
    print "Your Telegram token is wrong!"
    sys.exit()


def writefile(filename, text):
   filename = str(filename)
   text = str(text).encode("UTF-8")
   f = open(filename, 'w')
   f.write(text) 
   f.close()


def write_telegram_files():
    telegram_directory = "Telegram"

    if not os.path.exists("./"+telegram_directory):
      os.makedirs(telegram_directory)

    file1 = "Telegram/sendTelegramAudioSam"
    file2 = "Telegram/sendTelegramPicSam"
    file3 = "Telegram/sendTelegramVideoSam"
    file4 = "Telegram/sendTelegramVoiceSam"


    content_file1 = """#!/bin/bash
    curl -X  POST "https://api.telegram.org/bot"""+telegram_token+"""/sendChatAction" -F chat_id=$1 -F action=upload_audio> /dev/null 2>&1
    curl -X  POST "https://api.telegram.org/bot"""+telegram_token+"""/sendAudio" -F chat_id=$1 -F audio="@$2" > /dev/null 2>&1"""

    content_file2 = """#!/bin/bash
    curl -X  POST "https://api.telegram.org/bot"""+telegram_token+"""/sendChatAction" -F chat_id=$1 -F action=upload_photo> /dev/null 2>&1
    curl -X  POST "https://api.telegram.org/bot"""+telegram_token+"""/sendPhoto" -F chat_id=$1 -F photo="@$2" > /dev/null 2>&1"""

    content_file3 = """#!/bin/bash
    curl -X  POST "https://api.telegram.org/bot"""+telegram_token+"""/sendChatAction" -F chat_id=$1 -F action=upload_video> /dev/null 2>&1
    curl -X  POST "https://api.telegram.org/bot"""+telegram_token+"""/sendVideo" -F chat_id=$1 -F video="@$2" > /dev/null 2>&1"""

    content_file4 = """#!/bin/bash
    curl -X  POST "https://api.telegram.org/bot"""+telegram_token+"""/sendChatAction" -F chat_id=$1 -F action=record_audio> /dev/null 2>&1
    curl -X  POST "https://api.telegram.org/bot"""+telegram_token+"""/sendVoice" -F chat_id=$1 -F voice="@$2" >/dev/null 2>&1"""

    writefile(file1, content_file1)
    writefile(file2, content_file2)
    writefile(file3, content_file3)
    writefile(file4, content_file4)

    st = os.stat(file1)
    os.chmod(file1, st.st_mode | 0o111)
    st = os.stat(file2)
    os.chmod(file2, st.st_mode | 0o111)
    st = os.stat(file3)
    os.chmod(file3, st.st_mode | 0o111)
    st = os.stat(file4)
    os.chmod(file4, st.st_mode | 0o111)

write_telegram_files()
# load variables from database
def get_variables():
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """SELECT * FROM variables"""
        cursor6.execute(command6)
        data = cursor6.fetchall()
        db6.close()
        my_dict = {}
        for i in data:
            my_dict.update({str(i[0].encode('utf-8')): str(i[1].encode('utf-8'))})
        return my_dict
    except Exception, e:
        print e

sam_vars = get_variables()


# Return equirectangular approximation distance in km.
def equi_rect_distance(loc1, loc2):
    R = 6371  # Radius of the earth in km.
    lat1 = math.radians(loc1[0])
    lat2 = math.radians(loc2[0])
    x = (math.radians(loc2[1]) - math.radians(loc1[1])
         ) * math.cos(0.5 * (lat2 + lat1))
    y = lat2 - lat1
    return R * math.sqrt(x * x + y * y)


# Return True if distance between two locs is less than distance in km.
def in_radius(loc1, loc2, distance):
    return equi_rect_distance(loc1, loc2) < distance


def AliveStatus(chatid):
    try:
        command = "SELECT waypoint,livestatus FROM user WHERE chatid = '" + str(chatid) +"'" 
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor = db6.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        db6.close()
        return data[0]
    except Exception, e:
        return []
        try:
            db6.close()
        except:
            pass

def addPoint(chatid):
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """UPDATE user SET points = points + 1 WHERE chatid = '"""+str(chatid)+"""' """
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e2:
        print e2
        try:
            db6.close()
        except:
            pass

def ReviveStatus(chatid):
    try:
        command = "SELECT inventory FROM user WHERE chatid = '" + str(chatid) +"'" 
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor = db6.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        db6.close()
        if "1," in str(data):
            return True
        else:
            return False
    except Exception, e:
        try:
            db6.close()
        except:
            pass
        print e
        return False

def GetInventory(chatid):
    try:
        command = "SELECT inventory FROM user WHERE chatid = '" + str(chatid) +"'" 
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor = db6.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        db6.close()
        return data[0][0]
    except Exception, e:
        return []
        try:
            db6.close()
        except:
            pass

def GetInventoryTypes():
    try:
        command = "SELECT * FROM extra_types" 
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor = db6.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        db6.close()
        mydict = {}
        values = data

        for i in values:
            id = i[0]
            name = i[1].encode("UTF-8")
            beschreibung = i[2].encode("UTF-8")
            mydict[str(id)] = str(name)+", "+str(beschreibung)
        return mydict
    except Exception, e:
        print "GetInventoryTypes"+str(e)
        return {}
        try:
            db6.close()
        except:
            pass

def GetInventoryTypesByName():
    try:
        command = "SELECT * FROM extra_types" 
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor = db6.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        db6.close()
        mydict = {}
        values = data

        for i in values:
            id = i[0]
            name = i[1].encode("UTF-8")
            beschreibung = i[2].encode("UTF-8")
            mydict[str(name)] = str(id)+", "+str(beschreibung)
        return mydict
    except Exception, e:
        print "GetInventoryTypes"+str(e)
        return {}
        try:
            db6.close()
        except:
            pass



def StartButton(chatid):
    alives = AliveStatus(chatid)
    if ReviveStatus(chatid):
        custom_keyboard = [['Start'], ['MedKit']]
    else:
        custom_keyboard = [['Start']]
    return custom_keyboard

def get_keyboard_type(the_chat_id):
    custom_keyboard = []
    alives = AliveStatus(the_chat_id)
    livestatus = alives[1]
    waypoint = alives[0]
    inventory = GetInventory(the_chat_id)
    topbuttons = ['Player', 'Hilfe']
    if (str(inventory) != "None") and (str(inventory) != "") :
        topbuttons = ['Inventar', 'Player', 'Hilfe']

    if str(the_chat_id) in admin_chatids:
        custom_keyboard = [topbuttons, [{
				"text": "Position aktualisieren",
				"request_location": True
			}], ['Trigger1', 'Trigger2', 'Trigger3']]
    else:
        if ((int(livestatus) == 0) or (int(waypoint) == 0)):
            custom_keyboard = [topbuttons, [{
                                    "text": "Position aktualisieren",
                                    "request_location": True
                            }] ]
        else:
            custom_keyboard = StartButton(the_chat_id)

    return custom_keyboard

def start(bot, update):
    try:

        try:
            cmd = 'Telegram/sendTelegramPicSam ' + str(update.message.chat_id) + ' '+sam_vars["start_image"]
            os.system(cmd)
            start_text=sam_vars["start_text"]
        except:
            pass

        reset_waypoint(update, update.message.chat_id)
        custom_keyboard = get_keyboard_type(update.message.chat_id)
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id, text=start_text, reply_markup=reply_markup)
        mydata = update.message.chat.first_name
        set_name(str(update.message.chat_id), str(mydata))
    except Exception, e:
        try:
            db6.close()
        except:
            pass
        print "reset_waypoint:"+str(e)
        bot.send_message(chat_id=update.message.chat_id, text=sam_vars["start_error"])

def stop(bot, update):
    try:
        (returntext, returntextkurz) = died(update.message.chat_id)
        stop_text = returntext
        custom_keyboard = StartButton(update.message.chat_id)

        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
        SendBroadcast(bot, update, update.message.chat.first_name+": "+returntextkurz)
        bot.send_message(chat_id=update.message.chat_id, text=stop_text, reply_markup=reply_markup)
    except Exception, e:
        print e
        bot.send_message(chat_id=update.message.chat_id, text=sam_vars["stop_error"])

def player(bot, update):
    try:
        command = "SELECT user.name, deathreason.text_kurz, user.points FROM user, deathreason WHERE user.livestatus = deathreason.id"
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor = db6.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        db6.close()
        text = "💂👨‍🔬👨‍💻<b>Liste der Spieler</b>👨‍💻👨‍🔬💂\n\n"
        for i in data:
            username = str(i[0])
            livestatus = str(i[1])
            points = str(i[2])
            if invincible == 0:
                text = text + "🕵️  " + username + " ("+str(livestatus)+")\n"
            else:
                text = text + "🕵️  " + username + " ("+str(points)+" Punkte)\n"

        custom_keyboard = get_keyboard_type(update.message.chat_id)
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id, text=text, reply_markup=reply_markup, parse_mode="HTML")
    except Exception, e:
        print e
        return []
        try:
            db6.close()
        except:
            pass

def help(bot, update):
    help_text = sam_vars["help_text"]
    custom_keyboard = get_keyboard_type(update.message.chat_id)
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text=help_text, reply_markup=reply_markup)

def echo(bot, update):
    try:
        text = str(update.message.text.encode('utf-8'))
        the_chat_id = str(update.message.chat_id)

        if text == "Start":
            start(bot, update)
        elif text == "Stop":
            stop(bot, update)
        elif text == "Inventar":
            infos(bot, update)
        elif text == "Hilfe":
            help(bot, update)
        elif text.lower() == "player":
            player(bot, update)
        elif text == "MedKit":
            useMedkit(bot, update, update.message.chat_id)
        elif text.lower().strip() == "reset":
            bot.send_message(chat_id=update.message.chat_id, text="Todesgründe freigegeben!")
            resetreasons()
        elif text[0:6].lower() == "revive":
            if str(the_chat_id) in admin_chatids:
                to_revive = text[7:].strip()
                text = sam_vars["revive_text"]

                the_ids = GetChatIDs(to_revive)

                for the_id in the_ids:
                    custom_keyboard = get_keyboard_type(the_id)
                    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
                    bot.send_message(chat_id=the_id, text=text, reply_markup=reply_markup)
                reviveU(str(to_revive))
        elif text == "restart":
            if str(the_chat_id) in admin_chatids:
                text = "Restarting SAM..."
                bot.send_message(chat_id=update.message.chat_id, text=text)
                cwd = os.getcwd()
                cmd = 'sudo '+cwd+'/start.sh '+str(cwd)+' > /tmp/sam-restart.log 2>&1 &'
                realcmd = "nohup bash -c '"+str(cmd)+"'"
                os.system(cmd)
        elif text.lower()[0:4] == "send":
            if str(the_chat_id) in admin_chatids:
                SendBroadcast(bot, update)
        elif str(the_chat_id) in admin_chatids:
            if text.lower().strip() == "trigger1":
                cmd = "./modules/activateTrigger.py trigger1 >/dev/null 2>&1 &"
                os.system(cmd)
            elif text.lower().strip() == "trigger2":
                cmd = "./modules/activateTrigger.py trigger2 >/dev/null 2>&1 &"
                os.system(cmd)
            elif text.lower().strip() == "trigger3":
                cmd = "./modules/activateTrigger.py trigger3 >/dev/null 2>&1 &"
                os.system(cmd)
        else:
            bot.send_message(chat_id=update.message.chat_id, text=sam_vars["unknown_text"])
    except Exception, e:
        print e
        bot.send_message(chat_id=update.message.chat_id, text="Fehler: "+str(e))

def finished(bot, update, chatid = ""):
    try:
        bot.send_message(chat_id=update.message.chat_id, text=sam_vars["finished_text"])
    except:
        bot.send_message(chat_id=chatid, text=sam_vars["finished_text"])


def get_all_extras():
    try:
        command = "SELECT * FROM extra_waypoints WHERE amount >= 1"
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor = db6.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        db6.close()
        return data
    except Exception, e:
        return []
        try:
            db6.close()
        except:
            pass

def check_extras(bot, update, location):
    try:
        chatid = update.message.chat_id
        extras = get_all_extras()
        user_location = update.message.location
        lat = user_location.latitude
        long = user_location.longitude
        location = (float(lat), float(long))
        for i in extras:
            id = i[0]
            waypoint_location = i[1]
            type = i[2]
            amount = i[3]
            chance = int(i[4])

            try:
                custom_trigger_distance_m = int(i[5])
            except:
                custom_trigger_distance_m = 0

            if custom_trigger_distance_m != 0:
                the_trigger_distance = custom_trigger_distance_m
            else:
                the_trigger_distance = item_radius_m



            la = waypoint_location.split(", ")[0]
            lo = waypoint_location.split(", ")[1]
            location_point = (float(la), float(lo))
            distance = equi_rect_distance(location_point, location)

            if int(float(distance)*1000) <= the_trigger_distance:
                if chance < 100:
                    myint = random.randint(1,100)
                    if myint <= chance:

                        if int(type) == 14:
                            reduceItem(id)
                            removeTrap(chatid)
                            trap(bot, update, chatid)
                            break
                        else:
                            if (addToInventory(chatid, type)):
                               itemFound(bot, update, type)
                               reduceItem(id)
                else:
                    if int(type) == 14:
                        reduceItem(id)
                        removeTrap(chatid)
                        trap(bot, update, chatid)
                        break
                    else:
                        if (addToInventory(chatid, type)):
                           itemFound(bot, update, type)
                           reduceItem(id)

    except:
        pass

def addToInventory(chatid, extra):
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        extra = str(extra) + ","
        command6 = """UPDATE user SET inventory = Concat(inventory, '"""+str(extra)+"""') WHERE chatid = '"""+str(chatid)+"""' """
        cursor6.execute(command6)
        db6.commit()
        db6.close()
        return True
    except Exception, e2:
        print e2
        try:
            db6.close()
        except:
            pass
        return False

def reduceItem(extra_id):
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """UPDATE extra_waypoints SET amount = amount - 1 WHERE id = '"""+str(extra_id)+"""' """
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e2:
        print e2
        try:
            db6.close()
        except:
            pass


def itemFound(bot, update, extra):
    try:
        text3 = " <b>gefunden!</b>"
        chatid = chat_id=update.message.chat_id

        mydict = GetInventoryTypes()
        emojidict = GetEmojis()

        daten = str(mydict[str(extra)]).split(",")
        name = daten[0]
        beschreibung = daten[1]
        emoji = emojidict[str(extra)]

        if str(name) == "Falle":
            text3 = " <b>ausgelöst!</b>"

        text2 = str(emoji)+" /"+str(name)
        custom_keyboard = get_keyboard_type(update.message.chat_id)
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id, text=text2+text3, reply_markup=reply_markup, parse_mode='HTML')
    except:
        pass

def location(bot, update):
    try:
        user_location = update.message.location
        try:
            if str(cheat_detection) == "0":
                raise ValueError('Cheat detection disabled!')
            verified = update.message.reply_to_message

            if verified == None:
                if invincible == 0:
                    (returntext, returntextkurz) = died(update.message.chat_id, 1)
                    stop_text = returntext
                    custom_keyboard = StartButton(update.message.chat_id)
                    try:
                        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
                        bot.send_message(chat_id=update.message.chat_id, text=stop_text, reply_markup=reply_markup)
                    except Exception, e:
                        print e
                    SendBroadcast(bot, update, update.message.chat.first_name+": "+returntextkurz)
                else:
                    stop_text = sam_vars["cheat_text"]
                    custom_keyboard = get_keyboard_type(update.message.chat_id)
                    try:
                        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
                        bot.send_message(chat_id=update.message.chat_id, text=stop_text, reply_markup=reply_markup)
                    except Exception, e:
                        print e
                    
        except:
            lat = user_location.latitude
            long = user_location.longitude
            location = (float(lat), float(long))
            UpdateLocation(update.message.chat_id, str(lat)+", "+str(long))
            radius = 1
            chatid = update.message.chat_id
            check_extras(bot, update, location)

            data = GetWaypoints(chatid)
            if len(data) == 0:
                finished(bot, update)
            for i in data:
                id = i[0]
                verify = AliveStatus(chatid)
                if ((verify[1] != 0) and (int(id) != 0)):
                    return
                waypoint_location = i[1]

                text = i[2]
                bild = i[3]
                audio = i[4]
                video = i[5]
                voice = i[6]
                trigger = i[7]
                info = i[8]
                question = i[9]
                is_wrong = i[10]
                is_right = i[11]
                is_wrong2 = i[12]
                try:
                    wayname = i[13]
                except:
                    wayname = "Null"

                try:
                    custom_trigger_distance_m = int(i[14])
                except:
                    custom_trigger_distance_m = 0


                if custom_trigger_distance_m != 0:
                    the_trigger_distance = custom_trigger_distance_m
                else:
                    the_trigger_distance = waypoint_radius_m

                if text is not None:
                    text = i[2].encode('utf-8', 'ignore')
                    text = emoji.emojize(text, use_aliases=True)

                if question is not None:
                    try:
                        question = i[9].encode('utf-8', 'ignore')
                    except:
                        question = i[9]
                        pass
                    try:
                        is_wrong = i[10].encode('utf-8', 'ignore')
                    except:
                        is_wrong = i[10]

                    try:
                        is_right = i[11].encode('utf-8', 'ignore')
                    except:
                        is_right = i[11]

                if is_wrong2 is not None:
                    try:
                        is_wrong2 = i[12].encode('utf-8', 'ignore')
                    except:
                        is_wrong2 = i[12]


                chatid = update.message.chat_id
                la = waypoint_location.split(", ")[0]
                lo = waypoint_location.split(", ")[1]
                location_point = (float(la), float(lo))

                distance = equi_rect_distance(location_point, location)
                if int(float(distance)*1000) <= the_trigger_distance:
                    if (str(id) == "0"):
                        revive(chatid)
                        resetPoints(chatid)
                    if video is not None:
                        cmd = 'Telegram/sendTelegramVideoSam ' + str(update.message.chat_id) + ' '+str(video)
                        os.system(cmd)
                    if bild is not None:
                        cmd = 'Telegram/sendTelegramPicSam ' + str(update.message.chat_id) + ' '+str(bild)
                        os.system(cmd)
                    if text is not None:
                        bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode='HTML')
                    if audio is not None:
                        cmd = 'Telegram/sendTelegramAudioSam ' + str(update.message.chat_id) + ' '+str(audio)
                        os.system(cmd)
                    if voice is not None:
                        cmd = 'Telegram/sendTelegramVoiceSam ' + str(update.message.chat_id) + ' '+str(voice)
                        os.system(cmd)
                    if trigger is not None:
                        cmd = "./modules/activateTrigger.py " + str(trigger)+" >/dev/null 2>&1 &"
                        os.system(cmd)
                    if question is None:
                        next_waypoint(update.message.chat_id)
                        location2(bot, update, update.message.chat_id, location)
                    if question is not None:
                        if is_wrong2 is not None:
                            myint = random.randint(0,2)
                            keyboard = []
                            if myint == 0:
                                icon1 = emojize(is_right, use_aliases=True)
                                mydata1 = "question|"+str(is_right)+"|"+str(chatid)+"|"+"true|"+str(long)+"|"+str(lat)
                                keyboard.append([InlineKeyboardButton(icon1, callback_data=mydata1)])

                                icon2 = emojize(is_wrong, use_aliases=True)
                                mydata2 = "question|"+str(is_wrong)+"|"+str(chatid)+"|"+"false|"+str(long)+"|"+str(lat)
                                keyboard.append([InlineKeyboardButton(icon2, callback_data=mydata2)])

                                icon3 = emojize(is_wrong2, use_aliases=True)
                                mydata3 = "question|"+str(is_wrong2)+"|"+str(chatid)+"|"+"false|"+str(long)+"|"+str(lat)
                                keyboard.append([InlineKeyboardButton(icon3, callback_data=mydata3)])
                            elif myint == 1:
                                icon2 = emojize(is_wrong, use_aliases=True)
                                mydata2 = "question|"+str(is_wrong)+"|"+str(chatid)+"|"+"false|"+str(long)+"|"+str(lat)
                                keyboard.append([InlineKeyboardButton(icon2, callback_data=mydata2)])

                                icon1 = emojize(is_right, use_aliases=True)
                                mydata1 = "question|"+str(is_right)+"|"+str(chatid)+"|"+"true|"+str(long)+"|"+str(lat)
                                keyboard.append([InlineKeyboardButton(icon1, callback_data=mydata1)])

                                icon3 = emojize(is_wrong2, use_aliases=True)
                                mydata3 = "question|"+str(is_wrong2)+"|"+str(chatid)+"|"+"false|"+str(long)+"|"+str(lat)
                                keyboard.append([InlineKeyboardButton(icon3, callback_data=mydata3)])

                            elif myint == 2:

                                icon2 = emojize(is_wrong, use_aliases=True)
                                mydata2 = "question|"+str(is_wrong)+"|"+str(chatid)+"|"+"false|"+str(long)+"|"+str(lat)
                                keyboard.append([InlineKeyboardButton(icon2, callback_data=mydata2)])

                                icon3 = emojize(is_wrong2, use_aliases=True)
                                mydata3 = "question|"+str(is_wrong2)+"|"+str(chatid)+"|"+"false|"+str(long)+"|"+str(lat)
                                keyboard.append([InlineKeyboardButton(icon3, callback_data=mydata3)])

                                icon1 = emojize(is_right, use_aliases=True)
                                mydata1 = "question|"+str(is_right)+"|"+str(chatid)+"|"+"true|"+str(long)+"|"+str(lat)
                                keyboard.append([InlineKeyboardButton(icon1, callback_data=mydata1)])

                            reply_markup = InlineKeyboardMarkup(keyboard)
                            update.message.reply_text(emojize(question, use_aliases=True), reply_markup=reply_markup)
                        else:
                            myint = random.randint(0,1)
                            keyboard = []
                            if myint == 0:
                                icon1 = emojize(is_right, use_aliases=True)
                                mydata1 = "question|"+str(is_right)+"|"+str(chatid)+"|"+"true|"+str(long)+"|"+str(lat)
                                keyboard.append([InlineKeyboardButton(icon1, callback_data=mydata1)])

                                icon2 = emojize(is_wrong, use_aliases=True)
                                mydata2 = "question|"+str(is_wrong)+"|"+str(chatid)+"|"+"false|"+str(long)+"|"+str(lat)
                                keyboard.append([InlineKeyboardButton(icon2, callback_data=mydata2)])
                            else:
                                icon1 = emojize(is_wrong, use_aliases=True)
                                mydata = "question|"+str(is_wrong)+"|"+str(chatid)+"|"+"false|"+str(long)+"|"+str(lat)
                                keyboard.append([InlineKeyboardButton(icon1, callback_data=mydata)])


                                icon2 = emojize(is_right, use_aliases=True)
                                mydata2 = "question|"+str(is_right)+"|"+str(chatid)+"|"+"true|"+str(long)+"|"+str(lat)
                                keyboard.append([InlineKeyboardButton(icon2, callback_data=mydata2)])

                            reply_markup = InlineKeyboardMarkup(keyboard)
                            update.message.reply_text(emojize(question, use_aliases=True), reply_markup=reply_markup)


                elif int(float(distance)*1000) <= 4999:
                    if hasMap(chatid):
                        direction_message = " ("+str(direction(location, location_point))+")"
                    else:
                        direction_message = ""
                    the_text = "Der nächste Wegpunkt ist in "+str(int(distance*1000))+"m"+direction_message
#                    bot.send_message(chat_id=update.message.chat_id, text=the_text, parse_mode='HTML')
                    custom_keyboard = get_keyboard_type(update.message.chat_id)
                    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
                    bot.send_message(chat_id=update.message.chat_id, text=the_text, reply_markup=reply_markup, parse_mode='HTML')
                elif int(float(distance)*1000) >= 5000:
                    #the_text sollte eine variable sein
                    the_text = "Du bist noch zu weit entfernt!  "+str(int(distance))+"km entfernung!"
                    #bot.send_message(chat_id=update.message.chat_id, text=the_text, parse_mode='HTML')
                    custom_keyboard = get_keyboard_type(update.message.chat_id)
                    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
                    bot.send_message(chat_id=update.message.chat_id, text=the_text, reply_markup=reply_markup)

    except Exception, e:
        bot.send_message(chat_id=update.message.chat_id, text='Fehler Location: '+str(e))



def location2(bot, update, chatid = "", the_location = ""):
    if chatid == "":
        try:
            chatid = update.message.chat_id
        except:
            pass
    if the_location == "":
        the_location = update.message.location
    try:
        user_location = the_location
        try:
            lat, long = user_location
        except:
            lat = user_location.latitude
            long = user_location.longitude
        location = (float(lat), float(long))
        radius = 1
        data = GetWaypoints(chatid)
        if len(data) == 0:
            finished(bot, update, chatid)
        for i in data:
            id = i[0]
            waypoint_location = i[1]
            text = i[2]
            bild = i[3]
            audio = i[4]
            video = i[5]
            voice = i[6]
            trigger = i[7]

            la = waypoint_location.split(", ")[0]
            lo = waypoint_location.split(", ")[1]
            location_point = (float(la), float(lo))

            distance = equi_rect_distance(location_point, location)
            if int(float(distance)*1000) <= 4999:
                if hasMap(chatid):
                    direction_message = " ("+str(direction(location, location_point))+")"
                else:
                    direction_message = ""
                the_text = "Auf zum nächsten Wegpunkt!\n"+str(int(distance*1000))+"m"+direction_message
           #     bot.send_message(chat_id=chatid, text=the_text, parse_mode='HTML')
                custom_keyboard = get_keyboard_type(chatid,)
                reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
                bot.send_message(chat_id=chatid, text=the_text, reply_markup=reply_markup)
            elif int(float(distance)*1000) >= 5000:
                the_text = "Der Start des Trail befindet sich in "+str(int(distance))+"km entfernung!"
            #    bot.send_message(chat_id=chatid, text=the_text, parse_mode='HTML')
                custom_keyboard = get_keyboard_type(chatid,)
                reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
                bot.send_message(chat_id=chatid, text=the_text, reply_markup=reply_markup)
    except Exception, e:
        print e
        bot.send_message(chat_id=chatid, text='Fehler Location2: '+str(e))


def direction(orgin, destination):
    (lat, lon) = orgin
    (lat2, lon2) = destination

    lat = float(lat)
    lon = float(lon)
    origin_point = LatLng.from_degrees(lat, lon)

    pokemon_point = LatLng.from_degrees(float(lat2), float(lon2))
    diff = pokemon_point - origin_point
    diff_lat = diff.lat().degrees
    diff_lng = diff.lng().degrees
    direction = (('N' if diff_lat >= 0 else 'S')
                if abs(diff_lat) > 1e-4 else '') +\
                (('O' if diff_lng >= 0 else 'W')
                if abs(diff_lng) > 1e-4 else '')
    return direction

def GetWaypoints(chatid):
    try:
        command = """SELECT * FROM waypoints, user WHERE user.chatid = '"""+str(chatid)+"""' and user.waypoint = waypoints.id"""
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor = db6.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        db6.close()
        return data
    except Exception, e:
        return []
        try:
            db6.close()
        except:
            pass

def GetUsername(chatid):
    try:
        command = """SELECT name FROM user WHERE chatid = '"""+str(chatid)+"""'"""
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor = db6.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        db6.close()
        return data[0][0]
    except Exception, e:
        return []
        try:
            db6.close()
        except:
            pass


def GetChatIDs(playername):
    try:
        command = """SELECT chatid FROM user WHERE name = '"""+str(playername)+"""'"""
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor = db6.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        db6.close()
        return data[0]
    except Exception, e:
        return []
        try:
            db6.close()
        except:
            pass



def button_all(bot, update):
    query = update.callback_query

    data = query.data
    type = data.split("|")[0].encode('utf-8')
    if str(type) == "question":
        button_question(bot, update)

def trap(bot, update, chatid):
    custom_keyboard = StartButton(chatid)
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
    the_text = "Du bist in eine Falle geraten!"
    bot.send_message(chat_id=chatid, text=the_text, reply_markup=reply_markup)
    try:
        stop_text = sam_vars["stop_text"]


        if invincible == 0:
            (returntext, returntextkurz) = died(chatid)
            the_text = returntext
            bot.send_message(chat_id=chatid, text=the_text, reply_markup=reply_markup)


        if invincible == 0:
            try:
                bot.send_message(chat_id=chatid, text=stop_text, reply_markup=reply_markup)
            except Exception, e:
                print e

            try:
                SendBroadcast(bot, update, str(GetUsername(chatid))+": "+str(returntextkurz))
            except Exception, e:
                print e
    except Exception, e3:
      print e3

		
def button_question(bot, update):
    query = update.callback_query

    data = query.data
    name = data.split("|")[1].encode('utf-8')
    chatid = data.split("|")[2].encode('utf-8')
    mode = data.split("|")[3].encode('utf-8')
    lon = data.split("|")[4].encode('utf-8')
    lat = data.split("|")[5].encode('utf-8')

    old_location = (float(lat), float(lon))

    mytext = data.encode('utf-8')
    mytext = str(mytext)

    if str(mode) == "true":
        mytext = sam_vars["rightanswer_text"]
        bot.edit_message_text(text=mytext,
                          chat_id=chatid,
                          message_id=query.message.message_id)
        addPoint(chatid)
        next_waypoint(chatid)
        location2(bot, update, chatid, old_location)
    elif str(mode) == "false":
        if invincible == 0:
            (returntext, returntextkurz) = died(chatid)
            the_text = returntext
        else:
            next_waypoint(chatid)
            location2(bot, update, chatid, old_location)
            the_text = sam_vars["wronganswer_text"]

        bot.edit_message_text(text=the_text,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

        if invincible == 0:
            stop_text = sam_vars["stop_text"]
            custom_keyboard = StartButton(chatid)

            try:
                reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
                bot.send_message(chat_id=chatid, text=stop_text, reply_markup=reply_markup)
            except Exception, e:
                print e

            try:
                SendBroadcast(bot, update, str(GetUsername(chatid))+": "+str(returntextkurz))
            except Exception, e:
                print e

		
def reset_waypoint(update, chatid):
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """INSERT INTO user (waypoint, chatid) VALUES (0, '"""+str(chatid)+"""')"""
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e:
        try:
            db6.close()
        except:
            pass
        try:
            db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
            cursor6 = db6.cursor()
            command6 = """UPDATE user SET waypoint = 0 WHERE chatid = '"""+str(chatid)+"""' """
            cursor6.execute(command6)
            db6.commit()
            db6.close()
        except Exception, e2:
            print e2
            try:
                db6.close()
            except:
                pass
    try:
        resetInventory(chatid, True)
    except Exception, e2:
        print e2

def freereason():
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = "SELECT id FROM `deathreason` WHERE inuse = 0 LIMIT 1"
        cursor6.execute(command6)
        data = cursor6.fetchall()
        return data[0][0]
        db6.close()
    except Exception, e:
        print e
        try:
            db6.close()
        except:
            pass
        resetreasons()
        return freereason()

def reasondata(reason):
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = "SELECT * FROM `deathreason` WHERE id = "+str(reason)
        cursor6.execute(command6)
        data = cursor6.fetchall()
        db6.close()
        return data[0]
    except Exception, e:
        print e
        try:
            db6.close()
        except:
            pass

def blockreason(id):
    if (str(id) == "1"):
        return
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """UPDATE deathreason SET inuse = 1 WHERE id = '"""+str(id)+"""' """
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e:
        try:
            db6.close()
        except:
            pass

def resetreasons():
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """UPDATE deathreason SET inuse = 0 WHERE inuse = 1"""
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e:
        try:
            db6.close()
        except:
            pass


def died(chatid, reason = 99):
    if (reason == 99):
        reason = freereason()

    reasondatarray = reasondata(reason)
    text = reasondatarray[1]
    textkurz = reasondatarray[2]

    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """UPDATE user SET livestatus = """+str(reason)+""" WHERE chatid = '"""+str(chatid)+"""' """
        cursor6.execute(command6)
        db6.commit()
        db6.close()
        blockreason(reason)
    except Exception, e:
        print e
        try:
            db6.close()
        except:
            pass

    try:
        resetInventory(chatid)
    except Exception, e2:
        print e2

    return (text, textkurz)

def revive(chatid):
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """UPDATE user SET livestatus = 0 WHERE chatid = '"""+str(chatid)+"""' """
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e2:
        print e2
        try:
            db6.close()
        except:
            pass

def reviveU(playername):
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """UPDATE user SET livestatus = 0 WHERE name = '"""+str(playername)+"""' """
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e2:
        print e2
        try:
            db6.close()
        except:
            pass

def resetPoints(chatid):
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """UPDATE user SET points = 0 WHERE chatid = '"""+str(chatid)+"""' """
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e2:
        print e2
        try:
            db6.close()
        except:
            pass

def hasMap(chatid):
    hasMap = False
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = "SELECT inventory FROM `user` WHERE chatid = '"+str(chatid)+"'"
        cursor6.execute(command6)
        data = cursor6.fetchall()
        db6.close()
        values = str(data[0][0])
        if "23," in values:
            hasMap = True
    except Exception, e:
        try:
            db6.close()
        except:
            pass
        print e
    return hasMap

def resetInventory(chatid, total = False):
    InventoryArray = []
    hasMedKit = False
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = "SELECT inventory FROM `user` WHERE chatid = '"+str(chatid)+"'"
        cursor6.execute(command6)
        data = cursor6.fetchall()
        db6.close()
        values = str(data[0][0])
        if "1," in values:
            hasMedKit = True
            values = values.replace("1,", "", 1)
        InventoryArray = values.split(",")
    except Exception, e:
        try:
            db6.close()
        except:
            pass
        print e

    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        if (hasMedKit and (total == False)):
            command6 = """UPDATE user SET inventory = "1," WHERE chatid = '"""+str(chatid)+"""' """
        else:
            command6 = """UPDATE user SET inventory = "" WHERE chatid = '"""+str(chatid)+"""' """
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except:
        pass

    try:
        for i in InventoryArray:
            if (str(i) != ""):
                DropItem(str(i), chatid)
    except Exception,e:
        print e

def UpdateLocation(chatid, location):
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """UPDATE user SET location = '"""+str(location)+"""' WHERE chatid = '"""+str(chatid)+"""' """
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except:
        pass

def DBLocation(chatid):
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """SELECT location FROM user WHERE chatid = '"""+str(chatid)+"""' """
        cursor6.execute(command6)
        data = cursor6.fetchall()
        db6.close()
        return data[0]
    except:
        pass

def DropItem(type, chatid):
    location = DBLocation(chatid)[0]
    if ((str(type) != "0") and (str(location) != "None") and (str(type) != "") ):
        try:
            db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
            cursor6 = db6.cursor()
            command6 = """INSERT INTO extra_waypoints (location, type, amount) VALUES ('"""+str(location)+"""', '"""+str(type)+"""', '1')"""
            cursor6.execute(command6)
            db6.commit()
            db6.close()
        except Exception, e:
            print e
            try:
                db6.close()
            except:
                pass

def DropInventoryItem(type, chatid):
    try:
        command = "SELECT inventory FROM user WHERE chatid = '" + str(chatid) +"'"
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor = db6.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        db6.close()
        newinventory = str(data[0][0]).replace(str(type)+',', '', 1)

        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """UPDATE user SET inventory = '"""+str(newinventory)+"""' WHERE chatid = '"""+str(chatid)+"""' """
        cursor6.execute(command6)
        db6.commit()
        db6.close()
	DropItem(type, chatid)
    except Exception, e:
        return []
        try:
            db6.close()
        except:
            pass

def removeMedkit(chatid):
    try:
        command = "SELECT inventory FROM user WHERE chatid = '" + str(chatid) +"'"
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor = db6.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        db6.close()
        newinventory = str(data[0][0]).replace('1,', '', 1)

        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """UPDATE user SET inventory = '"""+str(newinventory)+"""' WHERE chatid = '"""+str(chatid)+"""' """
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e:
        return []
        try:
            db6.close()
        except:
            pass


def removeTrap(chatid):
    try:
        command = "SELECT inventory FROM user WHERE chatid = '" + str(chatid) +"'"
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor = db6.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        db6.close()
        newinventory = str(data[0][0]).replace('14,', '', 1)

        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """UPDATE user SET inventory = '"""+str(newinventory)+"""' WHERE chatid = '"""+str(chatid)+"""' """
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e:
        return []
        try:
            db6.close()
        except:
            pass

def useMedkit(bot, update, chatid):
    if ReviveStatus(chatid):
        try:
            db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
            cursor6 = db6.cursor()
            command6 = """UPDATE user SET livestatus = 0 WHERE chatid = '"""+str(chatid)+"""' """
            cursor6.execute(command6)
            db6.commit()
            db6.close()
            resetInventory(chatid)
            removeMedkit(chatid)
            text ="<b>Du hast dein MedPack benutzt und Lebst nun wieder!</b>"
            custom_keyboard = get_keyboard_type(chatid)
            reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
            bot.send_message(chat_id=chatid, text=text, reply_markup=reply_markup, parse_mode="HTML")
        except Exception, e2:
            print e2
            try:
                db6.close()
            except:
                pass
    else:
        text ="<b>Du hast gar kein MedPack!</b>\n<b>Cheater!</b>"
        custom_keyboard = StartButton(chatid)
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
        bot.send_message(chat_id=chatid, text=text, reply_markup=reply_markup, parse_mode="HTML")


def unknown(bot, update):
    command = str(update.message.text.encode('utf-8'))[1:]
    beschreibung = ""
    name = ""
    InventoryExtra = ""
    
    try:
        mydict = GetInventoryTypesByName()
        daten = str(mydict[command]).split(",")
        id = str(daten[0])
        beschreibung = str(daten[1])

        emojidict = GetEmojis()
        emoji = emojidict[str(id)]
	
        userinventory = GetInventory(update.message.chat_id)
        
        if str(id)+"," in str(userinventory):
            InventoryExtra = "\nYou got it!"
    except Exception, e:
        print e

    text = sam_vars["unknown_text"]
    text = emoji+" <b>"+str(command)+"</b>"+" "+emoji+"\n"+beschreibung.strip()
    text = text + InventoryExtra
    try:
        bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode="HTML")
    except:
        pass


def GetEmojis():
    try:
        emojiarray = {}
        emojiarray["1"] = "💉"
        emojiarray["2"] = "🗝️"
        emojiarray["3"] = "🔫"
        emojiarray["4"] = "🍺"
        emojiarray["5"] = "📓"
        emojiarray["6"] = "🔦"
        emojiarray["7"] = "💰"
        emojiarray["8"] = "🖊️"
        emojiarray["9"] = "💊️"
        emojiarray["10"] = "🛡️️"
        emojiarray["11"] = "🕯️"
        emojiarray["12"] = "🎀"
        emojiarray["13"] = "🔪"
        emojiarray["14"] = "💣"
        emojiarray["15"] = "🎾"
        emojiarray["16"] = "🍎"
        emojiarray["17"] = "🍄"
        emojiarray["18"] = "🌮"
        emojiarray["19"] = "🌯"
        emojiarray["20"] = "🍪"
        emojiarray["21"] = "🥃"
        emojiarray["22"] = "📯"
        emojiarray["23"] = "🗺️"
        return emojiarray
    except:
        return {}

def infos(bot, update):
    try:
        text = "📦📦📦 <b>Inventar</b> 📦📦📦 \n\n"
        chatid = chat_id=update.message.chat_id
        inventory = GetInventory(chatid)
        inventoryarray = inventory.split(",")
        mydict = GetInventoryTypes()
        emojidict = GetEmojis()
        for i in inventoryarray:
             if (str(i) != ""):
                 daten = str(mydict[str(i)]).split(",")
                 name = daten[0]
                 beschreibung = daten[1]
                 emoji = emojidict[str(i)]
                 text = text + emoji + "  /" + str( name )+"\n"

        bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode="HTML")
    except Exception, e:
        print str(e)

def SendBroadcast(bot, update, broadcast_text = ""):
    if (broadcast_text == ""):
        broadcast_text = update.message.text[5:]
    else:
        broadcast_text = "<b>" + broadcast_text + "</b>"
    data = ""

    if broadcast_death == 1:
        try:
            db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
            cursor6 = db6.cursor()
            command6 = "SELECT chatid FROM `user`"
            cursor6.execute(command6)
            data = cursor6.fetchall()
            db6.close()
        except Exception, e:
            try:
                db6.close()
            except:
                pass
            print e

        for i in data:
            try:
    #            custom_keyboard = get_keyboard_type(i[0])
    #            reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
    #            bot.send_message(chat_id=i[0], text=broadcast_text, reply_markup=reply_markup, parse_mode="HTML")
                bot.send_message(chat_id=i[0], text=broadcast_text, parse_mode="HTML")
            except Exception, e:
                print e

def set_name(chatid, name):
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """UPDATE user SET name = '"""+str(name)+"""' WHERE chatid = '"""+str(chatid)+"""'"""
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e:
        print e
        print command6
        pass


def next_waypoint(chatid):
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """UPDATE user SET waypoint = waypoint + 1 WHERE chatid = '"""+str(chatid)+"""'"""
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e:
        pass


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


echo_handler = MessageHandler(Filters.text, echo)
location_handler = MessageHandler(Filters.location, location)
start_handler = CommandHandler('start', start)
stop_handler = CommandHandler('stop', stop)
help_handler = CommandHandler('help', help)
info_handler = CommandHandler('infos', infos)
unknown_handler = MessageHandler(Filters.command, unknown)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(stop_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(location_handler)
dispatcher.add_handler(info_handler)
dispatcher.add_handler(unknown_handler)

dispatcher.add_handler(CallbackQueryHandler(button_all))

updater.start_polling()
