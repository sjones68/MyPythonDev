#sjParseXML.py

#purse Parse XML objects into KML


#import Modules
import xml, string, os, arcpy, datetime, shutil
from xml.dom.minidom import parse

#start
start = datetime.datetime.now()

#todo: Banner and Parameters
print '***\nEMU File Conversion\n\nSusan Jones\n8 January 2015\n***\n'
xmlParse = r'd:\tmp\XMlCAFFeed17Dec2014.xml'
csvFile = r'd:\tmp\tmpEMU.csv'
kmlFile = r'd:\tmp\tmpEMU.kmz'
kmlMxd = r'd:\tmp\kml.mxd'
outFolder = r'd:\tmp'
outputShapefile = r'd:\tmp\EMU.shp'
outputLayerfile = r'd:\tmp\EMU.lyr'
arcpy.env.overwriteOutput = 1
arcpy.env.workspace = outFolder

#todo: file Maintenance
print "File maintenance"
if os.path.exists(kmlFile):
    os.remove(kmlFile)
if os.path.exists(csvFile):
    os.remove(csvFile)
fs = open(csvFile, "w")
fs.write("TimeStamp,VehicleId,Longitude,Latitude\n")

#todo: parse XML
doc = parse(xmlParse)
recs = doc.getElementsByTagName('UpdateLocationRequest')

#todo: cycle Through Records
print "Parsing EMU File"
for rec in recs:
    #todo: extract attributes
    vehicleStatus = rec.getElementsByTagName("VehicleStatus")[0].childNodes[0].data
    vehicleId = rec.getElementsByTagName("VehicleId")[0].childNodes[0].data
    timeStamp = rec.getElementsByTagName("Timestamp")[0].childNodes[0].data
    longitude = rec.getElementsByTagName("Longitude")[0].childNodes[0].data
    latitude = rec.getElementsByTagName("Latitude")[0].childNodes[0].data
    fs.write(str(timeStamp) + "," + str(vehicleId) + "," + str(longitude) + "," + str(latitude) + "," + "\n")
fs.close()

#todo: make fieldInfo
print "\nMake FieldInfo for EMU"
fi = arcpy.FieldInfo()
fi.addField("Longitude", "Longitude", "VISIBLE", "NONE")
fi.addField("Latitude", "Latitude", "VISIBLE", "NONE")
fi.addField("VehicleId", "VehicleId", "VISIBLE", "NONE")
fi.addField("Timestamp", "Timestamp", "VISIBLE", "NONE")

print fi.count
print fi.getFieldName(0) ##longitude

#todo: make XY Event Layer
print "\nMake EMU event Layer"
arcpy.MakeTableView_management(in_table = csvFile, out_view = "EMU_VIEW", field_info = fi)  
arcpy.MakeXYEventLayer_management(table = "EMU_VIEW", in_x_field = "Longitude", in_y_field = "Latitude", out_layer = "EMU")

#todo: copy shapefile
print "\nCopy EMU_test shapefile"
if arcpy.Exists(outputShapefile):
    arcpy.Delete_management(outputShapefile)
arcpy.CopyFeatures_management("EMU", outputShapefile)

#todo: update Timetamp field and get Unique VehicleID
lstVehicleID = []
print "\nUpdate Timestamp field"
arcpy.MakeFeatureLayer_management(outputShapefile, "EMU")
recs = arcpy.UpdateCursor("EMU")
rec = recs.next()
while rec:
    if not rec.VehicleID in lstVehicleID:
        lstVehicleID.append(rec.VehicleID)
    timeStamp = string.split(rec.Timestamp, "T")[1]
    timeStamp = string.split(timeStamp, ".")[0]
    timeStamp = string.split(timeStamp, "+")[0]
    rec.Timestamp = timeStamp
    recs.updateRow(rec)
    rec = recs.next()
del rec
del recs


###todo:make KML file
print "\nConvert EMU Layers from Map to KML"
extent = arcpy.Extent()
extent.XMin = 0
extent.XMax = 180
extent.YMin = -90
extent.YMax = 0

#todo: loop through layers
for v in lstVehicleID:
    sql = "\"VehicleId\" = \'" + v + "\'"
    print sql
    arcpy.MakeFeatureLayer_management(in_features = "EMU", out_layer = v, where_clause = sql)
    kmlFile = outFolder + os.path.sep + v + ".kmz"
    vfc = outFolder + os.path.sep + "tmp"
    arcpy.Select_analysis(in_features = "EMU", out_feature_class = vfc, where_clause = sql)
    arcpy.MakeFeatureLayer_management(in_features = vfc + ".shp", out_layer = "v")
    arcpy.ApplySymbologyFromLayer_management(in_layer = "v", in_symbology_layer = outputLayerfile)
    tmpLayer = outFolder + os.path.sep + "tmpLayer.lyr"
    arcpy.SaveToLayerFile_management (in_layer = "v", out_layer = tmpLayer)
    arcpy.LayerToKML_conversion(layer = tmpLayer, out_kmz_file = kmlFile, boundary_box_extent = extent)
    
#todo: cleanup
print "Cleanup"
del doc
arcpy.Delete_management(vfc)
arcpy.Delete_management(tmpLayer)
arcpy.Delete_management(vfc)

#todo: Measure elapsed
end = datetime.datetime.now()
print "\nRunning time: " + str(end - start)

#all good 
print '\nCompleted'

