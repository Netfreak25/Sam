#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Moritz Kuhn
#####################################################################
import cgitb, datetime, time,  cgi, sys, os, urllib2, requests, MySQLdb
from os import listdir
from os.path import isfile, join
cgitb.enable(display=1, logdir="/var/www/log/")

print "Content-Type: text/html; charset=UTF-8"     # HTML is following
print                               # blank line, end of headers
print "<html>"
print "<head>"
print "<title>Wegpunkt</title>"
print """

    <link rel="icon" sizes="512x512" href="/img/favicon.png">
    <link rel="apple-touch-icon" href="/img/favicon.png">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">

<meta name="viewport" content="width=device-width, initial-scale=1" >
<meta name="mobile-web-app-capable" content="yes">
<meta charset="utf-8">

<style>
* {font-family:"Courier New", Courier, monospace}

</style>

"""
print "</head>"
print "<body>"
print "<div style='margin-top: 20px; padding: 5px;'>"
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
    mode = form["action"].value
    action = mode
    print "Mode:"+str(mode)
except Exception, e:
    mode = "Null"
    action = "Null"
    pass

try:
    html_waypoint = form["id"].value
except Exception, e:
    html_waypoint = "0"

try:
    html_realid = form["realID"].value
except Exception, e:
    html_realid = "0"

try:
    html_text = form["text"].value
    html_text = str(html_text).replace("|", "")
except Exception, e:
    html_text = "Null"

try:
    html_bild = form["bild"].value
except Exception, e:
    html_bild = "Null"

try:
    html_audio = form["audio"].value
except Exception, e:
    html_audio = "Null"

try:
    html_video = form["video"].value
except Exception, e:
    html_video = "Null"

try:
    html_voice = form["voice"].value
except Exception, e:
    html_voice = "Null"

try:
    html_trigger = form["trigger"].value
except Exception, e:
    html_trigger = "Null"

try:
    html_question = form["question"].value
    html_question = str(html_question).replace("|", "")
except Exception, e:
    html_question = "Null"

try:
    html_right = form["right"].value
    html_right = str(html_right).replace("|", "")
except Exception, e:
    html_right = "Null"

try:
    html_wrong1 = form["wrong"].value
    html_wrong1 = str(html_wrong1).replace("|", "")
except Exception, e:
    html_wrong1 = "Null"

try:
    html_wrong2 = form["wrong2"].value
    html_wrong2 = str(html_wrong2).replace("|", "")
except Exception, e:
    html_wrong2 = "Null"


try:
    html_wayname = form["wayname"].value
    html_wayname  = str(html_wayname).replace("|", "")
except Exception, e:
    html_wayname = "Null"



try:
    html_tdistance = form["tdistance"].value
    html_tdistance  = str(html_tdistance).replace("|", "")

except Exception, e:
    html_tdistance = "0"


try:
    html_location = form["location"].value
    html_location  = str(html_location).replace("|", "")
except Exception, e:
    html_location = "0.0 ,0.0"


def prepareText(text):
    if str(text) != "Null":
        text = "'"+text+"'"
    return str(text)

def doChanges():
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """UPDATE waypoints SET id = """+prepareText(html_waypoint)+""", location = """+prepareText(html_location)+""", trigger_distance_m = """+prepareText(html_tdistance)+""", name = """+prepareText(html_wayname)+""", text = """+prepareText(html_text)+""", bild = """+prepareText(html_bild)+""", audio = """+prepareText(html_audio)+""", video = """+prepareText(html_video)+""", voice = """+prepareText(html_voice)+""", samtrigger = """+prepareText(html_trigger)+""", question = """+prepareText(html_question)+""", is_wrong = """+prepareText(html_wrong1)+""", is_wrong2 = """+prepareText(html_wrong2)+""", is_right = """+prepareText(html_right)+"""  WHERE id = """+str(html_realid)
        print command6
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e2:
        print e2
        try:
            db6.close()
        except:
            pass


action_message = ""
if (str(action) == "editWaypoint"):
    print "high"
    doChanges()
    action_message = "Änderung gespeichert!"
    print """
<script>
close();
</script>
    """

def return_missing_numbers(numberarray):
    a=numberarray

    from itertools import imap, chain
    from operator import sub
    values = list(chain.from_iterable((a[i] + d for d in xrange(1, diff))
                        for i, diff in enumerate(imap(sub, a[1:], a))
                        if diff > 1))

    return values

def unused_waypoint():
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """SELECT id FROM waypoints ORDER BY  `waypoints`.`id` ASC ;"""
        cursor6.execute(command6)
        data = cursor6.fetchall()
        db6.close()
        numberarray = []
        numberarray.append(-1)
        for i in data:
            numberarray.append(i[0])

        newway = (max(numberarray) + 2)
        numberarray.append(int(newway))
        return return_missing_numbers(numberarray)
    except Exception, e:
        print e


# load variables from database
def get_waypoint(wid):
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """SELECT * FROM waypoints WHERE id = """+str(wid)+""";"""
        cursor6.execute(command6)
        data = cursor6.fetchall()
        db6.close()
        return data[0]
    except Exception, e:
        print e




w = get_waypoint(html_waypoint)
wid = w[0]
wlocation = w[1]
try:
    wtext = str(w[2].encode("utf-8")).replace("None","")
except:
    wtext = str(w[2]).replace("None","")

wbild = str(w[3]).replace("None","")
waudio = str(w[4]).replace("None","")
wvideo = str(w[5]).replace("None","")
wvoice = str(w[6]).replace("None","")
wtrigger = str(w[7]).replace("None","")
winfo = str(w[8]).replace("None","")
try:
    wquestion = str(w[9].encode("utf-8")).replace("None","")
except:
    wquestion = str(w[9]).replace("None","")

try:
    wwrong = str(w[10].encode("utf-8")).replace("None","")
except:
    wwrong = str(w[10]).replace("None","")

try:
    wright = str(w[11].encode("utf-8")).replace("None","")
except:
    wright = str(w[11]).replace("None","")

try:
    wwrong2 = str(w[12].encode("utf-8")).replace("None","")
except:
    wwrong2 = str(w[12]).replace("None","")

try:
    wname = str(w[13]).replace("None","")
except:
    wname = ""

try:
    wdistance = str(w[14]).replace("None","")

except:
    wdistance = ""

def availableFiles(selected_file, extension = "all", extension2 = "all"):
    mypath = "./data/"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    data = ""
    noselection = True
    for i in onlyfiles:
        if (str("data/"+str(i)).strip() == str(selected_file).strip()):
            if ((str(extension) in i) or (str(extension2) in i) or (extension == "all")):
                noselection = False
                data = data + '<option value="data/'+str(i)+'" selected>'+str(i)+'</option>\n'
        else:
            if ((str(extension) in i) or (str(extension2) in i) or (extension == "all")):
                data = data + '<option value="data/'+str(i)+'">'+str(i)+'</option>\n'

    if (noselection):
        data = data + '<option value="" selected>Inaktiv</option>\n'
    else:
        data = data + '<option value="">Inaktiv</option>\n'     
    return data



print "<div style='margin-top: -10px;'>"+action_message+"</div>"
print "<div>"
print '''
<form action="waypoint.cgi" method="get">

<div style= "clear: both;">
  <input type="hidden" name="action" value="editWaypoint">
  <input type="hidden" name="realID" value="'''+str(wid)+'''">
  <div style="float: left; width: 175px"><label for="waypoint">Wegpunkt</label></div>
  <div style="float: left; width: 175px">

  <select id="waypoint" name="id">
  <option selected value="'''+str(wid)+'''">Wegpunkt '''+str(wid)+'''</option>'''
unused = unused_waypoint()
for i in unused:
    print '<option value="'+str(i)+'">Wegpunkt '+str(i)+'</option>'
print '''
</select>
  </div>
</div>

<div style= "clear: both;">
  <div style="float: left; width: 175px"><label for="wayname">Name</label></div>
  <div style="float: left; width: 175px"><input id="wayname" name="wayname" value="'''+str(wname)+'''"></div>
</div>

<div style= "clear: both;">
  <div style="float: left; width: 175px"><label for="location">Ort</label></div>
  <div style="float: left; width: 175px"><input id="location" name="location" value="'''+str(wlocation)+'''"></div>
</div>

<div style= "clear: both;">
  <div style="float: left; width: 175px"><label for="tdistance">Radius (in m)</label></div>
  <div style="float: left; width: 175px">'''



print """<select name="tdistance">"""
distance_form = ""
if int(wdistance) == 0:
    distance_form = distance_form + '<option value="0" selected>Globale Einstellung</option>'
else:
    distance_form = distance_form + '<option value="0">Globale Einstellung</option>'


if int(wdistance) == 10:
    distance_form = distance_form + '<option value="10" selected>10m</option>'
else:
    distance_form = distance_form + '<option value="10">10m</option>'
    

if int(wdistance) == 20:
    distance_form = distance_form + '<option value="20" selected>20m</option>'
else:
    distance_form = distance_form + '<option value="20">20m</option>'
    
if int(wdistance) == 30:
    distance_form = distance_form + '<option value="30" selected>30m</option>'
else:
    distance_form = distance_form + '<option value="30">30m</option>'
    
if int(wdistance) == 40:
    distance_form = distance_form + '<option value="40" selected>40m</option>'
else:
    distance_form = distance_form + '<option value="40">40m</option>'
    
if int(wdistance) == 50:
    distance_form = distance_form + '<option value="50" selected>50m</option>'
else:
    distance_form = distance_form + '<option value="50">50m</option>'
    
if int(wdistance) == 60:
    distance_form = distance_form + '<option value="60" selected>60m</option>'
else:
    distance_form = distance_form + '<option value="60">60m</option>'
    
if int(wdistance) == 70:
    distance_form = distance_form + '<option value="70" selected>70m</option>'
else:
    distance_form = distance_form + '<option value="70">70m</option>'
    
if int(wdistance) == 80:
    distance_form = distance_form + '<option value="80" selected>80m</option>'
else:
    distance_form = distance_form + '<option value="80">80m</option>'
    
if int(wdistance) == 90:
    distance_form = distance_form + '<option value="90" selected>90m</option>'
else:
    distance_form = distance_form + '<option value="90">90m</option>'
    
if int(wdistance) == 100:
    distance_form = distance_form + '<option value="100" selected>100m</option>'
else:
    distance_form = distance_form + '<option value="100">100m</option>'

if int(wdistance) == 110:
    distance_form = distance_form + '<option value="110" selected>110m</option>'
else:
    distance_form = distance_form + '<option value="110">110m</option>'

if int(wdistance) == 120:
    distance_form = distance_form + '<option value="120" selected>120m</option>'
else:
    distance_form = distance_form + '<option value="120">120m</option>'

if int(wdistance) == 130:
    distance_form = distance_form + '<option value="130" selected>130m</option>'
else:
    distance_form = distance_form + '<option value="130">130m</option>'

if int(wdistance) == 140:
    distance_form = distance_form + '<option value="140" selected>140m</option>'
else:
    distance_form = distance_form + '<option value="140">140m</option>'

if int(wdistance) == 150:
    distance_form = distance_form + '<option value="150" selected>150m</option>'
else:
    distance_form = distance_form + '<option value="150">150m</option>'


if int(wdistance) == 200:
    distance_form = distance_form + '<option value="200" selected>200m</option>'
else:
    distance_form = distance_form + '<option value="200">200m</option>'


if int(wdistance) == 300:
    distance_form = distance_form + '<option value="300" selected>300m</option>'
else:
    distance_form = distance_form + '<option value="300">300m</option>'

print distance_form
print """</select>"""
print '''




  </div>
</div>

<div style= "clear: both;">
  <div style="float: left; width: 175px"><label for="text">Text</label></div>
  <div style="float: left; width: 175px"><textarea rows="6" id="text" name="text" >'''+str(wtext)+'''</textarea> </div>
</div>


<div style= "clear: both;">
  <div style="float: left; width: 175px"><label for="bild">Bild</label></div>
  <div style="float: left; width: 175px">
  <select id="bild" name="bild">'''
print availableFiles(wbild, "jpg", "png")
print '''
  </select>

  </div>
</div>

<div style= "clear: both;">
  <div style="float: left; width: 175px"><label for="audio">Audio</label></div>
  <div style="float: left; width: 175px">
  <select id="audio" name="audio">'''
print availableFiles(waudio, "mp3")
print '''
  </select>
  

  </div>
</div>

<div style= "clear: both;">
  <div style="float: left; width: 175px"><label for="video">Video</label></div>
  <div style="float: left; width: 175px">
    <select id="video" name="video">'''
print availableFiles(wvideo, "mp4")
print '''
  </select>
  </div>
</div>

<div style= "clear: both;">
  <div style="float: left; width: 175px"><label for="voice">Sprache</label></div>
  <div style="float: left; width: 175px">
      <select id="voice" name="voice">'''
print availableFiles(wvoice, "ogg")
print '''
  </select>
  </div>
</div>




<div style= "clear: both;">
  <div style="float: left; width: 175px"><label for="trigger">Trigger</label></div>
  <div style="float: left; width: 175px">
<select id="trigger" name="trigger">'''
if str(wtrigger) == "":
    print '''
  <option value="trigger1">Trigger 1</option>
  <option value="trigger2">Trigger 2</option>
  <option value="trigger3">Trigger 3</option>
  <option selected value="">Inaktiv</option>'''
elif str(wtrigger) == "trigger1":
    print '''
  <option selected value="trigger1">Trigger 1</option>
  <option value="trigger2">Trigger 2</option>
  <option value="trigger3">Trigger 3</option>
  <option value="">Inaktiv</option>'''
elif str(wtrigger) == "trigger2":
    print '''
  <option value="trigger1">Trigger 1</option>
  <option selected value="trigger2">Trigger 2</option>
  <option value="trigger3">Trigger 3</option>
  <option value="">Inaktiv</option>'''
elif str(wtrigger) == "trigger3":
    print '''
  <option value="trigger1">Trigger 1</option>
  <option value="trigger2">Trigger 2</option>
  <option selected value="trigger3">Trigger 3</option>
  <option value="">Inaktiv</option>'''
print '''
</select>

  </div>
</div>
<div style= "clear: both;">
  <div style="float: left; width: 175px"><label for="question">Frage</label></div>
  <div style="float: left; width: 175px"><textarea rows="6"  id="question" name="question" >'''+str(wquestion)+'''</textarea> </div>
</div>
<div style= "clear: both;">
  <div style="float: left; width: 175px"><label for="right">Korrekte Antwort</label></div>
  <div style="float: left; width: 175px"><textarea rows="2"  id="right" name="right" >'''+str(wright)+'''</textarea> </div>
</div>
<div style= "clear: both;">
  <div style="float: left; width: 175px"><label for="wrong">Falsche Antwort #1</label></div>
  <div style="float: left; width: 175px"><textarea rows="2"  id="wrong" name="wrong" >'''+str(wwrong)+'''</textarea> </div>
</div>
<div style= "clear: both;">
  <div style="float: left; width: 175px"><label for="wrong2">Falsche Antwort #2 (Optional)</label></div>
  <div style="float: left; width: 175px"><textarea rows="2"  id="wrong2" name="wrong2" >'''+str(wwrong2)+'''</textarea> </div>
</div>
<div style= "clear: both;">
  <br>
  <button>speichern</button>
</div>





</form>
'''
print "</div>"
print "</div>"

