#sjProcessSnitchToGIS.py

#Susan Jones
#23 December 2016

#Purpose: Merge Snith Data with Routes.

#import Modules
import os, arcpy, string

#banner
print '***\nGeoEnable Snitch with Routes\n***'

#declare Parameters
print '\nSet the parameters'
gdb = r'D:\TMP\SCATS GPS Coordinate\SCATS GPS Coordinate\SCATS_ODS.gdb'
snitch = 'Snitch'
snitchField = 'Route_Name'
routes = 'PT_IVUGTFSRoute_DV'
routeField = 'RouteName'

#environment Settings
arcpy.env.overwriteOutput = 1
arcpy.env.workspace = gdb

#create in_memory stuff
print '\nCreate in_memory stuff'
arcpy.MakeTableView_management(in_table = snitch, out_view = "snitch")
arcpy.MakeFeatureLayer_management(in_features = routes, out_layer = "routes")


print arcpy.GetCount_management("snitch")
print arcpy.GetCount_management("routes")

#join routes to snitch
print '\nJoin routes to snitch'
arcpy.AddJoin_management(in_layer_or_view = "snitch", in_field = snitchField, join_table = "routes", join_field = routeField, join_type = "keep_common")


#Work with the aggregated table
print '\nWork with the aggregated table'
print arcpy.GetCount_management("snitch")

##arcpy.RemoveJoin_management(in_layer_or_view = "snitch", join_name = "routes")


#cleanup
arcpy.Delete_management(in_data = "snitch")
arcpy.Delete_management(in_data = "routes")


#completed
print '\nCompleted'
