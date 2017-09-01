#sjDeliveCAFSComparisons.py

#purse Parse XML objects into KML

#Susan Jones
#15 

#import Modules
import xml, string, os, arcpy, datetime, shutil
from xml.dom.minidom import parse

#convertAngular
def convertToAngular(dd):
    degrees = dd / 100
    minutes = ((degrees - int(degrees)) * 100) / 60
    seconds = (minutes - int(minutes)) 
    coord = int(degrees) + minutes
    return coord

#start
start = datetime.datetime.now()

#todo: Banner and Parameters
print '***\nEMU File Conversion\n\nSusan Jones\n8 January 2015\n***\n'
xmlParse = r'd:\tmp\XMlCAFFeed17Dec2014.xml'
csvFile = r'd:\tmp\tmpEMU.csv'
kmlFile = r'd:\tmp\tmpEMU.kmz'
wayPointFile = r'D:\TMP\ATwaypointsCW.xlsx' ##\ATwaypointsCW''
scratchGDB = r'D:\TMP\ScratchGDB.gdb'
outFolder = r'd:\tmp'
outputLayerfile = r'D:\TMP\CAFS_GIS.lyr'
arcpy.env.overwriteOutput = 1
arcpy.env.workspace = outFolder
sr = arcpy.SpatialReference(4326)

#todo: Make CAFS, EMU and WayPoints Featureclass
print "Make CAFS, EMU and WayPoints Featureclass"
fc = r"D:\TMP\ScratchGDB.gdb\TrainSignals" ##scratchGDB + os.path.sep + "KMZ"
arcpy.CreateFeatureclass_management(out_path = scratchGDB, out_name = "TrainSignals", geometry_type = "POINT", spatial_reference = sr)
arcpy.AddField_management(in_table = fc, field_name = "DateTime", field_type = "DATE", field_length = 30)
arcpy.AddField_management(in_table = fc, field_name = "VehicleID", field_type = "TEXT", field_length = 30)
arcpy.AddField_management(in_table = fc, field_name = "FeedType", field_type = "TEXT", field_length = 10)
arcpy.AddField_management(in_table = fc, field_name = "Timestamp", field_type = "TEXT", field_length = 30)
arcpy.AddField_management(in_table = fc, field_name = "Longitude", field_type = "DOUBLE")
arcpy.AddField_management(in_table = fc, field_name = "Latitude", field_type = "DOUBLE")
arcpy.AddIndex_management (in_table = fc, fields = "VehicleID", index_name = "VehicleIDIdx")
arcpy.AddIndex_management (in_table = fc, fields = "FeedType", index_name = "FeedTypeIdx")

#todo:Process Waypoint File
print "updates Waypoint File"
tbl = scratchGDB + os.path.sep + "WayPoints"
if arcpy.Exists(tbl):
    arcpy.Delete_management(tbl)
arcpy.ExcelToTable_conversion (Input_Excel_File = wayPointFile, Output_Table = tbl, Sheet = "ATwaypointsCW")
recs = arcpy.da.SearchCursor(in_table = tbl, field_names = ["Waypoint_name", "Longitude", "Latitude"])
rows = []
for rec in recs:
    longitude = convertToAngular(rec[1])
    latitude = convertToAngular(rec[2])
    pt = [longitude, latitude]
    row = [pt, "Waypoint"]
    rows.append(row)
del recs
print "insert Waypoints"
fldList = ["SHAPE@XY", "FeedType"]
irecs = arcpy.da.InsertCursor(in_table = fc, field_names = fldList)
for row in rows:
    irecs.insertRow(row)
del irecs


#todo: process CAFS Layer
print "\nProcess CAFS Layer"
fs = open(csvFile, "w")
fs.write("TimeStamp,VehicleId,Longitude,Latitude\n")
doc = parse(xmlParse)
recs = doc.getElementsByTagName('UpdateLocationRequest')
for rec in recs:
    #todo: extract attributes
    vehicleStatus = rec.getElementsByTagName("VehicleStatus")[0].childNodes[0].data
    vehicleId = rec.getElementsByTagName("VehicleId")[0].childNodes[0].data
    timeStamp = rec.getElementsByTagName("Timestamp")[0].childNodes[0].data
    longitude = rec.getElementsByTagName("Longitude")[0].childNodes[0].data
    latitude = rec.getElementsByTagName("Latitude")[0].childNodes[0].data
    fs.write(str(timeStamp) + "," + str(vehicleId) + "," + str(longitude) + "," + str(latitude) + "," + "\n")
fs.close()
datestamp = "17/12/2014"
arcpy.MakeTableView_management(in_table = csvFile, out_view = "EMU_VIEW")  
recs = arcpy.da.SearchCursor(in_table = "EMU_VIEW", field_names = ["VehicleId", "Timestamp", "Longitude", "Latitude"])
rows = []
for rec in recs:
    pt = [rec[2], rec[3]]
    #fix timestamp in CAFS
    timestamp = rec[1]
    timestamp = string.split(rec[1], "T")[1]
    timestamp = string.split(timestamp, ".")[0]
    timestamp = string.split(timestamp, "+")[0]
    timestamp = datestamp + " " + timestamp
    row = [pt, timestamp, rec[0], "CAFS", rec[1], rec[2], rec[3]]
    rows.append(row)
del recs
print "insert CAFS Data"
fldList = ["SHAPE@XY", "DateTime", "VehicleID", "FeedType", "Timestamp", "Longitude", "Latitude"]
irecs = arcpy.da.InsertCursor(in_table = fc, field_names = fldList)
for row in rows:
    irecs.insertRow(row)
del irecs

#todo: process EMU Layer
print "\nProcess EMU Layer"
csvFile = r'd:\tmp\AT_EMU.csv'
arcpy.MakeTableView_management(in_table = csvFile, out_view = "EMU_VIEW")  
recs = arcpy.da.SearchCursor(in_table = "EMU_VIEW", field_names = ["remotename", "datetime_nzdt", "longitude_wgs84", "latitude_wgs84"])
rows = []
for rec in recs:
    pt = [rec[2], rec[3]]
    row = [pt, rec[1], rec[0], "EMU", rec[1], rec[2], rec[3]]
    rows.append(row)
del recs
print "insert EMU Data"
fldList = ["SHAPE@XY", "DateTime", "VehicleID", "FeedType", "Timestamp", "Longitude", "Latitude"]
irecs = arcpy.da.InsertCursor(in_table = fc, field_names = fldList)
for row in rows:
    irecs.insertRow(row)
del irecs

#todo: loop through layers
lstVehicleID = []
recs = arcpy.da.SearchCursor(in_table = fc, field_names = ["VehicleID", "FeedType"])
for rec in recs:
    if not (rec[0] in lstVehicleID) and (str(rec[0]) <> "None"): lstVehicleID.append(rec[0])
del recs
outfc = r"D:\TMP\ScratchGDB.gdb\outKMZ"
#process Vehicle KML
for v in lstVehicleID:
    print "Processing: " + v
    #todo: waypoint
    sql = "VehicleId = \'" + v + "\'"
    print "\tcreating Selection For " + v
    outfc = scratchGDB + os.path.sep + v
    print outfc
    arcpy.Select_analysis(in_features = fc, out_feature_class = outfc, where_clause = sql)
    print "\tapplying Symbology"
    arcpy.MakeFeatureLayer_management(in_features = outfc, out_layer = str(v))
    arcpy.ApplySymbologyFromLayer_management(in_layer = str(v), in_symbology_layer = outputLayerfile)
    tmpLayer = outFolder + os.path.sep + str(v) + ".lyr"
    arcpy.SaveToLayerFile_management (in_layer = str(v), out_layer = tmpLayer)
#process Waypoints
print "Processing: Waypoints"
##kmlFile = pth + os.path.sep + "WayPoints.kmz"
#todo: waypoint
sql = "FeedType = \'Waypoint\'"
print sql
print "\tcreating Selection For Waypoint"
outfc = scratchGDB + os.path.sep + "WayPts"
arcpy.Select_analysis(in_features = fc, out_feature_class = outfc, where_clause = sql)
print "\tapplying Symbology"
arcpy.MakeFeatureLayer_management(in_features = outfc, out_layer = "WayPts")
arcpy.ApplySymbologyFromLayer_management(in_layer = "WayPts", in_symbology_layer = outputLayerfile)
tmpLayer = outFolder + os.path.sep + "Waypt.lyr"
arcpy.SaveToLayerFile_management (in_layer = "WayPts", out_layer = tmpLayer)
   

#todo: cleanup
print "\nCleanup"
del doc


#todo: Measure elapsed
end = datetime.datetime.now()
print "\nRunning time: " + str(end - start)

#all good 
print '\nCompleted'

