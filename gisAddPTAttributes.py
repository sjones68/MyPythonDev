#gisAddPTAttributes.py

#Purpose:
#Create full attribution for the arta_staging.dbo.gis_gtfs_station table in the data warehouse.
#Attribution is based on Auckland Council and Census Boundaries.

#Source dataset - at.gisadmin.gis_gtfs_stop
#Destination dataset - arta_staging.dbo.gis_gtfs_stop_attributes

#import the modules
import arcpy, os, sys, string



#banner
print "***\nPerform attribution for gis_gtfs_stopAttributes\n***"


#todo: set Paramters
srcDb = r'Database Connections\gisadmin@db@atalgissdbu01.sde'
srcTable = srcDb + "\\AT.GISADMIN.PT_StopAttributes_DV"

destDb = r"Database Connections\ARTA_STAGING@ATALSDBU01.odc"
destTable = destDb + "\\dbo.gis_gtfs_stopattributes"

arcpy.env.overwriteOutput = 1
##arcpy.env.workspace = descSource


#todo: set up a Join
print "make Feature Layer"
arcpy.MakeFeatureLayer_management(in_features = srcTable, out_layer = "StopAttributes")

print "make Table View"
arcpy.MakeTableView_management(in_table = destTable, out_view = "StopAttributesUpdate")

print "add Join"
arcpy.AddJoin_management(in_layer_or_view = "StopAttributes", in_field = "stopid", join_table = "StopAttributesUpdate", join_field = "stop_id", join_type = "KEEP_COMMON")

flds = arcpy.ListFields("StopAttributes")
for fld in flds:
    print fld.name


print "\ncalculate suburb"
arcpy.CalculateField_management(in_table = "StopAttributes", field = "SUBURB", expression = "AT.GISADMIN.PT_StopAttributes_DV.SUBURB")


#todo: remove a Join
#print "remove Join"
#arcpy.RemoveJoin_management(in_layer_or_view = "StopAttributes", join_name = "dbo")


    


#todo: cleanup
print "\nCleanup"
arcpy.Delete_management(r"in_memory\StopAttributes")
#del recs


#complete
print "Complete"


