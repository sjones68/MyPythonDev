#useArcGISServer.py


#import Modules
import json, string, os
from urlparse import urlparse, urlunparse
from ntlm import HTTPNtlmAuthHandler

#import Modules
import urllib, urllib2, sys, os, time, unicodedata, codecs, getpass


#set Security
def setSecurity (url, username, password):    
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, url, username, password)
    auth_NTLM = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(passman)
    opener = urllib2.build_opener(auth_NTLM)
    urllib2.install_opener(opener)

#generate portal token
def generateTokenPortal(username, password, agsUrl, callEnd):
    url = portalUrl + callEnd
    parameters = urllib.urlencode({'username' : username,
                                   'password' : password,
                                   'client' : 'referer',
                                   'referer': agsUrl,
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



##todo: START HERE

#place a banner in the code
print '***\nManage ArcGIS Server Content\nSusan Jones\nAuckland Transport\n***\n'

#todo: set The Portal Connections
portalUrl = "https://atalgispsu01.aucklandtransport.govt.nz/arcgis/"
agsUrl = "https://atalgisau01.aucklandtransport.govt.nz/arcgis/rest/services/"
ending='?f=pjson'

print 'ArcGIS Server\t' + agsUrl + '\n'

#user credentials
domain = 'TRANSPORT\\'
username = domain + getpass.getuser()
password = getpass.getpass(prompt = 'Enter password for ' + username + ':')

#todo: generate Portal Token
setSecurity (portalUrl + 'sharing/rest/generateToken?', username, password)
token = generateTokenPortal(username, password, portalUrl, "sharing/rest/generateToken?")


#get Folders
setSecurity (agsUrl + ending, username, password)
url = agsUrl + '/rest/?'

#todo: get Arcgis Services
parameters = urllib.urlencode({ 'f' : 'pjson', 'token' : token })
response = urllib2.urlopen(agsUrl + ending, parameters).read()
jsonResponse = json.loads(response)


#todo: get The Services at the root level
n = 0

#todo: write to File
fs = open(r'\\atalgisau01\ADMIN\Portal User Content\UAT' + os.path.sep + 'ArcGISContent.csv', 'w+')
fs.write('Folder,ServiceType,ServiceName,ServiceURL\n')


f = 'root'
for sname in jsonResponse['services']:
    try:
        serviceUrl = agsUrl + sname['name'] + '/' + sname['type']
        fs.write(f + ',' + sname['type'] + ',' + sname['name'] + ',' + serviceUrl + '\n')
        n += 1
    
    except:
        print agsUrl + f + ending + '\tnot authorised'


#todo: process folders containing arcgis services
for f in jsonResponse['folders']:

    try:
        #todo: navigate the URL
        setSecurity (agsUrl + f + ending, username, password)
        parameters = urllib.urlencode({ 'f' : 'pjson', 'token' : token })
        folderResponse = urllib2.urlopen(agsUrl + f, parameters ).read()
        jsonFolder = json.loads(folderResponse)

        #todo: get Contents
        for sname in jsonFolder['services']:
            serviceUrl = agsUrl + sname['name'] + '/' + sname['type']
            fs.write(f + ',' + sname['type'] + ',' + sname['name'] + ',' + serviceUrl + '\n')
            n += 1

    except:
        status = 'next'
        

#todo: close the file
fs.close()

print '\n' + str(n) + '  arcgis services in ' + agsUrl

print '\ncompleted'
