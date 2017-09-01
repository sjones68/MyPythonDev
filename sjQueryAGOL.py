#sjQueryAGOL.py

#Todo: import Modules
import json, string, datetime, sys
from urlparse import urlparse, urlunparse
from ntlm import HTTPNtlmAuthHandler
import urllib, urllib2, sys, os, time, unicodedata, codecs, getpass, httplib


#set Security
def setSecurity (url, username, password):    
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, url, username, password)
    auth_NTLM = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(passman)
    opener = urllib2.build_opener(auth_NTLM)
    urllib2.install_opener(opener)


#generarate AGOL Content
def getAGOLContent(url):
    #here
    setSecurity (url, "sjonesAT", "cha1tdb123")
    parameters = urllib.urlencode({'f': 'pjson'}) #parse json markup
    response = urllib2.urlopen(url, parameters).read()
    


#banner
print("\n***\nget Features from AGOL\n****")

#set Parameters
username = r"TRANSPORT\SusanJon1"
password = "Cha1tdb1274"


print("set Proxy")
url = "https://atalgispsu01.aucklandtransport.govt.nz/arcgis/sharing/rest/generateToken?"
url = "https://services2.arcgis.com/JkPEgZJGxhSjYOo0/arcgis/rest/services?"
setSecurity (url, username, password)


print("proxy Set")

parameters = urllib.urlencode({'username' : None,
                               'password' : None,
                               'client' : 'referer',
                               'referer': url,
                               'expiration': 60, #minutes
                               'f' : 'pjson'})

response = urllib2.urlopen(url,parameters).read()

print response

##setSecurity ( "http://www.google.com", "TRANSPORT\\SusanJon1", "Cha1tdb1274")



agolUrl = "https://services2.arcgis.com/"
contentUrl = agolUrl + "JkPEgZJGxhSjYOo0/arcgis/rest/services?"



##print("\n" + contentUrl)
##getAGOLContent (contentUrl)


#complete
print("\ncompleted")
