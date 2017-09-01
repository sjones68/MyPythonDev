#sjSummariseStations.py

#Susan Jones
#29th January 2015

#import Modules
import arcpy, string, datetime

print "***\nSummarise Station Data\n***"

#todo Parametes

lstFC = ["HOP_PaperTicket", "HOP_TagOn"]


arcpy.env.workspace = r"D:\TMP\HOP_Activity_2013_2014.gdb"
arcpy.env.overwriteOutput = 1

#todo: create featureclass and fields
print "\ncreating HOP Transactions"
arcpy.CreateTable_management(arcpy.env.workspace, "HOP_Transactions")
print "\nadding Fields"
print "station_name..."
arcpy.AddField_management(in_table = "HOP_Transactions", field_name = "Station_Name", field_type = "TEXT", field_length = 100)
print "station_type..."
arcpy.AddField_management(in_table = "HOP_Transactions", field_name = "Station_Type", field_type = "TEXT", field_length = 10)
print "Av_Daily_TagOn..."
arcpy.AddField_management(in_table = "HOP_Transactions", field_name = "Av_Daily_TagOn", field_type = "DOUBLE")
print "Av_Daily_Paper..."
arcpy.AddField_management(in_table = "HOP_Transactions", field_name = "Av_Daily_Paper", field_type = "DOUBLE")
print "Av_Daily_Total..."
arcpy.AddField_management(in_table = "HOP_Transactions", field_name = "Av_Daily_Total", field_type = "DOUBLE")
print "Av_Daily_Total..."
arcpy.AddField_management(in_table = "HOP_Transactions", field_name = "GPSCoordinateLongitude", field_type = "DOUBLE")
print "Av_Daily_Total..."
arcpy.AddField_management(in_table = "HOP_Transactions", field_name = "GPSCoordinateLatitude", field_type = "DOUBLE")
print "adding Station_Name Index..."
arcpy.AddIndex_management(in_table = "HOP_Transactions", fields = ["Station_Name"], index_name = "StationNameIdx")

#todo: make arcpy.da.InsertCursor
print "\nmake arcpy.da.InsertCursor"
iFields = ["Station_Name", "Station_Type", "GPSCoordinateLongitude", "GPSCoordinateLatitude", "Av_Daily_TagOn", "Av_Daily_Paper", "Av_Daily_Total"]
irecs = arcpy.da.InsertCursor(in_table = "HOP_Transactions", field_names = iFields)

#todo: use arcpy.da.InsertCursor
print "\nprocess HOP_TagOn"
lstStationName = []
recs = []
fields = ["Station_Name", "Station_Type", "GPSCoordinateLongitude", "GPSCoordinateLatitude", "Av_Daily__TagOn"]
#lstFC[1] HOP_TagOn
srecs = arcpy.da.SearchCursor(in_table = lstFC[1], field_names = fields)
for srec in srecs:
    if srec[0] not in lstStationName:
        lstStationName.append(srec[0])
        rec = [srec[0], srec[1], srec[2], srec[3], srec[4], 0, 0]
        recs.append(rec)

#lstFC[0] HOP_PaperTicket
print "\nprocess HOP_PaperTicket"
ptLst = [] #paper tickets List
urecs = [] #to
srecs = arcpy.da.SearchCursor(in_table = lstFC[0], field_names = fields)
for srec in srecs:
    if srec[0] not in lstStationName: #not there
        lstStationName.append(srec[0])
        rec = [srec[0], srec[1], srec[2], srec[3], 0, srec[4], 0]
        urecs.append(rec)
    #if paper tickets > 0
    if srec[4] > 0:
        ptLst.append([srec[0], srec[4]])

#todo: insert rows 
for rc in recs: irecs.insertRow(rc)
for rc in urecs: irecs.insertRow(rc)
del irecs
del urecs

print len(ptLst)

#todo: update Paper Tickets
n = 0 
print "\nUpdate Paper Tickets"
start = datetime.datetime.now()
iFields = ["Station_Name", "Av_Daily_TagOn", "Av_Daily_Paper", "Av_Daily_Total"]
for pt in ptLst:
    if "\'" in pt[0]:
        station = string.replace(pt[0], "\'", "\'\'")
        sql = "Station_Name = \'" + station + "\'"
    else: sql = "Station_Name = \'" + pt[0] + "\'"
    urecs = arcpy.UpdateCursor(dataset = "HOP_Transactions", where_clause = sql)
    urec = urecs.next()
    while urec:
        total = urec.Av_Daily_TagOn + pt[1]
        urec.Av_Daily_Paper = pt[1]
        if total > 0:
            urec.Av_Daily_Total = urec.Av_Daily_TagOn / total
            urecs.updateRow(urec)
        n += 1
        if n % 100 == 0:
            print str(n) + " processed\t" + str(datetime.datetime.now() - start)
            start = datetime.datetime.now()
        urec = urecs.next()
print str(n) + " processed\t" + str(datetime.datetime.now() - start)
start = datetime.datetime.now()

#completed
print "completed"
