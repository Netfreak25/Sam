#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Moritz Kuhn
#####################################################################
import cgitb, datetime, time,  cgi, sys, os, urllib2, requests, MySQLdb
cgitb.enable(display=1, logdir="/var/www/log/")


###### Read html input
form = cgi.FieldStorage()



try:
    mode = form["action"].value
    action = mode
except Exception, e:
    mode = "none"
    action = "none"
    pass

try:
    html_lat = form["lat"].value
except Exception, e:
    html_lat = "none"

try:
    html_lng = form["lng"].value
except Exception, e:
    html_lng = "none"

try:
    html_type = form["type"].value
except Exception, e:
    html_type = "none"


try:
    html_id = form["id"].value
except Exception, e:
    html_id = "none"

try:
    html_amount = form["amount"].value
except Exception, e:
    html_amount = "1"



html_location = ""
if (html_lat != "none"):
    html_location = html_lat+", "+html_lng

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

gmaps_key = str(getconfig('gmaps_key'))
zoom_koordinaten = str(getconfig('zoom_koordinaten'))
zoom_level = str(getconfig('zoom_level'))



trigger_distance_m = int(getconfig('trigger_distance_m'))
extra_distance_m = int(getconfig('extra_distance_m'))

sam_host = str(getconfig('sam_host'))
sam_db = str(getconfig('sam_db'))
sam_db_user = str(getconfig('sam_db_user'))
sam_db_pw = str(getconfig('sam_db_pw'))

print "Content-Type: text/html; charset=UTF-8"     # HTML is following
print                               # blank line, end of headers



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



def DropItem(type, location, amount):
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """INSERT INTO extra_waypoints (location, type, amount) VALUES ('"""+str(location)+"""', '"""+str(type)+"""', '"""+str(amount)+"""')"""
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e:
        print e
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

def highestid():
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = "SELECT id FROM `waypoints` ORDER BY `waypoints`.`id`  DESC LIMIT 1"
        cursor6.execute(command6)
        data = cursor6.fetchall()
        return data[0][0]
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



def addWaypoint(location):
    try:
        newid = int(highestid()) + 1
        newid = str(newid)
    except:
        newid = "0"
    try:
        db6 = MySQLdb.connect(sam_host,sam_db_user,sam_db_pw,sam_db, charset='utf8')
        cursor6 = db6.cursor()
        command6 = """INSERT INTO waypoints (id, location) VALUES ('"""+str(newid)+"""', '"""+str(location)+"""')"""
        cursor6.execute(command6)
        db6.commit()
        db6.close()
    except Exception, e:
        print e
        try:
            db6.close()
        except:
            pass


if (str(action) == "addWaypoint"):
    addWaypoint(html_location)

if (str(action) == "deleteWaypoint"):
    removeWaypoint(html_id)

if (str(action) == "addItem"):
    DropItem(html_type, html_location, html_amount)

if (str(action) == "deleteItem"):
    removeItem(html_id)


if (str(action) == "minusItem"):
    minusOne(html_id)

if (str(action) == "plusItem"):
    plusOne(html_id)

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
            p


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



# load variables from database
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




def typeDropDown():
    type_dict = GetInventoryTypes()
    emojidict = GetEmojis()
    print "<select name = 'type' style='display:table-cell; vertical-align:middle;'>"
    for i in type_dict:
        id = str(i)
        data = type_dict[i]
        name = str(data).split(",")[0] 
        beschreibung = str(data).split(",")[1] 
        print '<option value="'+str(id)+'">'+str(emojidict[id])+' '+str(name)+'</option>'
    print "</select>"




def AmounttypeDropDown():
    print "<select name = 'amount'>"
    count = 20
    for i in range(1,count):
        print '<option value="'+str(i)+'">'+str(i)+'</option>'
    print "</select>"


# load variables from database
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






action_message = ""
wps = get_waypoints()

try:
    val = wps[len(wps)-1][1].replace(" ","")
    zoom_koordinaten = str(val).strip()
except:
    pass



action_message = ""



itms = get_items()


type_dict = GetInventoryTypes()
emojidict = GetEmojis()


def importIcons():
    data = ""
    for i in range(1,22):
        data = data + """
    var image"""+str(i)+""" = {
    url: '/img/emoji/"""+str(i)+""".png',
    // This marker is 20 pixels wide by 32 pixels high.
    size: new google.maps.Size(16, 16),
    // The origin for this image is (0, 0).
    origin: new google.maps.Point(0, 0),
    // The anchor for this image is the base of the flagpole at (0, 32).
    anchor: new google.maps.Point(8, 8)
  };
  """
    return data



if (str(action) == "addItem"):
    action_message = "Gegenstand der Karte hinzugefügt: "+str(emojidict[html_type])

if (str(action) == "deleteItem"):
    action_message = "Gegenstand von der Karte gelöscht!"

if (str(action) == "plusItem"):
    action_message = "Menge wurde um +1 erhöht"

if (str(action) == "minusItem"):
    action_message = "Menge wurde um -1 gesenkt"

if (str(action) == "addWaypoint"):
    action_message = "Wegpunkt der Karte hinzugefügt!"

if (str(action) == "deleteWaypoint"):
    action_message = "Wegpunkt von der Karte gelöscht!"




def printWayPointMarker():
    data = ""
    count = 1
    for i in wps:
        id = i[0]
        location = i[1]
        try:
            text = i[2].encode("utf-8")
        except:
            text = "None"
            
        bild = i[3]
        audio = i[4]
        video = i[5]
        samtrigger = i[7]
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
    #    print "<div>"+str()+": "+str(text)+"</div>"
        extradata = ""
        extradata = extradata + "<br>Location: "+str(location)
        extradata = extradata + "<br>Bild: "+str(bild)
        extradata = extradata + "<br>Audio: "+str(audio)
        extradata = extradata + "<br>Video: "+str(video)
        extradata = extradata + "<br>Trigger: "+str(samtrigger)
        extradata = extradata + "<br>Frage: "+str(question)
        if str(question) != "None":
            extradata = extradata + "<br>Richtige Antwort: "+str(is_right)
            extradata = extradata + "<br>Falsche Antwort 1: "+str(is_wrong)
            if str(is_wrong2) != "None":
                extradata = extradata + "<br>Falsche Antwort 2: "+str(is_wrong)


        removeurl = '<a href="map.cgi?action=deleteWaypoint&id='+str(id)+'">entfernen<a/>'
        editurl = """<a href="website" onclick="openwindow(\\'waypoint.cgi?id="""+str(id)+"""\\'); return false;">editieren<a/>"""
        beschreibung = """Wegpunkt """+str(id)+""":<br><br>"""+str(text).replace("\r\n","<br>")+"""<br>"""+str(extradata)+"""<br><br>"""+str(editurl)+"""<br>"""+str(removeurl)
        data = data + """  ['"""+str(beschreibung)+"""', """+str(location)+""", """+str(count)+""", 'Wegpunkt """+str(id)+"""'],\n"""
        count = count + 1
    return data[:-2]

def printMarker():
    data = ""
    count = 1
    for i in itms:
        id = i[0]
        location = i[1]
        type = str(i[2])
        amount = i[3]
        chance = i[4]
        radius = i[5]
        if str(radius) == '0':
            radius = str(extra_distance_m)
        typename = type_dict[type]
        typename = typename.split(",")[0]
        emoji = emojidict[str(type)]
        deleteurl = '<a href="map.cgi?action=deleteItem&id='+str(id)+'">entfernen<a/>'
        plusurl = '<a href="map.cgi?action=plusItem&id='+str(id)+'">+1<a/>'
        minusurl = '<a href="map.cgi?action=minusItem&id='+str(id)+'">-1<a/>'
        beschreibung = str(typename)+"""<br>Anzahl: """+str(amount)+"""<br>Chance: """+str(chance)+"""%<br>"""+str(plusurl)+""" """+str(minusurl)+"""<br>"""+str(deleteurl)+"""<br>"""
        data = data + """  ['"""+str(beschreibung)+"""', """+str(location)+""", """+str(count)+""", '/img/emoji/"""+str(type)+""".png', '"""+str(typename)+"""', '"""+str(radius)+"""'],\n"""
        count = count + 1
    return data[:-2]














print r"""
<html>
<head>
  <meta http-equiv="content-type" content="text/html; charset=UTF-8">
  
    <link rel="icon" sizes="512x512" href="/img/favicon.png">
    <link rel="apple-touch-icon" href="/img/favicon.png">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">

  <meta name="robots" content="noindex, nofollow">
  <meta name="googlebot" content="noindex, nofollow">
  <meta name="viewport" content="width=device-width, initial-scale=1">
      <script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?v=3.exp&amp;libraries=geometry&amp;key="""+str(gmaps_key)+"""&amp;libraries=places,geometry"></script>
  <style type="text/css">
    html, body {
  height: 100%;
  margin: 0;
  padding: 0;
  display:block;
  overflow:auto;
}
#map-canvas{
  height: 80%;
  width: 100%;
}

* {font-family:"Courier New", Courier, monospace}
</style>


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

  <title>Map</title>

<script type="text/javascript"> 
function openwindow(url){
      NewWindow=window.open(url,'newWin','width=400,height=600,left=20,top=20,toolbar=No,location=No,scrollbars=no,status=No,resizable=no,fullscreen=No');  NewWindow.focus(); void(0);  }
</script>
  
<style type="text/css">.gm-style {
        font: 400 11px Roboto, Arial, sans-serif;
        text-decoration: none;
      }
      .gm-style img { max-width: none; }</style>
      </head>


<body>

<div style="padding: 6px 12px; border: 1px solid #ccc; overflow: hidden; margin: 5px; height: 85px">
    <div id="header" style="padding-left: 0px; padding-top: 0px; padding-bottom: 0px; display: table">
    <div style="float: left"><h3 style="margin: 0px; margin-bottom: 2px"><a href="index.cgi">Home</a></h3></div>"""
print "<div style='margin: -3px; margin-left: 50px; width: 400px'>"+action_message+"</div>"
print """
    </div>
    <div id="header" style="">


    <div style='float: left'>


<div style='margin: 5px;'>
<form action="map.cgi" method="post">

<input style="border: 1px solid #ccc; display:table-cell; vertical-align:middle;" type="text" name="lat" id="lat2" size="9" readonly>
<input style="border: 1px solid #ccc; display:table-cell; vertical-align:middle;" type="text" name="lng" id="lng2" size="9" readonly>

"""
typeDropDown()
AmounttypeDropDown()
print """
<button type="submit" name="action" value="addItem" style="display:table-cell; vertical-align:middle;">Item hinzufügen</button>
</form>
</div>

    <div style='margin: 5px;'>
    <form action="map.cgi" method="post">

    <input style="border: 1px solid #ccc;" type="text" name="lat" id="lat" size="9" readonly>
    <input style="border: 1px solid #ccc;" type="text" name="lng" id="lng" size="9" readonly>


    <button type="submit" name="action" value="addWaypoint">Wegpunkt hinzufügen</button>
    </form>
    </div>

</div>
    </div>

</div>
<div id="map-canvas" style="clear:both;"></div>

<script type="text/javascript">

var map,
    marker = null;

function initialize() {
  var mapOptions = {
    zoom: """+str(zoom_level)+""",
    center: new google.maps.LatLng("""+str(zoom_koordinaten)+"""),
    mapTypeId: google.maps.MapTypeId.HYBRID
  };

  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

  google.maps.event.addListener(map, 'click', function(event) {
      if (marker==null) {
         marker = new google.maps.Marker({
           position : event.latLng,
           map: map
         });          
      } else {
          marker.setPosition(event.latLng);
      }      
      document.getElementById('lat').value = event.latLng.lat();
      document.getElementById('lng').value = event.latLng.lng();

      document.getElementById('lat2').value = event.latLng.lat();
      document.getElementById('lng2').value = event.latLng.lng();
  });

  setMarkers(map);
  setWaypointMarkers(map);
  addYourLocationButton(map);


}
  var samitems = [
"""+str(printMarker())+"""
];

      var samwaypoints = [
"""+str(printWayPointMarker())+"""
    ];
google.maps.event.addDomListener(window, 'load', initialize);

function setMarkers(map) {
  // Adds markers to the map.

  // Marker sizes are expressed as a Size of X,Y where the origin of the image
  // (0,0) is located in the top left of the image.

  // Origins, anchor positions and coordinates of the marker increase in the X
  // direction to the right and in the Y direction down.


  // Shapes define the clickable region of the icon. The type defines an HTML
  // <area> element 'poly' which traces out a polygon as a series of X,Y points.
  // The final coordinate closes the poly by connecting to the first coordinate.
  var shape = {
    coords: [0, 0, 0, 32, 32, 32, 32, 0],
    type: 'poly'
  };
  for (var i = 0; i < samitems.length; i++) {
    var theitem = samitems[i];
    var contentString = samitems[i][0] + '';
    var marker = new google.maps.Marker({
      position: {lat: theitem[1], lng: theitem[2]},
      center: {lat: theitem[1], lng: theitem[2]},
      map: map,
      icon: { url: theitem[4], size: new google.maps.Size(16, 16), origin: new google.maps.Point(0, 0), anchor: new google.maps.Point(8, 8) },
      shape: shape,
      title: theitem[5],
      zIndex: theitem[3],
      contentString: contentString
    });
    var itemCircle = new google.maps.Circle({
        strokeColor: '#0000FF',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#0000FF',
        fillOpacity: 0.35,
        map: map,
        center: {lat: theitem[1], lng: theitem[2]},
        radius: parseInt(theitem[6]) / 2
      });

          var infowindow = new google.maps.InfoWindow({});

          marker.addListener('click', function() {
          infowindow.setContent(this.contentString);
          infowindow.open(map, this);
          map.setCenter(this.getPosition());
     });
  }


};





function setWaypointMarkers(map) {
  // Adds markers to the map.

  // Marker sizes are expressed as a Size of X,Y where the origin of the image
  // (0,0) is located in the top left of the image.

  // Origins, anchor positions and coordinates of the marker increase in the X
  // direction to the right and in the Y direction down.

    var image = {
    url: '/img/emoji/waypoint.png',
    // This marker is 20 pixels wide by 32 pixels high.
    size: new google.maps.Size(16, 16),
    // The origin for this image is (0, 0).
    origin: new google.maps.Point(0, 0),
    // The anchor for this image is the base of the flagpole at (8, 8).
    anchor: new google.maps.Point(8, 8)
  };

  // Shapes define the clickable region of the icon. The type defines an HTML
  // <area> element 'poly' which traces out a polygon as a series of X,Y points.
  // The final coordinate closes the poly by connecting to the first coordinate.
  var shape = {
    coords: [0, 0, 0, 32, 32, 32, 32, 0],
    type: 'poly'
  };
  for (var i = 0; i < samwaypoints.length; i++) {
    var theitem = samwaypoints[i];
    var contentString = samwaypoints[i][0] + '';
    var marker = new google.maps.Marker({
      position: {lat: theitem[1], lng: theitem[2]},
      center: {lat: theitem[1], lng: theitem[2]},
      map: map,
      icon: image,
      shape: shape,
      title: theitem[4],
      zIndex: theitem[3],
      contentString: contentString
    });

    var waypointCircle = new google.maps.Circle({
        strokeColor: '#FF0000',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#FF0000',
        fillOpacity: 0.35,
        map: map,
        center: {lat: theitem[1], lng: theitem[2]},
        radius: 10
      });

          var infowindow = new google.maps.InfoWindow({});

          marker.addListener('click', function() {
          infowindow.setContent(this.contentString);
          infowindow.open(map, this);
          map.setCenter(this.getPosition());
     });
  }
};





  function getLocation(map) {

        // Try HTML5 geolocation.
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };

            map.setCenter(pos);
          }, function() {
            handleLocationError(true, infoWindow, map.getCenter());
          });
        } else {
          // Browser doesn't support Geolocation
          handleLocationError(false, infoWindow, map.getCenter());
        }
      }


function addYourLocationButton(map) 
{
    var controlDiv = document.createElement('div');

    var firstChild = document.createElement('button');
    firstChild.style.backgroundColor = '#fff';
    firstChild.style.border = 'none';
    firstChild.style.outline = 'none';
    firstChild.style.width = '28px';
    firstChild.style.height = '28px';
    firstChild.style.borderRadius = '2px';
    firstChild.style.boxShadow = '0 1px 4px rgba(0,0,0,0.3)';
    firstChild.style.cursor = 'pointer';
    firstChild.style.marginRight = '10px';
    firstChild.style.padding = '0px';
    firstChild.title = 'Your Location';
    controlDiv.appendChild(firstChild);

    var secondChild = document.createElement('div');
    secondChild.style.margin = '5px';
    secondChild.style.width = '18px';
    secondChild.style.height = '18px';
    secondChild.style.backgroundImage = 'url(https://maps.gstatic.com/tactile/mylocation/mylocation-sprite-1x.png)';
    secondChild.style.backgroundSize = '180px 18px';
    secondChild.style.backgroundPosition = '0px 0px';
    secondChild.style.backgroundRepeat = 'no-repeat';
    secondChild.id = 'you_location_img';
    firstChild.appendChild(secondChild);


    firstChild.addEventListener('click', function() {
        var imgX = '0';
        if(navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                var latlng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
                map.setCenter(latlng);
            });
        }
    });

    controlDiv.index = 1;
    map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(controlDiv);
}


</script>
</div>


<script>
function getClientHeight() {
    var myheight;
    mywidth = document.documentElement.clientHeight;
    var cols = document.getElementById('map-canvas');
    var value = String(mywidth)
    var newvalue = (parseInt(value.replace(/px/,""))-109)+"px"
    cols.style.height = newvalue;
};

</script>
<script>
getClientHeight();
</script>

"""
