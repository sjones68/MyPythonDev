#sjParseJson.py

#from http://www.plugshare.com/

#import Modules
import json, string, os, codecs, sys

#banner

print "***\nWORKING WITH PLUGSHARE\nhttp://www.plugshare.com/\n\nSusan Jones\n19 July 2016\n"

print "json to CSV Parsing\n***"

#todo: hardcode the parameters
n = 0
jsonFile = r'd:\Tmp\worksite.json'

##pType = raw_input("R = Residential, C = Commercial?")
##print pType

#todo: Parse the json
json_data = open(jsonFile).read()
responses = json.loads(json_data)


n = 0
for response in responses:
    n += 1
print responses['data'] ##data , links
print n
    

###todo: loop json Response
###if C
##if pType == 'C':
##    #todo: open file for reading
##    csvFile = r'd:\Tmp\all.csv'
##    fs = codecs.open(csvFile, mode = 'w', encoding = 'utf8')
##    #todo: write Header
##    fs.write("rowNumber,name,stationsId,itype,longitude,latitude\n")
##    for response in responses:
##        #todo: fetch the attributes      
##        stationsId = response['stations'][0]['id']
##        longitude = response['longitude']
##        latitude = response['latitude']
##        name = response['name']
##        name = "\"" + name + "\""
##        name = name.encode('ascii', 'replace')
##        itype = response['icon_type']
##        if name == "\"\"":
##            name = "n/a"
##        n += 1
##        toWrite = str(n) + "," + name + "," + str(stationsId) + "," + itype + "," + str(longitude) + "," + str(latitude) + "\n"
##        fs.write(toWrite)
##    #todo: messaging
##    print "\nlook at " + csvFile
##    print str(n) + " records"
##
###if R    
##else:
##    #todo: open file for reading
##    csvFile = r'd:\Tmp\allResidential.csv'
##    fs = codecs.open(csvFile, mode = 'w', encoding = 'utf8')
##    #todo: write Header
##    fs.write("rowNumber,name,stationsId,itype,longitude,latitude\n")
##    for response in responses:
##        #todo: fetch the attributes      
##        stationsId = response['stations'][0]['id']
##        longitude = response['longitude']
##        latitude = response['latitude']
##        name = response['name']
##        name = "\"" + name + "\""
##        name = name.encode('ascii', 'replace')
##        itype = response['icon_type']
##        if name == "\"\"":
##            name = "n/a"
##        n += 1
##        toWrite = str(n) + "," + name + "," + str(stationsId) + "," + itype + "," + str(longitude) + "," + str(latitude) + "\n"
##        fs.write(toWrite)
##    #todo: messaging
##    print "\nlook at " + csvFile
##    print str(n) + " records"
        

#todo: file and object management
del responses
##fs.close()



#completed
print "\ncompleted, because Susan is very cool."
