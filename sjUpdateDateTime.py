#sjUpdateDateTime.py

#purpose: update data and time fields

#import modules
import arcpy, string, os, datetime

#startTime
startTime = datetime.datetime.now()

#banner
print '***\nUpdate data and time fields\n****'

#set Parameters
print '\nset Parameters'
fc = "D:\\TMP\\SCATS GPS Coordinate\\Demo\\output\\Scats_Demo_January2016.gdb\\Bus_Features"
arcpy.MakeFeatureLayer_management(in_features = fc, out_layer = "Bus")
##fields = arcpy.ListFields("Bus")
##for field in fields:
##    print field.name
fields = ["BusAttributes_Service_Date", "BusAttributes_Service_Start_Time__Hh24mm_", "DateTime"]

#prepare UpdateCursor
n = 0
print '\nprepare Update Cursor'
recs = arcpy.da.UpdateCursor(in_table = "Bus", field_names = fields)
for rec in recs:
    n += 1
    tmList = string.split(rec[1], ":") #time object -> H M S
    rec[2] = rec[0] + datetime.timedelta(hours = int(tmList[0]))
    recs.updateRow(rec)
##    if n % 1000 == 0: print str(n) + ' processed'
print str(n) + ' processed'
del recs

#clean Up
print '\nClean up'
arcpy.Delete_management(in_data = "Bus")

#complete
print '\nComplete'

#measure Elapsed Time
endTime = datetime.datetime.now()
print '\nElapsed time ' + str(endTime - startTime)
