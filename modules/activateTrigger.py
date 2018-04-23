#!/usr/bin/python
import sys
import time

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


reset_minutes = str(getconfig('reset_minutes'))
www_path = trigger


if len(sys.argv) <= 1:
    print "No trigger provided"
    sys.exit()

trigger = sys.argv[1]


def readtrigger(triggerfile):
    triggerdatafile = www_path + "/" + triggerfile
    f = open(triggerdatafile, 'r')
    triggerx = f.read().strip()
    f.close()
    return triggerx

def writetrigger(triggerfile, triggerx):
    triggerdatafile = www_path + "/" + triggerfile
    f = open(triggerdatafile, 'w')
    f.write(triggerx)
    f.close()

def writeweb(trigger_1, trigger_2, trigger_3):
    triggerdatafile = www_path + "/trigger.htm"
    f = open(triggerdatafile, 'w')
    towrite = "trigger1: "+str(trigger_1)+"::trigger2: "+str(trigger_2)+"::trigger3: "+str(trigger_3)
    f.write(towrite)
    f.close()

trigger1 = readtrigger("trigger1")
trigger2 = readtrigger("trigger2")
trigger3 = readtrigger("trigger3")

if (trigger == "trigger1"):
    print 1
    print trigger2
    print trigger3
    writetrigger("trigger1", "1")
#    writeweb("1", trigger2, trigger3)
elif (trigger == "trigger2"):
    print trigger1
    print 1
    print trigger3
    writetrigger("trigger2", "1")
#    writeweb(trigger1, "1", trigger3)
elif (trigger == "trigger3"):
    print trigger1
    print trigger2
    print 1
    writetrigger("trigger3", "1")
#    writeweb(trigger1, trigger2, "1")



tosleep = 60 * int(reset_minutes)
print "sleeping "+str(reset_minutes)+" minutes, to release the trigger"
time.sleep(tosleep)


if (trigger == "trigger1"):
    trigger2 = readtrigger("trigger2")
    trigger3 = readtrigger("trigger3")
    print 0
    print trigger2
    print trigger3
    writetrigger("trigger1", "0")
#    writeweb("0", trigger2, trigger3)
elif (trigger == "trigger2"):
    trigger1 = readtrigger("trigger1")
    trigger3 = readtrigger("trigger3")
    print trigger1
    print 0
    print trigger3
    writetrigger("trigger2", "0")
#    writeweb(trigger1, "0", trigger3)
elif (trigger == "trigger3"):
    trigger1 = readtrigger("trigger1")
    trigger2 = readtrigger("trigger2")
    print trigger1
    print trigger2
    print 0
    writetrigger("trigger3", "0")
#    writeweb(trigger1, trigger2, "0")
