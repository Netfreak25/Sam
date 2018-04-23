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

sam_host = str(getconfig('sam_host'))
sam_db = str(getconfig('sam_db'))
sam_db_user = str(getconfig('sam_db_user'))
sam_db_pw = str(getconfig('sam_db_pw'))

print "Content-Type: text/html; charset=UTF-8"     # HTML is following
print                               # blank line, end of headers


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
elif (str(action) == "deleteWaypoint"):
    removeWaypoint(html_id)


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
itms = get_waypoints()

try:
    val = itms[0][1].replace(" ","")
    zoom_koordinaten = str(val).strip()
except:
    pass

print zoom_koordinaten
print val
if (str(action) == "addWaypoint"):
    action_message = "Wegpunkt der Karte hinzugefügt!"

if (str(action) == "deleteWaypoint"):
    action_message = "Wegpunkt von der Karte gelöscht!"



def printMarker():
    data = ""
    count = 1
    for i in itms:
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


        removeurl = '<a href="waypoints.cgi?action=deleteWaypoint&id='+str(id)+'">entfernen<a/>'
        editurl = """<a href="website" onclick="openwindow(\\'waypoint.cgi?id="""+str(id)+"""\\'); return false;">editieren<a/>"""
        beschreibung = """Wegpunkt """+str(id)+""":<br><br>"""+str(text).replace("\r\n","<br>")+"""<br>"""+str(extradata)+"""<br><br>"""+str(editurl)+"""<br>"""+str(removeurl)
        data = data + """  ['"""+str(beschreibung)+"""', """+str(location)+""", """+str(count)+""", 'Wegpunkt """+str(id)+"""'],\n"""
        count = count + 1
    return data[:-2]

def waypointeditor():
    print """
    <html>
    <head>
    </head>
    <body>
    Wegpunkt editor ist noch nicht implementiert :(
    </body>
    </html>
    """

def waypointmap():
    print r"""
    <html>
    <head>

    <link rel="icon" sizes="512x512" href="/img/favicon.png">
    <link rel="apple-touch-icon" href="/img/favicon.png">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">

    
      <meta http-equiv="content-type" content="text/html; charset=UTF-8">
      <meta name="robots" content="noindex, nofollow">
      <meta name="googlebot" content="noindex, nofollow">
      <meta name="viewport" content="width=device-width, initial-scale=1">
          <script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?v=3.exp&&amp;libraries=geometry&&amp;key="""+str(gmaps_key)+"""&&amp;libraries=places,geometry"></script>
      <style type="text/css">
        html, body {
      height: 100%;
      margin: 0;
      padding: 0;
      display:block;
      overflow:auto;
    }
    #map-canvas{
      height: 100%;
      width: 100%;
    }
* {font-family:"Courier New", Courier, monospace}
      </style>
<script type="text/javascript"> 
function openwindow(url){
      NewWindow=window.open(url,'newWin','width=400,height=600,left=20,top=20,toolbar=No,location=No,scrollbars=no,status=No,resizable=no,fullscreen=No');  NewWindow.focus(); void(0);  }
</script>

      <title>Wegpunkt Editor</title>
    <style type="text/css">.gm-style {
            font: 400 11px Roboto, Arial, sans-serif;
            text-decoration: none;
          }
          .gm-style img { max-width: none; }</style>

          </head>

    <body>

<div style="padding: 6px 12px; border: 1px solid #ccc; overflow: hidden; margin: 5px; height: 82px">
    <div id="header" style="padding-left: 20px; padding-top: 2px; height: 50px; display: table">
    <div><h3><a href="index.cgi">Home</a></h3></div>"""
    print "<div style='margin-top: -10px;'>"+action_message+"</div>"
    print """
    </div>
    <div id="header" style="float: left; padding-left: 20px; height: 30px">
    

    <div style='float: left'>
    <form action="waypoints.cgi" method="post">

    <input style="border: 1px solid #ccc;" type="text" name="lat" id="lat" size="9" readonly>
    <input style="border: 1px solid #ccc;" type="text" name="lng" id="lng" size="9" readonly>

    """
    print """
    <button type="submit" name="action" value="addWaypoint">Wegpunkt hinzufügen</button>
    </div>


    </div>

</div>
    <div id="map-canvas" style="clear:both;"></div>

    <script type="text/javascript">

    var map,
        marker = null;

    function initialize() {
      var mapOptions = {
      zoom: """+zoom_level+""",
      center: new google.maps.LatLng("""+zoom_koordinaten+"""),
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
      });

      setMarkers(map);
      addYourLocationButton(map);



    }
      var samitems = [
"""+str(printMarker())+"""
    ];
    google.maps.event.addDomListener(window, 'load', initialize);

    function setMarkers(map) {
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
        // The anchor for this image is the base of the flagpole at (0, 32).
        anchor: new google.maps.Point(0, 16)
      };

      // Shapes define the clickable region of the icon. The type defines an HTML
      // <area> element 'poly' which traces out a polygon as a series of X,Y points.
      // The final coordinate closes the poly by connecting to the first coordinate.
      var shape = {
        coords: [1, 1, 1, 20, 18, 20, 18, 1],
        type: 'poly'
      };
      for (var i = 0; i < samitems.length; i++) {
        var theitem = samitems[i];
        var contentString = samitems[i][0] + '';
        var marker = new google.maps.Marker({
          position: {lat: theitem[1], lng: theitem[2]},
          map: map,
          icon: image,
          shape: shape,
          title: theitem[4],
          zIndex: theitem[3],
          contentString: contentString
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
    var newvalue = (parseInt(value.replace(/px/,""))-106)+"px"
    cols.style.height = newvalue;
};

</script>
<script>
getClientHeight();
</script>

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
    evt.currentTarget.className += " active";
}
</script>
    """

if (str(action) != "editWaypoint"):
    waypointmap()
else:
    waypointeditor()
