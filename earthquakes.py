#earthquakes.py

##reported Earthquake Magnitude in New ealand
##http://api.geonet.org.nz/intensity?type=measured


#import the modules
import json, os, string, urllib, getpass, urllib2
from ntlm import HTTPNtlmAuthHandler

#todo: set Security
def setSecurity (url, username, password):    
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, url, username, password)
    auth_NTLM = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(passman)
    opener = urllib2.build_opener(auth_NTLM)
    urllib2.install_opener(opener)


#START HERE
print "***\nEarthquakes Area of interest\n***"

###user credentials
##domain = 'TRANSPORT\\'
##username = domain + getpass.getuser()
##password = getpass.getpass(prompt = 'Enter password for ' + username + ':')
##
##print username
##print password

#parameters
url = "http://api.geonet.org.nz/intensity?type=measured"
##setSecurity (url, username, password)
fs=r"d:\tmp\earthquakes.json"
earthquakes="d:\\tmp\\earthquakes.csv"
f = open(earthquakes, 'w')
f.write("Longitude,Latitude,Magnitude\n")

#json_data = open(url).read()
#json_data = urllib.urlopen(url)
responses = json.loads(open(fs).read())

n = 0

#0 - type
#1 - features
for response in responses["features"]:

    #coordinates
    longitude = response["geometry"]["coordinates"][0]
    latitude = response["geometry"]["coordinates"][1]      

    #get Magnitude
    MMI = response["properties"]["mmi"]            

    f.write(str(longitude) + "," + str(latitude) + "," + str(MMI) +  "\n")
    n += 1


##f.close()

print n

#completed
print "\ncompleted"
