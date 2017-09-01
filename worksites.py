#worksites.py

#purpose extracts worksite json into gis format

#import modukes
import json, arcpy, datetime, dateutil.parser, string, urllib, getpass, urllib2
from ntlm import HTTPNtlmAuthHandler

start = datetime.datetime.now()

#make the pointArray
def makePolygon(pointArray):
    n = 0
    pts = arcpy.Array()
    while n < len(pointArray):
        longitude = pointArray[n]
        latitude = pointArray[n + 1]
        pt = arcpy.Point(X = longitude, Y = latitude)
        pts.add(pt)
        n += 2
    pts.add(pts[0])
    poly = arcpy.Polygon(pts)
    if poly.area == 0:
        polyline = arcpy.Polyline(pts)
        poly = polyline.buffer(0.0015)

    return poly


#set Security
def setSecurity (url, username, password):
    print 'test'
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, url, username, password)
    auth_NTLM = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(passman)
    opener = urllib2.build_opener(auth_NTLM)
    urllib2.install_opener(opener)
    print 'test2'
    
        

#parameters
worksiteUrl = r'D:/TMP/worksite.json'
fc = 'D:/TMP/Geoprocessing.gdb/worksites'

#get Credentials
domain = 'TRANSPORT\\'
username = domain + getpass.getuser()
print username
password = getpass.getpass(prompt = 'Enter password for ' + username + ':')
print password
#banner
print('***\nExport worksites.json\n')


#cycle Companies JSON
companiesUrl = "https://uat1.myworksites.co.nz/api/worksites?"
setSecurity (companiesUrl, username, password)
values = {'access_token' : 'smpOkKrD2ud8Zy4zkrRmkcoGkUa8UZ8mfK2aNxoFcM6aFJahZew3K2HJsmFG6wAu'}
data = urllib.urlencode(values)
f = urllib.request.urlopen(companiesUrl, data).read()
##responses = json.loads(f)
##print len(responses)


###deleteFeatures
##arcpy.DeleteFeatures_management(in_features = fc)
##
##
###cycle GeoJSON file
##with open(worksiteUrl) as jsonData:
##    responses = json.load(jsonData)
##
###process Responses
##print('\nProcessing GeoJSON Features')
##fields = ["Id","Name", "Address", "CompanyID", "StartDate", "EndDate", "WorksiteType", "WorksiteCode", "Shape"]
##recs = arcpy.InsertCursor(dataset = fc)
##rows = []
##maxL = 0
##n = 1
##for response in responses["data"]:
##    #extract GeoJSON
##    row = []
##    row.append(string.replace(response["attributes"]["reference"], "#", "")) #0
##    row.append(response["attributes"]["name"]) #1
##    row.append(response["attributes"]["address"]) #2
##    row.append(response["attributes"]["company"]["id"]) #3
##    row.append(response["attributes"]["startDate"]) #4
##    row.append(response["attributes"]["endDate"]) #5
##    row.append(response["attributes"]["worksiteType"]) #6
##    row.append(response["attributes"]["worksiteCode"]) #7
##    row.append(response["attributes"]["location"]["coordinates"]) #8
##    rows.append(tuple(row))
##    #populate New Row
##    polygon = makePolygon(str(response["attributes"]["location"]["coordinates"]).replace("[","").replace("]","").replace(" ","").split(","))
##    rec = recs.newRow()
####    rec.id = int(row[0])
##    rec.name = row[1]
##    rec.address = row[2]
##    rec.companyid = row[3]
##    rec.startdate = row[4]
##    rec.enddate = row[5]
##    rec.worksitetype = row[6]
##    rec.worksitecode = row[7]
##    rec.setValue( "Shape", polygon)
##    recs.insertRow(rec)
##    n += 1
##
##
###deal With Dates
####print(rows[0][3])
####print(maxL)
##
###cleanUp
##del recs
##del responses

#completes
print('\ncompleted')

end = datetime.datetime.now()

print('\nelapsed: ' + str(end - start))
