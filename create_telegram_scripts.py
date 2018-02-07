#!/usr/bin/python
import os

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

telegram_token = str(getconfig('telegram_token'))

telegram_directory = "Telegram"

def writefile(filename, text):
   filename = str(filename)
   text = str(text).encode("UTF-8")
   f = open(filename, 'w')
   f.write(text) 
   f.close()

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
