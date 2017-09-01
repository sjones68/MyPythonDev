#sjExtractCRMToCSV.py

#import Modules
import arcpy, os, string, datetime

startTime = datetime.datetime.now()

#banner
print "***\nExtract CRM to CSV\n***"

#fetch Parameters
print "\n1. fetch Parameters"
crmFile = "d:\\TMP\\CRMExtract.csv"
fc = "\\\\atalgisau01\\admin\\Maintenance\\connections\\dba@GIS@atalgissdbu01.sde\\GIS.GISADMIN.CR_CRMRapidResponseComplaint_DV"
arcpy.MakeFeatureLayer_management(in_features = fc, out_layer = "CRM")

print arcpy.GetCount_management("CRM")

fieldList = ["TICKETNUMBER", "RECEIVED", "MONTH", "OWNINGTEAM", "STATE", "DESCRIPTION", "LATITUDE", "LONGITUDE"] 
print len(fieldList)

#extract The Rows
print "\n2. extract CRM"
crmSet = []
rows = arcpy.da.SearchCursor(in_table = "CRM", field_names = fieldList)
for row in rows:
    crmSet.append([row[0],str(row[1]),str(row[2]),row[3],row[4],row[5],row[6],row[7]])
del rows


print crmSet[500][1]

#write to File
if os.path.exists(crmFile):
    os.remove(crmFile)
fs = open(name = crmFile, mode = "w")
fs.write("TicketNumber,Receiver,Month,OwningTeam,State,Latitude,Longitude\n")
for crm in crmSet:
    description = "\"" + str(row[5]) + "\""
    fs.write(str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])+","+str(row[4])+","+str(row[7])+","+str(row[6])+"\n")
fs.close

#cleanup
print "\ncleanUp"

#complete
print "\ncomplete"

#elapsed
endTime = datetime.datetime.now()
print "\nelapsed " + str(endTime - startTime)
