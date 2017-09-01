#sjParseXML_Smarktrak.py

#purse Parse XML objects into KML


#import Modules
import xml, string, os, arcpy, datetime, shutil
from xml.dom.minidom import parse

#start
start = datetime.datetime.now()

#todo: Banner and Parameters
print '***\nEMU File Conversion\n\nSusan Jones\n8 January 2015\n***\n'
csvFile = r'd:\tmp\AT_EMU.csv'
kmlFile = r'd:\tmp\tmpEMU.kmz'
outFolder = r'd:\tmp'
outputGDB = r'd:\tmp\EMU_Smartrak.gdb'
outputLayerfile = r'd:\tmp\EMU_Smartrak.lyr'
arcpy.env.overwriteOutput = 1
arcpy.env.workspace = outputGDB

#todo: make Spatial Reference
sr = arcpy.SpatialReference(4326)

#todo: make XY Event Layer
print "\nMake EMU event Layer"
fi = arcpy.FieldInfo()

arcpy.MakeTableView_management(in_table = csvFile, out_view = "EMU_VIEW", field_info = fi)  
arcpy.MakeXYEventLayer_management(table = "EMU_VIEW", in_x_field = "Longitude_wgs84", in_y_field = "Latitude_wgs84", out_layer = "EMU", spatial_reference = sr)

#todo: copy shapefile
print "\nCopy EMU_test feature class"
if arcpy.Exists("EMU_Smartrak"):
    arcpy.Delete_management("EMU_Smartrak")
arcpy.CopyFeatures_management("EMU", "EMU_Smartrak")

#todo: update Timetamp field and get Unique VehicleID
lstVehicleID = []
print "\nUpdate Timestamp field"
arcpy.MakeFeatureLayer_management("EMU_Smartrak", "EMU")

recs = arcpy.UpdateCursor("EMU")
rec = recs.next()
while rec:
    if not rec.remotename in lstVehicleID:
        lstVehicleID.append(rec.remotename)
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
    sql = "remotename = \'" + v + "\'"
    print sql
##    arcpy.MakeFeatureLayer_management(in_features = "EMU", out_layer = "v", where_clause = sql)
    kmlFile = outFolder + os.path.sep + v + ".kmz"
    arcpy.Select_analysis(in_features = "EMU", out_feature_class = v, where_clause = sql)
    arcpy.DeleteField_management(in_table = v, drop_field = "remoteid")
    arcpy.DeleteField_management(in_table = v, drop_field = "remotename")
    arcpy.MakeFeatureLayer_management(in_features = v, out_layer = "v")
    arcpy.ApplySymbologyFromLayer_management(in_layer = "v", in_symbology_layer = outputLayerfile)
    tmpLayer = outFolder + os.path.sep + "tmpLayer.lyr"
    arcpy.SaveToLayerFile_management (in_layer = "v", out_layer = tmpLayer)
    arcpy.LayerToKML_conversion(layer = tmpLayer, out_kmz_file = kmlFile, boundary_box_extent = extent)
    arcpy.KMLToLayer_conversion(in_kml_file = kmlFile, output_folder = outFolder)
    
    
#todo: cleanup
print "Cleanup"
#arcpy.Delete_management(tmpLayer)


#todo: Measure elapsed
end = datetime.datetime.now()
print "\nRunning time: " + str(end - start)

#all good 
print '\nCompleted'

