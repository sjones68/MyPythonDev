#smjMakeQueryTable.py

#Susan Jones

#Working with DBMS Query Tables

import arcpy, os

#parameters
arcpy.env.overwriteoutput = 1
arcpy.env.qualifiedFieldNames = False
arcpy.env.workspace = r'D:\TEMP\scratch.gdb'

#banner
print "***\nworking With A Many To One Relationship\n***"

#todo: declare parameters here
fc = "AucklandStravaMetro_Edges_NZTM"
fckey = 'AucklandStravaMetro_Edges_NZTM.edge_id'
tbl = r'Database Connections\gis@atalgissdbu01.odc\GIS.gisadmin.auckland_edges_ride_data'
tblkey = 'edge_id'
sqlClause = "(year = 2013 AND hour IN (16,17)) AND day IN (7,14,21,28,35,42,49,56,63,70,77,84,91,98,105,112,119,126,133,140,147,154,161,168,175,182,189,196,203,210,217,224,231,238,245,252,259,266,273,280,287,294,301,308,315,322,329,336,343,350,357,364)"
whereClause = "(CycleEvents.edge_id = AucklandStravaMetro_Edges_NZTM.edge_id)"

#todo: make query Layer
print 'make Query Layer'
listTables = []
listTables.append(tbl)
arcpy.MakeQueryTable_management(in_table = listTables, out_table = "auckland_edges_ride_data", in_key_field_option = "ADD_VIRTUAL_KEY_FIELD")

#copy Query Table Locally
print 'Copy Query Tables Locally to Cycle Events'
if arcpy.Exists("CycleEvents"):
    arcpy.Delete_management("CycleEvents")
arcpy.CopyRows_management("auckland_edges_ride_data", "CycleEvents")
flds = []
flds.append("edge_id")
arcpy.AddIndex_management(in_table = "CycleEvents", fields = flds, index_name = "EdgeIdIdx")

#many To One Join
#print "start Many To One Join"
#listTables = ["CycleEvents", fc]
#arcpy.MakeQueryTable_management(in_table = listTables, out_table = "temp1", in_key_field_option = "ADD_VIRTUAL_KEY_FIELD", where_clause = whereClause)
#print 'Copy Query Tables Locally to All Cycle Event Features'
#if arcpy.Exists("AllCycleEvents"):
#    print "deleting AllCycleEvents..."
#    arcpy.Delete_management("AllCycleEvents")
#print "copying AllCycleEvents..."
#arcpy.CopyRows_management("temp1", "AllCycleEvents")
flds = []
flds.append("edge_id")
#arcpy.AddIndex_management(in_table = "CycleEvents", fields = flds, index_name = "EdgeIdIdx")


#todo: all done
print "\n***completed"
