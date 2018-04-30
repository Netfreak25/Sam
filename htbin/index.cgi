#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Moritz Kuhn
#####################################################################
import cgitb, datetime, time,  cgi, sys, os, urllib2, requests, MySQLdb
from os import listdir
from os.path import isfile, join
import shutil

cgitb.enable(display=1, logdir="/var/www/log/")

print "Content-Type: text/html; charset=UTF-8"     # HTML is following
print                               # blank line, end of headers
print "<html>"
print "<head>"


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

try:
    botname = str(getconfig('botname'))
except:
    botname = "Botname not set"

try:
    pagename = str(getconfig('pagename'))
except:
    pagename = "Schnitzeljagdt"

try:
    invincible = int(getconfig('invincible'))
except:
    invincible = 0

try:
    advanced = int(getconfig('advanced'))
except:
    advanced = 0



try:
    sudo_access = os.path.isfile("htbin/.sudo")
except:
    sudo_access = False


try:
    auto_start_update = os.path.isfile(".autoupdate")
except:
    auto_start_update = False

###### Read html input
form = cgi.FieldStorage()


try:
    html_text_kurz = form["text_kurz"].value
except Exception, e:
    html_text_kurz = "Null"

try:
    html_text = form["text"].value
except Exception, e:
    html_text = "Null"

try:
    html_name = form["name"].value
except Exception, e:
    html_name = "Null"

try:
    html_tab = form["tab"].value
except Exception, e:
    html_tab = "wegpunkte"

try:
    html_id = form["id"].value
except Exception, e:
    html_id = "None"

try:
    html_value = form["value"].value
except Exception, e:
    html_value = "100"

try:
    html_file = form["file"].value
    html_file = str(html_file).replace("%20"," ")
except Exception, e:
    html_file = "None"


weg = "tablinks"
items = "tablinks"
deathreason = "tablinks"
dateien  = "tablinks"
benutzer = "tablinks"
variablen = "tablinks"
triggerclients = "tablinks"
configtab = "tablinks"

wegs = 'overflow: auto;'
itemss = 'overflow: auto;'
deathreasons = 'overflow: auto;'
dateiens  = 'overflow: auto;'
benutzers = 'overflow: auto;'
variablens = 'overflow: auto;'
triggerclientss = 'overflow: auto;'
configtabs = 'overflow: auto;'

if str(html_tab) == "wegpunkte":
    weg = "tablinks active"
    wegs = '''style="display: block; overflow: auto;"'''
elif str(html_tab) == "items":
    items = "tablinks active"
    itemss = '''style="display: block; overflow: auto;"'''
elif str(html_tab) == "todesursache":
    deathreason = "tablinks active"
    deathreasons = '''style="display: block; overflow: auto;"'''
elif str(html_tab) == "dateien":
    dateien  = "tablinks active"
    dateiens  = '''style="display: block; overflow: auto;"'''
elif str(html_tab) == "benutzer":
    benutzer = "tablinks active"
    benutzers = '''style="display: block; overflow: auto;"'''
elif str(html_tab) == "variablen":
    variablen = "tablinks active"
    variablens = '''style="display: block; overflow: auto;"'''
elif str(html_tab) == "triggerclients":
    triggerclients = "tablinks active"
    triggerclientss = '''style="display: block; overflow: auto;"'''
elif str(html_tab) == "config":
    configtab = "tablinks active"
    configtabs = '''style="display: block; overflow: auto;"'''





print "<title>"+str(pagename)+"</title>"
print """


    <link rel="icon" sizes="512x512" href="/img/favicon.png">
    <link rel="apple-touch-icon" href="/img/favicon.png">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">

<meta name="viewport" content="width=device-width, initial-scale=1" >
<meta name="mobile-web-app-capable" content="yes">
<meta charset="utf-8">
<style>
body {font-family: Arial;}

/* Style the tab */
.tab {
    overflow: hidden;
    border: 1px solid #ccc;
    background-color: #f1f1f1;
}

/* Style the buttons inside the tab */
.tab button {
    background-color: inherit;
    float: left;
    border: none;
    outline: none;
    cursor: pointer;
    padding: 2px 5px;
    transition: 0.3s;
    font-size: 17px;
}

/* Change background color of buttons on hover */
.tab button:hover {
    background-color: #ddd;
}

/* Create an active/current tablink class */
.tab button.active {
    background-color: #ccc;
}

/* Style the tab content */
.tabcontent {
    display: none;
    padding: 6px 12px;
    border: 1px solid #ccc;
    border-top: none;
}

* {font-family:"Courier New", Courier, monospace}


a {
    color: #000000;
    text-decoration: none;
}

.clearfix:after {
  content: "";
  display: table;
  clear: both;
}
</style>

<script type="text/javascript"> 
function openwindow(url){
      NewWindow=window.open(url,'newWin','width=400,height=600,left=20,top=20,toolbar=No,location=No,scrollbars=no,status=No,resizable=no,fullscreen=No');  NewWindow.focus(); void(0);  }
</script>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>


"""
#//<script>
#//window.onblur= function() {window.onfocus= function () {location.reload(true)}};
#//</script>


print "</head>"
print """<body onload="myFunction()">"""
print """
<script>
function myFunction() {
   $("a.eLink").click(function (evt) {
        url = evt.target.href;
        var tk = "Wirklich entfernen?";
        if (confirm(tk)) {
            window.open(url, '_self');
        }
        return false;
    });
}
</script>

"""
try:
    mode = form["action"].value
    action = mode
except Exception, e:
    mode = "none"
    action = "none"
    pass



def list_chase():
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """SHOW TABLES LIKE '%save_w_%'"""
        cursor6.execute(command6)
        data = cursor6.fetchall()
        db6.close()
        return data
    except Exception, e:
        print e

chases = list_chase()

def load_chase():
    reset_chase()

    newwtable = "save_w_"+str(html_name)
    newitable = "save_e_"+str(html_name)
    newctable = "save_c_"+str(html_name)

    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = 'INSERT waypoints SELECT * FROM '+str(newwtable)+';'
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
        command6 = 'INSERT extra_waypoints SELECT * FROM '+str(newitable)+';'
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
        command6 = 'INSERT config SELECT * FROM '+str(newctable)+';'
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e:
        print e
        try:
            db6.close()
        except:
            pass

def delete_chase():
    newwtable = "save_w_"+str(html_name)
    newitable = "save_e_"+str(html_name)
    newctable = "save_c_"+str(html_name)

    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = 'DROP TABLE '+str(newwtable)+';'
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
        command6 = 'DROP TABLE '+str(newitable)+';'
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
        command6 = 'DROP TABLE '+str(newctable)+';'
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e:
        print e
        try:
            db6.close()
        except:
            pass

def reset_chase():
    removeAllWaypoints()
    removeAllItem()
    removeAllConfig()

def save_chase():
    newwtable = "save_w_"+str(html_name)
    newitable = "save_e_"+str(html_name)
    newctable = "save_c_"+str(html_name)

    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = 'CREATE TABLE '+str(newwtable)+' LIKE waypoints;'
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e:
        try:
            db7 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
            cursor7 = db7.cursor()
            command7 = 'TRUNCATE TABLE '+str(newwtable)+';'
            cursor7.execute(command7)
            db7.commit()
            db7.close()
        except Exception, e2:
            try:
                db7.close()
            except:
                pass
        try:
            db6.close()
        except:
            pass

    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = 'INSERT '+str(newwtable)+' SELECT * FROM waypoints;'
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
        command6 = 'CREATE TABLE '+str(newitable)+' LIKE extra_waypoints;'
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e:
        try:
            db7 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
            cursor7 = db7.cursor()
            command7 = 'TRUNCATE TABLE '+str(newitable)+';'
            cursor7.execute(command7)
            db7.commit()
            db7.close()
        except Exception, e2:
            try:
                db7.close()
            except:
                pass
        try:
            db6.close()
        except:
            pass

    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = 'INSERT '+str(newitable)+' SELECT * FROM extra_waypoints;'
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
        command6 = 'CREATE TABLE '+str(newctable)+' LIKE config;'
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e:
        try:
            db7 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
            cursor7 = db7.cursor()
            command7 = 'TRUNCATE TABLE '+str(newctable)+';'
            cursor7.execute(command7)
            db7.commit()
            db7.close()
        except Exception, e2:
            try:
                db7.close()
            except:
                pass
        try:
            db6.close()
        except:
            pass

    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = 'INSERT '+str(newctable)+' SELECT * FROM config;'
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e:
        print e
        try:
            db6.close()
        except:
            pass


def restart():
    cwd = os.getcwd()
    cmd = 'sudo '+cwd+'/start.sh '+str(cwd)+' > /tmp/sam-restart.log 2>&1 &'
    realcmd = "nohup bash -c '"+str(cmd)+"'"
    os.system(cmd)

def enable_update():
    cwd = os.getcwd()
    cmd = 'touch '+str(cwd)+'/.autoupdate '
    os.system(cmd)

def disable_update():
    cwd = os.getcwd()
    cmd = 'rm '+str(cwd)+'/.autoupdate '
    os.system(cmd)

def save_uploaded_file():
    form_field = "datei"
    upload_dir = "./data/"

    fileitem = form["datei"]
    if not fileitem.file:
        print "Upload Fehler: Das war keine Datei!"
        return

    outpath = os.path.join(upload_dir, fileitem.filename)
    with open(outpath, 'wb') as fout:
        shutil.copyfileobj(fileitem.file, fout, 100000)

# load variables from database
def get_variables():
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """SELECT * FROM variables"""
        cursor6.execute(command6)
        data = cursor6.fetchall()
        db6.close()
        return data
    except Exception, e:
        print e

sam_vars = get_variables()

# load config from database
def get_dbconfig():
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """SELECT * FROM config"""
        cursor6.execute(command6)
        data = cursor6.fetchall()
        db6.close()
        return data
    except Exception, e:
        print e

configdata = get_dbconfig()



# load waypoints from database
def get_waypoints():
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """SELECT * FROM waypoints"""
        cursor6.execute(command6)
        data = cursor6.fetchall()
        db6.close()
        return data
    except Exception, e:
        print e

sam_vars = get_variables()


def get_items():
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """SELECT * FROM extra_waypoints"""
        cursor6.execute(command6)
        data = cursor6.fetchall()
        db6.close()
        return data
    except Exception, e:
        print e


def get_deathreasons():
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """SELECT * FROM deathreason"""
        cursor6.execute(command6)
        data = cursor6.fetchall()
        db6.close()
        return data
    except Exception, e:
        print e


def get_user():
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """SELECT * FROM user"""
        cursor6.execute(command6)
        data = cursor6.fetchall()
        db6.close()
        return data
    except Exception, e:
        print e


def addReason(html_text, html_text_kurz):
    html_id = str(highestReasonID() + 1)
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """INSERT INTO deathreason (id, text, text_kurz) VALUES ('"""+str(html_id)+"""', '"""+str(html_text)+"""', 'Tot durch """+str(html_text_kurz)+"""')"""
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e:
        print e
        try:
            db6.close()
        except:
            pass


def deleteReason():
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """DELETE FROM `deathreason` WHERE `deathreason`.`id` = """+str(html_id)+""";"""
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e:
        print e
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


def highestReasonID():
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = "SELECT id FROM `deathreason` ORDER BY id DESC LIMIT 1"
        cursor6.execute(command6)
        data = cursor6.fetchall()
        return int(data[0][0])
        db6.close()
    except Exception, e:
        try:
            db6.close()
        except:
            pass


def removeWaypoint(id):
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = "DELETE FROM waypoints WHERE id = "+str(id)+";"
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e:
        print e
        try:
            db6.close()
        except:
            pass

def removeAllWaypoints():
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

def removeItem(itemid):
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = "DELETE FROM extra_waypoints WHERE id = "+str(itemid)+";"
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e:
        print e
        try:
            db6.close()
        except:
            pass

def removeAllItem():
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

def removeEmptyItem():
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = "DELETE FROM extra_waypoints WHERE amount = 0;"
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e:
        print e
        try:
            db6.close()
        except:
            pass

def removeAllConfig():
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

def deleteFile():
    filename = str(html_file)
    if ((len(filename) >= 70) or ("/" in str(filename)) or (".." in str(filename))):
        pass
    else:
        try:
            os.remove("./data/"+filename)
        except Exception, e:
            print e
            try:
                db6.close()
            except:
                pass


def printFiles():
    mypath = "./data/"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    data = ""
    for i in onlyfiles:
        deleteurl = '<a class="eLink" href="index.cgi?action=deleteFile&tab=dateien&file='+str(i)+'">[entfernen]</a>'
        data = data + "<div style='clear:both;'><div style='float: left; width: 300px'><b>"+str(i)+"</b></div> <div style='float: left'>"+deleteurl+"</div></div>\n"
    return data

def printTriggerClients():
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """SELECT * FROM trigger_clients"""
        cursor6.execute(command6)
        data = cursor6.fetchall()
        db6.close()
        return data
    except Exception, e:
        print e

def chanceItem(itemid):
    chance = html_value
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """UPDATE extra_waypoints SET chance = '"""+str(chance)+"""' WHERE id = '"""+str(itemid)+"""' """
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e2:
        print e2
        try:
            db6.close()
        except:
            pass

def changeDistance(itemid):
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """UPDATE `extra_waypoints` SET `item_distance_m` = '"""+str(html_value)+"""' WHERE id = '"""+str(itemid)+"""' """
        cursor6.execute(command6)

        db6.commit()
        db6.close()
    except Exception, e2:
        print e2
        try:
            db6.close()
        except:
            pass

def plusOne(itemid):
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """UPDATE extra_waypoints SET amount = amount + 1 WHERE id = '"""+str(itemid)+"""' """
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e2:
        print e2
        try:
            db6.close()
        except:
            pass


def minusOne(itemid):
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """UPDATE extra_waypoints SET amount = amount - 1 WHERE id = '"""+str(itemid)+"""' """
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e2:
        print e2
        try:
            db6.close()
        except:
            pass

def changeText():
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """UPDATE variables SET value = '"""+str(html_text).replace("'","\\'")+"""' WHERE name = '"""+str(html_name)+"""' """
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e2:
        print e2
        try:
            db6.close()
        except:
            pass

def changeConfig():
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """INSERT INTO config (name, value) VALUES ('"""+str(html_name)+"""', '"""+str(html_text)+"""')"""   
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e2:
        try:
            db6.close()
        except:
            pass
        try:
            db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
            cursor6 = db6.cursor()
            command6 = """UPDATE config SET value = '"""+str(html_text).replace("'","\\'")+"""' WHERE name = '"""+str(html_name)+"""' """
            cursor6.execute(command6)
            db6.commit()
            db6.close()
        except Exception, e2:
            print e2
            try:
                db6.close()
            except:
                pass

def deleteConfig():
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """DELETE FROM `config` WHERE `config`.`name` = '"""+str(html_name)+"""' """
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e2:
        print e2
        try:
            db6.close()
        except:
            pass

def deleteUser():
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """DELETE FROM `user` WHERE `user`.`chatid` = """+str(html_id)+""";"""
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e:
        print e
        try:
            db6.close()
        except:
            pass


def get_admins():
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """SELECT value FROM config WHERE name = 'admin_ids'"""
        cursor6.execute(command6)
        data = cursor6.fetchall()
        db6.close()
        return data[0]
    except Exception, e:
        print e



def makeAdmin():
    try:
        the_admins = str(get_admins())
        the_admins.replace("Null","")
    except:
        the_admins = ""

    the_admins = the_admins + "," + str(html_id)
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """INSERT INTO config (name, value) VALUES ('admin_chatids', '"""+str(html_id)+"""')"""   
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e2:
        try:
            db6.close()
        except:
            pass
        try:
            db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
            cursor6 = db6.cursor()
            command6 = """UPDATE config SET value = '"""+str(the_admins).replace("'","\\'")+"""' WHERE name = 'admin_chatids' """
            cursor6.execute(command6)
            db6.commit()
            db6.close()
        except Exception, e2:
            print e2
            try:
                db6.close()
            except:
                pass


def deleteTriggerClient():
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """DELETE FROM `trigger_clients` WHERE `trigger_clients`.`name` = '"""+str(html_id)+"""';"""
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e:
        print e
        try:
            db6.close()
        except:
            pass


action_message = ""
if (str(action) == "addReason"):
    addReason(html_text, html_text_kurz)
elif (str(action) == "deleteReason"):
    deleteReason()
elif (str(action) == "deleteWaypoint"):
    removeWaypoint(html_id)
elif (str(action) == "deleteAllWaypoints"):
    removeAllWaypoints()
elif (str(action) == "deleteItem"):
    removeItem(html_id)
elif (str(action) == "deleteEmptyItem"):
    removeEmptyItem()
elif (str(action) == "deleteAllItem"):
    removeAllItem()
elif (str(action) == "deleteFile"):
    deleteFile()
elif (str(action) == "uploadFile"):
    save_uploaded_file()
elif (str(action) == "minusItem"):
    minusOne(html_id)
elif (str(action) == "plusItem"):
    plusOne(html_id)
elif (str(action) == "changeText"):
    changeText()
elif (str(action) == "changeConfig"):
    changeConfig()
elif (str(action) == "deleteConfig"):
    deleteConfig()
elif (str(action) == "deleteUser"):
    deleteUser()
elif (str(action) == "makeAdmin"):
    makeAdmin()
elif (str(action) == "deleteTriggerClient"):
    deleteTriggerClient()
elif (str(action) == "chanceItem"):
    chanceItem(html_id)
elif (str(action) == "changeDistance"):
    changeDistance(html_id)
elif (str(action) == "saveChase"):
    save_chase()
elif (str(action) == "loadChase"):
    load_chase()
elif (str(action) == "deleteChase"):
    delete_chase()
elif (str(action) == "resetChase"):
    reset_chase()
elif (str(action) == "enable_update"):
    enable_update()
elif (str(action) == "disable_update"):
    disable_update()





vars = get_variables()
wps = get_waypoints()
itms = get_items()
reasons = get_deathreasons()
user = get_user()

type_dict = GetInventoryTypes()
emojidict = GetEmojis()



GotNoStartPoint = True
GotGap = True


wparray = []
wparray.append(-1)
for i in wps:
    id = i[0]
    wparray.append(id)
    if int(id) == 0:
        GotNoStartPoint = False

def return_missing_numbers(numberarray):
    a=numberarray

    from itertools import imap, chain
    from operator import sub
    values = list(chain.from_iterable((a[i] + d for d in xrange(1, diff))
                        for i, diff in enumerate(imap(sub, a[1:], a))
                        if diff > 1))

    return values

verifywps = return_missing_numbers(wparray)
if len(verifywps) == 0:
    GotGap = False


print """
<h1 style="margin-bottom: 5px"><a href="index.cgi">"""+str(pagename)+"""</a> - <a href='https://t.me/"""+str(botname)+"""'>Bot</a> </h1>"""

print """

<div class="tab">"""
print '''
<button class="'''+str(weg)+'''" onclick="openOption(event, 'Wegpunkte')">Wegpunkte</button>
<button class="'''+str(items)+'''" onclick="openOption(event, 'Items')">Gegenstände</button>
'''
if str(invincible) == "0":
    print '''<button class="'''+str(deathreason)+'''" onclick="openOption(event, 'deathreason')">Todes Gründe</button>'''
print '''
<button class="'''+str(dateien)+'''" onclick="openOption(event, 'Dateien')">Dateien</button>
<button class="'''+str(benutzer)+'''" onclick="openOption(event, 'user')">Benutzer</button>
'''
if str(advanced) == "1":
    print '''<button class="'''+str(triggerclients)+'''" onclick="openOption(event, 'triggerclients')">Trigger Clients</button>'''
print '''
<button class="'''+str(variablen)+'''" onclick="openOption(event, 'Variablen')">Variablen</button>
<button class="'''+str(configtab)+'''" onclick="openOption(event, 'Configtab')">Optionen</button>
'''

print """
</div>

<div id="Variablen" """+str(variablens)+""" class="tabcontent" style="min-height: 250px">"""

if (str(action) == "changeText"):
    print "<div><b>Änderung gespeichert!</b></div>"


print """<div>"""
for i in vars:
    var = i[0]
    text = i[1].encode("UTF-8")
    print "<div id='var-parent' style='clear:both;'><div style='float: left; width: 160px'><b>"+str(var)+"</b></div> <div class='var-field' style='float: left'>"+str(text)+"</div></div>"
print """

<div style='clear:both; padding-top: 15px;'></div>

<div >
<form action="index.cgi" method="POST">
<input type="hidden" name="action" value="changeText">
<input type="hidden" name="tab" value="variablen">

<div>
    <div style="float: left">
        <label for="name">Variable</label>
    </div>

    <div style="width: 150px">
    <select id="name" name="name">
    """

for i in vars:
    var = i[0]
    text = i[1].encode("UTF-8")
    print '<option value="'+str(var)+'">'+str(var)+'</option>'
print """
        </select>
    </div>


</div>

<div>
    <div style="width: 150px;">
        <label for="text">Text</label>
    </div>
    <div style="loat: left">
        <textarea style="border: 1px solid #ccc;" rows="6" id="text" name="text" value=""></textarea>
    </div>
</div>

<div><button>Änderung speichern!</button>
</div>

</form>
</div>
</div>







</div>
</div>


<div id="Configtab" """+str(configtabs)+""" class="tabcontent" style="min-height: 250px">"""

if (str(action) == "restart"):
    print "<div><b>Gui & Bot werden neu gestartet!</b></div>"
    print "<div><b>Gui startet in kürze neu!</b></div>"
    print """
<script>

setTimeout(function(){ window.location.assign('/htbin/index.cgi?tab=config&action=restartDone'); }, 8000);

</script>
"""
elif (str(action) == "restartDone"):
    print "<div><b>Gui & Bot wurde neu gestartet!</b></div>"
elif (str(action) == "saveChase"):
    print "<div><b>Schnitzeljagdt unter '"+str(html_name)+"' gespeichert!</b></div>"
elif (str(action) == "loadChase"):
    print "<div><b>Schnitzeljagdt '"+str(html_name)+"' geladen!</b></div>"
elif (str(action) == "resetChase"):
    print "<div><b>Alle aktuellen Wegpunkte und Gegenstände wurden gelöscht!</b></div>"
elif (str(action) == "resetChase"):
    print "<div><b>Projekt '"+str(html_name)+"' gelöscht!</b></div>"
elif (str(action) == "changeConfigDone"):
    print "<div><b>Variable '"+str(html_name)+"' gespeichert!</b></div>"
elif (str(action) == "changeConfig"):
    print "<div><b>Variable '"+str(html_name)+"' gespeichert!</b></div>"
    print """
<script>
function newDoc() {
    window.location.assign('/htbin/index.cgi?tab=config&action=changeConfigDone&name="""+html_name+"""')
}

newDoc()
</script>
"""
elif (str(action) == "enable_updateDone"):
    print "<div><b>Update beim starten wurde aktiviert!</b></div>"
elif (str(action) == "enable_update"):
    print "<div><b>Update beim starten wurde aktiviert!</b></div>"
    print """
<script>
function newDoc() {
    window.location.assign('/htbin/index.cgi?tab=config&action=enable_updateDone')
}

newDoc()
</script>
"""
elif (str(action) == "disable_updateDone"):
    print "<div><b>Update beim starten wurde deaktiviert!</b></div>"
elif (str(action) == "disable_update"):
    print "<div><b>Update beim starten wurde deaktiviert!</b></div>"
    print """
<script>
function newDoc() {
    window.location.assign('/htbin/index.cgi?tab=config&action=disable_updateDone')
}

newDoc()
</script>
"""
elif (str(action) == "deleteConfigDone"):
    print "<div><b>Variable '"+str(html_name)+"' wurde gelöscht!</b></div>"
elif (str(action) == "deleteConfig"):
    print "<div><b>Variable '"+str(html_name)+"' wurde gelöscht!</b></div>"
    print """
<script>
function newDoc() {
    window.location.assign('/htbin/index.cgi?tab=config&action=deleteConfigDone&name="""+html_name+"""')
}

newDoc()
</script>
"""


print """<div>"""
print """

<div style='clear:both; padding-top: 15px;'></div>



<div id='speichern' style='border: 1px solid rgb(204, 204, 204); padding: 5px; margin:5px; height: 25px; overflow: hidden; '>
<h3 onclick="toggleSpeichern()" style="margin-top: 5px">Projekt speichern</h3>
<form action="index.cgi" method="GET">
<input type="hidden" name="action" value="saveChase">
<input type="hidden" name="tab" value="config">

<div>
    <div style="float: left">
    <input style="width: 150px; display:table-cell; vertical-align:middle;" id="name" name="name" type="text"></input>
   </div>
</div>

<div><button style="margin-left: 5px; width 80px">speichern</button>
</div>

</form>
<div style="font-size: 14px; color: red">ACHTUNG! Eventuell exitierende Daten werden überschrieben!</div>
</div>


<script>
function toggleSpeichern() {
    var el = document.getElementById('speichern');

    if ( el.style.overflow == 'hidden' ) {
        el.style.overflow = 'visible' 
        el.style.height = 'auto'
    }
    else {
        el.style.overflow = 'hidden' 
        el.style.height = '25px'
    } 
}
</script>






<div id='laden' style='border: 1px solid rgb(204, 204, 204); padding: 5px; margin:5px; height: 25px; overflow: hidden; '>
<h3 onclick="toggleLaden()" style="margin-top: 5px">Projekt laden</h3>
<form action="index.cgi" method="GET">
<input type="hidden" name="action" value="loadChase">
<input type="hidden" name="tab" value="config">

<div>
    <div style="float: left; width: 150px; display:table-cell; vertical-align:middle;">
        <select style="float: left; width: 150px; display:table-cell; vertical-align:middle;" id="name" name="name">"""
for i in chases:
    var = i[0]
    var = var[7:]
    print '<option  value="'+str(var)+'">'+str(var)+'</option>'
print """
        </select>
    </div>


</div>

<div ><button style="margin-left: 5px; width 80px">laden</button>
</div>

</form>
<div style="font-size: 14px; color: red">ACHTUNG! Ungespeicherte Daten gehen unwiederruflich verloren!</div>
</div>



<script>
function toggleLaden() {
    var el = document.getElementById('laden');

    if ( el.style.overflow == 'hidden' ) {
        el.style.overflow = 'visible' 
        el.style.height = 'auto'
    }
    else {
        el.style.overflow = 'hidden' 
        el.style.height = '25px'
    } 
}
</script>


<div id='loeschen' style='border: 1px solid rgb(204, 204, 204); padding: 5px; margin:5px; height: 25px; overflow: hidden; '>
<h3 onclick="toggleLoeschen()"  style="margin-top: 5px">Projekt löschen</h3>
<form action="index.cgi" method="GET">
<input type="hidden" name="action" value="deleteChase">
<input type="hidden" name="tab" value="config">

<div>
    <div style="float: left; width: 150px; display:table-cell; vertical-align:middle;">
        <select style="float: left; width: 150px; display:table-cell; vertical-align:middle;" id="name" name="name">"""
for i in chases:
    var = i[0]
    var = var[7:]
    print '<option  value="'+str(var)+'">'+str(var)+'</option>'
print """
        </select>
    </div>


</div>

<div><button style="margin-left: 5px; width 80px">löschen</button>
</div>

</form>
<div style="font-size: 14px; color: red">ACHTUNG! Projekt geht unwiederruflich verloren!</div>
</div>



<script>
function toggleLoeschen() {
    var el = document.getElementById('loeschen');

    if ( el.style.overflow == 'hidden' ) {
        el.style.overflow = 'visible' 
        el.style.height = 'auto'
    }
    else {
        el.style.overflow = 'hidden' 
        el.style.height = '25px'
    } 
}
</script>

<div id='optionen' style='border: 1px solid rgb(204, 204, 204); padding: 5px; margin:5px; height: 25px; overflow: hidden; '>
<h3 onclick="toggleOptionen()" style="margin-top: 5px">Aktionen</h3>

<div style="height: 100px">
<div style="float: left">
    <form action="index.cgi" method="POST">
    <input type="hidden" name="action" value="resetChase">
    <input type="hidden" name="tab" value="config">

    <div><button>Aktives Projekt Zurücksetzen</button></div>
    </form>

    <form action="index.cgi" method="POST">
    <input type="hidden" name="action" value="restart">
    <input type="hidden" name="tab" value="config">"""

restart_text = "Bot & Gui Neustarten"
if auto_start_update:
    restart_text = "Bot & Gui Updaten und Neustarten"
if sudo_access:
    print """<div ><button>"""+restart_text+"""</button></div>"""

print """
    </form>

    <div style="font-size: 14px; color: red">ACHTUNG! Ungespeicherte Daten gehen unwiederruflich verloren!</div>
</div>

<div style="float: left">
    <form action="index.cgi" method="POST">
    <input type="hidden" name="action" value="enable_update">
    <input type="hidden" name="tab" value="config">

    <div><button>Update beim Start aktivieren</button></div>
    </form>

    <form action="index.cgi" method="POST">
    <input type="hidden" name="action" value="disable_update">
    <input type="hidden" name="tab" value="config">

    <div><button>Update beim Start deaktivieren</button></div>
    </form>


</div>
</div>

</div>
</div>


<script>
function toggleOptionen() {
    var el = document.getElementById('optionen');

    if ( el.style.overflow == 'hidden' ) {
        el.style.overflow = 'visible' 
        el.style.height = 'auto'
    }
    else {
        el.style.overflow = 'hidden' 
        el.style.height = '25px'
    } 
}
</script>



<div id='configvars' style='clear:both; border: 1px solid rgb(204, 204, 204); padding: 5px; margin:5px; height: 25px; overflow: hidden; '>
<h3 onclick="toggleConfigvars()" style="margin-top: 5px">config.ini overwrite</h3>

<div>"""


for i in configdata:
    var = i[0]
    text = i[1].encode("UTF-8")
    removeurl = '<div style="float: right"><a class="eLink" href="index.cgi?action=deleteConfig&tab=config&name='+str(var)+'">[ X ]</a></div>'
    
    print "<div style='clear:both; height: 20px'><div style='float: left; width: 180px'><b>"+str(var)+"</b></div><div style='float: left; width: 30px'></div> <div class='config-field' style='float: left'>"+str(text)+"</div> "+str(removeurl)+"</div>"


print """



<br>
<div>
<form action="index.cgi" method="POST">
<input type="hidden" name="action" value="changeConfig">
<input type="hidden" name="tab" value="config">

<div style="float: left; width: 150px">
    <input id="name" name="name" placeholder="Neu Variable">
</div>

<div style='float: left; padding-left: 30px'></div>
<div class='config-field' style='float: left'>
        <input id="text" name="text" placeholder="Neuer Wert">

</div>
<div style="clear: both; padding-top: 10px">
<button>hinzufügen/überschreiben</button>
</div>
</form>


</div>


</div>
</div>


<script>
function toggleConfigvars() {
    var el = document.getElementById('configvars');

    if ( el.style.overflow == 'hidden' ) {
        el.style.overflow = 'visible' 
        el.style.height = 'auto'
    }
    else {
        el.style.overflow = 'hidden' 
        el.style.height = '25px'
    } 
}
</script>


</div>
</div>

<div id="Wegpunkte" """+str(wegs)+""" class="tabcontent" style="min-height: 250px">"""
  
if GotNoStartPoint:
    print "<div><font color='red'><b>Achtung du hast keinen Startpunkt!<br>Lege unbedingt Wegpunkt 0 an!</b></font></div>"


if GotGap:
    print "<div><font color='red'><b>Achtung deine Wegpunkte haben eine Lücke!</b></font></div>"
print """
<div>

"""

if (str(action) == "deleteWaypoint"):
    print "<div><b>Wegpunkt von der Karte entfernt!</b></div>"
print """
<h2 style="margin-top: 5px"><a href="map.cgi">[Karte]</a><br><p></h2>"""
for i in wps:
    print "<div id='waypoint"+str(i[0])+"' style='height: 25px; overflow: hidden; padding: 5px; margin-bottom: 10px; border: 1px solid #ccc;'>"
    id = i[0]
    location = i[1]
    lat = location.split(",")[0][0:9]
    long = location.split(",")[1][0:9]
    location = lat+","+long
    urllocation = "<a target='_new' href='https://www.google.com/maps/search/?api=1&query="+location+"'>"+location+"</a>"
    try:
        text = i[2].encode("utf-8")
    except:
        text = "None"
    bild = i[3]
    audio = i[4]
    video = i[5]
    voice = i[6]
    samtrigger = i[7]
    try:
        wname = str(i[13])
    except:
        wname = "Null"

    try:
        wdistance = str(i[14])+ "m"
        if wdistance == "0m":
            wdistance = "Default"
    except:
        wdistance = "Default"

    texticon = ""
    picicon = ""
    audioicon = ""
    videoicon = ""
    voiceicon = ""
    triggericon = ""
    questionicon = ""


    removeurl = '<div><a class="eLink" href="index.cgi?action=deleteWaypoint&tab=wegpunkte&id='+str(id)+'">[entfernen]</a></div>'
    editurl = """<a href="website" onclick="openwindow('waypoint.cgi?id="""+str(id)+"""'); return false;">[editieren]<a/>"""
 
    try:
        question = i[9].encode("UTF-8")
    except:
        question = "None"
    try:
        is_wrong = i[10].encode("UTF-8")
    except:
        is_wrong = "None"
    try:
        is_right = i[11].encode("UTF-8")
    except:
        is_right = "None"
    try:
        is_wrong2 = i[12].encode("UTF-8")
    except:
        is_wrong2 = "None"


    if str(text) != "None":
        texticon = '📝'

    if str(bild) != "None":
        picicon = '🖼️'

    if str(audio) != "None":
        audioicon = '🔊'

    if str(video) != "None":
        videoicon = '📺'

    if str(voice) != "None":
        voiceicon = '🗣️'

    if str(samtrigger) != "None":
        triggericon = '🕹️'

    if str(is_wrong2) != "None":
        questionicon = '❓❓'
    elif str(is_wrong) != "None":
        questionicon = '❓'

    statusbar = texticon + picicon + audioicon + videoicon + voiceicon + triggericon + questionicon


    waypointname = "Wegpunkt "+str(id).replace("None","-")
    if ((str(wname) != "") and (str(wname) != "Null")):
        waypointname = "["+ str(id) +"] " + str(wname)
    
    print "<div onclick='toggleWaypoint"+str(i[0])+"()' style='padding-bottom: 10px'><b>"+waypointname+"</b> "+statusbar+"</div>"
    print "<div>Text: "+str(text).replace("None","-")+"</div>"
    print "<div>Radius: "+str(wdistance).replace("None","-")+"</div>"
    print "<div>Ort: "+str(urllocation).replace("None","-")+"</div>"
    print "<div>Bild: "+str(bild).replace("None","-")+"</div>"
    print "<div>Audio: "+str(audio).replace("None","-")+"</div>"
    print "<div>Video: "+str(video).replace("None","-")+"</div>"
    print "<div>Sprache: "+str(voice).replace("None","-")+"</div>"
    print "<div>Trigger: "+str(samtrigger).replace("None","-")+"</div>"
    print "<div>Frage: "+str(question).replace("None","-")+"</div>"
    if str(question) != "None":
        print "<div>Richtige Antwort: "+str(is_right).replace("None","-")+"</div>"
        print "<div>Falsche Antwort #1: "+str(is_wrong).replace("None","-")+"</div>"
        if str(is_wrong2) != "None":
            print "<div>Falsche Antwort #2: "+str(is_wrong2).replace("None","-")+"</div>"

    print "<br>"
    print editurl
    print "<br>"
    print removeurl
    print "</div>"
    print """
    <script>
function toggleWaypoint"""+str(i[0])+"""() {
    var el = document.getElementById('waypoint"""+str(i[0])+"""');

    if ( el.style.overflow == 'hidden' ) {
        el.style.overflow = 'visible' 
        el.style.height = 'auto'
    }
    else {
        el.style.overflow = 'hidden' 
        el.style.height = '25px'
    } 
}
</script>"""

print """
<a class="eLink" href="index.cgi?action=deleteAllWaypoints&tab=wegpunkte">[Alle Wegpunkte entfernen]</a>
</div>
</div>


<div id="Items" """+str(itemss)+""" class="tabcontent" style="min-height: 250px">

<div>"""
if (str(action) == "deleteItem"):
    print "<div><b>Gegenstand von der Karte entfernt!</b></div>"
elif (str(action) == "plusItem"):
    print "<div><b>Menge wurde um +1 erhöht</b></div>"
elif (str(action) == "minusItem"):
    print "<div><b>Menge wurde um -1 gesenkt</b></div>"
elif (str(action) == "chanceItem"):
    print "<div><b>Fundchance wurde angepasst</b></div>"
elif (str(action) == "changeDistance"):
    print "<div><b>Reaktions Distanz wurde angepasst!</b></div>"


print """



<h2 style="margin-top: 5px"><a href="map.cgi">[Karte]</a><br><p></h2>"""
for i in itms:
    id = i[0]
    location = i[1]
    mylocation = "0,0"

    try:
        #location = i[3]
        location = location.encode("utf-8")
#        print location
        
        lat = location.split(",")[0][0:9].strip()
        long = location.split(",")[1][0:9].strip()
        mylocation = lat+","+long
    except Exception, e:
        print e
        location = "0,0"

    urllocation = "<a target='_new' href='https://www.google.com/maps/search/?api=1&query="+mylocation+"'>[Karte]</a>"
    type = str(i[2])
    amount = i[3]
    chance = i[4]
    distanceValue = i[5]
    typename = type_dict[type]
    typename = typename.split(",")[0]
    emoji = emojidict[str(type)]
    chance_form = """<form style="display:inline" action="index.cgi" method="post">

<input type='hidden' name='id' value='"""+str(id)+"""'>
<input type="hidden" name="action" value="chanceItem">
<input type="hidden" name="tab" value="items">

<select onchange="this.form.submit()" name="value">"""

    if int(chance) == 10:
        chance_form = chance_form + '<option value="10" selected>10%</option>'
    else:
        chance_form = chance_form + '<option value="10">10%</option>'
        
    if int(chance) == 20:
        chance_form = chance_form + '<option value="20" selected>20%</option>'
    else:
        chance_form = chance_form + '<option value="20">20%</option>'
        
    if int(chance) == 30:
        chance_form = chance_form + '<option value="30" selected>30%</option>'
    else:
        chance_form = chance_form + '<option value="30">30%</option>'
        
    if int(chance) == 40:
        chance_form = chance_form + '<option value="40" selected>40%</option>'
    else:
        chance_form = chance_form + '<option value="40">40%</option>'
        
    if int(chance) == 50:
        chance_form = chance_form + '<option value="50" selected>50%</option>'
    else:
        chance_form = chance_form + '<option value="50">50%</option>'
        
    if int(chance) == 60:
        chance_form = chance_form + '<option value="60" selected>60%</option>'
    else:
        chance_form = chance_form + '<option value="60">60%</option>'
        
    if int(chance) == 70:
        chance_form = chance_form + '<option value="70" selected>70%</option>'
    else:
        chance_form = chance_form + '<option value="70">70%</option>'
        
    if int(chance) == 80:
        chance_form = chance_form + '<option value="80" selected>80%</option>'
    else:
        chance_form = chance_form + '<option value="80">80%</option>'
        
    if int(chance) == 90:
        chance_form = chance_form + '<option value="90" selected>90%</option>'
    else:
        chance_form = chance_form + '<option value="90">90%</option>'
        
    if int(chance) == 100:
        chance_form = chance_form + '<option value="100" selected>100%</option>'
    else:
        chance_form = chance_form + '<option value="100">100%</option>'

    chance_form = chance_form + """
</select>

</form>"""

    distance_form = """<form style="display:inline" action="index.cgi" method="post">

<input type='hidden' name='id' value='"""+str(id)+"""'>
<input type="hidden" name="action" value="changeDistance">
<input type="hidden" name="tab" value="items">

<select onchange="this.form.submit()" name="value">"""

    if int(distanceValue) == 0:
        distance_form = distance_form + '<option value="0" selected>Globale Einstellung</option>'
    else:
        distance_form = distance_form + '<option value="0">Globale Einstellung</option>'


    if int(distanceValue) == 10:
        distance_form = distance_form + '<option value="10" selected>10m</option>'
    else:
        distance_form = distance_form + '<option value="10">10m</option>'
        

    if int(distanceValue) == 20:
        distance_form = distance_form + '<option value="20" selected>20m</option>'
    else:
        distance_form = distance_form + '<option value="20">20m</option>'
        
    if int(distanceValue) == 30:
        distance_form = distance_form + '<option value="30" selected>30m</option>'
    else:
        distance_form = distance_form + '<option value="30">30m</option>'
        
    if int(distanceValue) == 40:
        distance_form = distance_form + '<option value="40" selected>40m</option>'
    else:
        distance_form = distance_form + '<option value="40">40m</option>'
        
    if int(distanceValue) == 50:
        distance_form = distance_form + '<option value="50" selected>50m</option>'
    else:
        distance_form = distance_form + '<option value="50">50m</option>'
        
    if int(distanceValue) == 60:
        distance_form = distance_form + '<option value="60" selected>60m</option>'
    else:
        distance_form = distance_form + '<option value="60">60m</option>'
        
    if int(distanceValue) == 70:
        distance_form = distance_form + '<option value="70" selected>70m</option>'
    else:
        distance_form = distance_form + '<option value="70">70m</option>'
        
    if int(distanceValue) == 80:
        distance_form = distance_form + '<option value="80" selected>80m</option>'
    else:
        distance_form = distance_form + '<option value="80">80m</option>'
        
    if int(distanceValue) == 90:
        distance_form = distance_form + '<option value="90" selected>90m</option>'
    else:
        distance_form = distance_form + '<option value="90">90m</option>'
        
    if int(distanceValue) == 100:
        distance_form = distance_form + '<option value="100" selected>100m</option>'
    else:
        distance_form = distance_form + '<option value="100">100m</option>'

    distance_form = distance_form + """
</select>

</form>"""
    deleteurl = '<a class="eLink" href="index.cgi?action=deleteItem&tab=items&id='+str(id)+'">[entfernen]</a>'
    plusone = '<a href="index.cgi?action=plusItem&tab=items&id='+str(id)+'">[+1]</a>'
    minusone = '<a href="index.cgi?action=minusItem&tab=items&id='+str(id)+'">[-1]</a>'

    print "<div style='float: left; width: 40px'>"+str(amount)+"x</div><div><img style='height: 12px; width: 12px' src='/img/emoji/"+str(type)+".png'></img> "+minusone+""+plusone+" "+distance_form+" Radius "+chance_form+" Chance "+deleteurl+" "+str(urllocation)+"</div>"
print """

</div>
<div style="padding-top: 20px"><a class="eLink" href="index.cgi?action=deleteEmptyItem&tab=items">[Leere Gegenstände entfernen]</a></div>
<div><a class="eLink" href="index.cgi?action=deleteAllItem&tab=items">[Alle Gegenstände entfernen]</a></div>

</div>
</div>
"""

print """
<div id="deathreason" """+str(deathreasons)+""" class="tabcontent" style="min-height: 250px">


"""


if (str(action) == "addReason"):
    print "<div><b>Todesursache hinzugefügt!</b></div>"
elif (str(action) == "deleteReason"):
    print "<div><b>Todesursache entfernt!</b></div>"

for i in reasons:
    id = i[0]
    try:
        text = i[1].encode("utf-8")
    except:
        text = "None"

    try:
        text_short = i[2].encode("utf-8")
    except:
        text_short = "None"

    inuse = i[3]

    if (str(id) != "1") and (str(id) != "0"):
        deleteurl = '<a class="eLink" href="index.cgi?action=deleteReason&tab=todesursache&id='+str(id)+'">[entfernen]</a>'
    else:
        deleteurl = ''
    print "<div id='death-parent' style='clear:both;'><div style='float: left; width: 300px'><b>"+str(text_short)+"</b></div> <div class='death-field' style='float: left'>"+str(text)+" "+str(deleteurl)+"</div></div>"





print """
<div>
<div style='clear:both; padding-top: 15px;'></div>
<div >
<form action="index.cgi" method="POST">
<input type="hidden" name="action" value="addReason">
<input type="hidden" name="tab" value="todesursache">

<div>
    <div style="float: left">
        <label for="text_kurz">Tot durch</label>
    </div>

    <div style="clear: both; width: 300px">
        <input style="border: 1px solid #ccc;" id="text_kurz" name="text_kurz" value="">
    </div>
</div>

<div>
    <div style="clear: both; width: 150px;">
        <label for="text">Text</label>
    </div>
    <div style="float: left">
        <textarea style="border: 1px solid #ccc;" rows="6" id="text" name="text" value="">
        </textarea>
    </div>
</div>

<div style="margin-top: 60px"><button>hinzufügen</button>
</div>

</form>
</div>
</div>
</div>
</div>

"""


print """


<div id="user" """+str(benutzers)+""" class="tabcontent" style="min-height: 250px">"""
if (str(action) == "deleteUser"):
    print """<div><b>Benutzer wurde gelöscht!</b></div>"""

for i in user:
    chatid = i[0]
    location = i[1]
    waypoint = i[2]
    username = i[3]
    livestatus = i[4]
    inventory = i[5]
    points = i[6]
    mylocation = "0,0"

    try:
        username = i[3].encode("utf-8")
    except:
        username = "None"

    try:
        location = location.encode("utf-8")
        lat = location.split(",")[0][0:9].strip()
        long = location.split(",")[1][0:9].strip()
        mylocation = lat+","+long
    except:
        location = "0,0"

    inventoryarray = inventory.split(",")
    userinventory = "[ "
    for i2 in inventoryarray:
        if len(i2) >= 1:
            userinventory = userinventory + "<img style='height: 8px; width: 8px' src='/img/emoji/"+str(i2)+".png'></img> "

    userinventory = userinventory + "]"
    urllocation = "<a target='_new' href='https://www.google.com/maps/search/?api=1&query="+mylocation+"'>[Karte]</a>"
    deleteurl = '<a class="eLink" href="index.cgi?action=deleteUser&tab=benutzer&id='+str(chatid)+'">[entfernen]</a>'
    makeadminurl = '<a href="index.cgi?action=makeAdmin&tab=benutzer&id='+str(chatid)+'">'+str(chatid)+'</a>'

    print "<div><b>"+username+" "+str(makeadminurl)+"</b> "+userinventory+" "+urllocation+"  "+deleteurl+" </div>"

print """
</div>




<div id="triggerclients" """+str(triggerclientss)+""" class="tabcontent" style="min-height: 250px">
<div style="padding-bottom: 10px">"""
if (str(action) == "deleteTriggerClient"):
    print "<div><b>Client wurde gelöscht!</b></div>"


for i in printTriggerClients():
    fname = i[0]
    ftrigger = i[1]
    fbattery = i[2]
    flast_seen = i[3]


    deleteurl = '<a class="eLink" href="index.cgi?action=deleteTriggerClient&tab=triggerclients&id='+str(fname)+'">[entfernen]</a>'
    print """<div style="clear:both;"><div style="float: left; width: 120px; margin-top: 6px"><b>"""+str(fname)+"""</b></div> <div style="float: left">💡"""+str(ftrigger)+""" 🔋"""+str(fbattery)+"""% 🕑"""+str(flast_seen)+"""  """ +str(deleteurl)+"""</div></div>"""


print """<div style="clear:both; padding-top: 20px"><a target="_new" href="https://play.google.com/store/apps/details?id=cloudffm.eu.samtrigger">[Download Client from Android PlayStore]</a></div>"""
print """<div style="clear:both;"><a target="_new" href="../trigger/trigger.apk">[Download Client]</a></div>"""
print "</div>"
print """
</div>



<div id="Dateien" """+str(dateiens)+""" class="tabcontent" style="min-height: 250px">
<div style="padding-bottom: 10px">"""
if (str(action) == "uploadFile"):
    print """<div><b>Datei erfolgreich hochgeladen!</b></div>"""

if (str(action) == "deleteFile"):
    print "<div><b>Datei wurde gelöscht!</b></div>"

print "</div>"
print printFiles()
print """
<div style="padding-top: 50px">
<form method="post" action="index.cgi" enctype="multipart/form-data">
 <div>
    <input name="datei" type="file" size="50"> 
    <input name="action" type="hidden" value="uploadFile"> 
    <input name="tab" type="hidden" value="dateien"> 
</div>
<div>
  <button>Hochladen</button>
</div>
</form>

</div>
</div>"""


print """

<script>
function getFieldWidth() {
    var cols2 = document.getElementsByClassName('tabcontent');
    var mywidth2 = 0
    for(i=0; i<cols2.length; i++) {
        var data = cols2[i].clientWidth
        if (parseInt(data) >= 1) {
            mywidth2 = String(cols2[i].clientWidth)
        }
      
    }

    var newvalue = (parseInt(mywidth2.replace(/px/,""))-200)+"px";

    var cols3 = document.getElementsByClassName('var-field');
    for(i=0; i<cols3.length; i++) {
      cols3[i].style.width =  newvalue;
    }


    var newvalue2 = (parseInt(mywidth2.replace(/px/,""))-500)+"px";

    var cols3 = document.getElementsByClassName('config-field');
    for(i=0; i<cols3.length; i++) {
      cols3[i].style.width =  newvalue2;
    }
};

</script>
<script>
getFieldWidth();
</script>"""

if str(invincible) == "0":
    print """
<script>
function getFieldWidthDeath() {
    var cols2 = document.getElementsByClassName('tabcontent');
    var mywidth2 = 0
    for(i=0; i<cols2.length; i++) {
        var data = cols2[i].clientWidth
        if (parseInt(data) >= 1) {
            mywidth2 = String(cols2[i].clientWidth)
        }
      
    }

    var newvalue = (parseInt(mywidth2.replace(/px/,""))-340)+"px";

    var cols3 = document.getElementsByClassName('death-field');
    for(i=0; i<cols3.length; i++) {
      cols3[i].style.width =  newvalue;
    }
};

</script>
<script>
getFieldWidthDeath();
</script>"""

print """
<script>
function openOption(evt, cityName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(cityName).style.display = "block";
    document.getElementById(cityName).style.overflow = "auto";
    
    evt.currentTarget.className += " active";
    getFieldWidth();"""
if str(invincible) == "0":
    print "getFieldWidthDeath();"
print """
}
</script>

</div>"""

if (str(action) == "restart"):
    restart()


print "</body>"
