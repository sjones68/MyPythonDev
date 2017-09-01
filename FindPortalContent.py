#usePortalpy.py


#import Modules
import arcpy, json
from urlparse import urlparse, urlunparse
from ntlm import HTTPNtlmAuthHandler

import urllib, urllib2, sys, os, time, unicodedata, codecs, getpass

#generate portal token
def generateTokenPortal(username, password, portalUrl, callEnd):
    url = portalUrl + callEnd
    parameters = urllib.urlencode({'username' : username,
                                   'password' : password,
                                   'client' : 'referer',
                                   'referer': portalUrl,
                                   'expiration': 60, #minutes
                                   'f' : 'json'})
    response = urllib2.urlopen(url,parameters).read()
    try:
        jsonResponse = json.loads(response)
        if 'token' in jsonResponse:
            return jsonResponse['token']
        elif 'error' in jsonResponse:
            print jsonResponse['error']['message']
            for detail in jsonResponse['error']['details']:
                print detail
    except ValueError, e:
        print 'An unspecified error occurred.'
        print e


#set Security
def setSecurity (url, username, password):    
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, url, username, password)
    auth_NTLM = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(passman)
    opener = urllib2.build_opener(auth_NTLM)
    urllib2.install_opener(opener)


#generate Users
def generateUsers(folder):
    start = 1
    f = 1
    num = 100
    query = "a*"
    url = portalUrl + 'sharing/rest/community/users?'
    setSecurity (url, username, password)

    #todo: get Total Content
    parameters = urllib.urlencode({ 'q' : query, 'f' : 'json', 'start' : start, 'num' : num}) #remember to generate json content
    response = urllib2.urlopen(url, parameters ).read()
    jsonResponse = json.loads(response)
    total = jsonResponse['total']
    print str(total) + ' users'

    #todo: prepare file for writing
    fs = open(folder + os.path.sep + "PortalUsers.csv", "w+")
    fs.write("Username,Full Name,Created,Modified\n")

    while f < total + 1:
        parameters = urllib.urlencode({ 'q' : query, 'f' : 'json', 'start' : start, 'num' : num}) #remember to generate json content
        response = urllib2.urlopen(url, parameters ).read()
        jsonResponse = json.loads(response)
        #loop 
        for i in jsonResponse['results']:
            created = time.strftime('%d/%m/%Y', time.gmtime(i['created']/1000))
            modified = time.strftime('%d/%m/%Y', time.gmtime(i['modified']/1000))
            fs.write(i['username'] + ',' + i['fullName'] + ',' + created + ',' + modified + '\n') #username,fullName,created          
            f+=1
        start += 100
    fs.close()


#generate Content
def generateContent(folder):
    start = 1
    f = 1
    num = 100
    query = "a*"
    url = portalUrl + 'sharing/rest/search?'
    setSecurity (url, username, password)

    #todo: get Total Content
    parameters = urllib.urlencode({ 'q' : query, 'f' : 'json', 'start' : start, 'num' : num}) #remember to generate json content
    response = urllib2.urlopen(url, parameters ).read()
    jsonResponse = json.loads(response)
    total = jsonResponse['total']
    print str(total) + ' content'

    #todo: prepare file for writing
    fs = open(folder + os.path.sep + "PortalContent.csv", "w+")
    fs.write("Owner,Title,Created,Modified,URL,NumViews\n")

    while f < total + 1: ##3518, 3257
        parameters = urllib.urlencode({ 'q' : query, 'f' : 'json', 'start' : start, 'num' : num}) #remember to generate json content
        response = urllib2.urlopen(url, parameters ).read()
        jsonResponse = json.loads(response)     
        #loop through the Results
        for i in jsonResponse['results']:
            created = time.strftime('%d/%m/%Y', time.gmtime(i['created']/1000))
            modified = time.strftime('%d/%m/%Y', time.gmtime(i['modified']/1000))
            ##print to file
            serviceInfo = (i['owner'] + ',\"' + i['title'] + '\",' + created + ',' + modified + ',' + str(i['url']) + ',' + str(i['numViews']) + '\n' )
            try:
               fs.write(serviceInfo)
            except:
                status = 'next'
            f+=1
        start += 100
    fs.close()



##todo: START HERE

#todo: set The Parameters
proxies = {'http' : 'http://at-proxy.aucklandtransport.govt.nz:8080'}

#todo: set The Portal Connections
portalUrl = "https://atalgispsu01.aucklandtransport.govt.nz/arcgis/"
ending='sharing/rest/generateToken?'

domain = 'TRANSPORT\\'
username = domain + getpass.getuser()
password = getpass.getpass(prompt = 'Enter password for ' + username + ':')

folder = r'D:\TEMP\pythontemp'


#todo: generate Token
#print 'generate Token...'
##setSecurity (portalUrl + 'sharing/rest/generateToken?', username, password)
##token = generateTokenPortal(username, password, portalUrl, 'sharing/rest/generateToken?')
#print token + '\n'


#generateUsers
print "todo: Generate Users"
generateUsers(folder)

#todo: generate Content
print "todo: Generate Content"
generateContent(folder)



print "completed"
