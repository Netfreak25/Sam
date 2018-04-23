#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Moritz Kuhn
#####################################################################
import cgitb, datetime, time,  cgi, sys, os, urllib2, requests, MySQLdb
from os import listdir
from os.path import isfile, join
import shutil

cgitb.enable(display=1, logdir="/var/www/log/")




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


###### Read html input
form = cgi.FieldStorage()


try:
    html_trigger = form["t"].value
except Exception, e:
    html_trigger = "Null"


try:
    html_id = form["id"].value
except Exception, e:
    html_id = "Null"


try:
    html_battery = form["bat"].value
except Exception, e:
    html_battery = "Null"


print "Content-Type: text/html; charset=UTF-8"     # HTML is following
print                               # blank line, end of headers


def addUser():
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """INSERT INTO `samsquetch`.`trigger_clients` (`name`, `battery`, `trigger`) VALUES ('"""+str(html_id)+"""', '""" + str(html_battery)+ """', '""" + str(html_trigger) + """')"""
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e:
        try:
            db6.close()
        except:
            pass
        updateUserdata()

def updateUserdata():
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """UPDATE `samsquetch`.`trigger_clients` SET `battery` = '""" + str(html_battery)+ """', `trigger` = '""" + str(html_trigger) + """', `count` = `count` + 1 WHERE `name` = '"""+str(html_id)+"""' """
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e2:
        try:
            db6.close()
        except:
            pass

def readtrigger(triggerfile):
    triggerdatafile = "trigger/" + triggerfile
    f = open(triggerdatafile, 'r')
    triggerx = f.read().strip()
    f.close()
    return triggerx


def writeweb(trigger_1, trigger_2, trigger_3):
    towrite = "trigger1: "+str(trigger_1)+"::trigger2: "+str(trigger_2)+"::trigger3: "+str(trigger_3)
    print towrite

trigger1 = readtrigger("trigger1")
trigger2 = readtrigger("trigger2")
trigger3 = readtrigger("trigger3")

writeweb(trigger1, trigger2, trigger3)
if html_id != "Null":
    addUser()


