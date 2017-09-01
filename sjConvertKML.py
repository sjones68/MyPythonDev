#sjConvertKML.py

#import Modules
import arcpy, string

#banner
print "***\nProcess KML\'s\n***"



#parameters
folder = r'D:\TMP\SCATS GPS Coordinate\SCATS GPS Coordinate'

arcpy.env.workspace = folder

fcs = arcpy.ListFeatureClasses("*")

#loop fcs
for fc in fcs:
    print arcpy.GetCount_management(fc)


#completed
print "completed"
