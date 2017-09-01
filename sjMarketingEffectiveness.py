#sjMarketingEffectiveness.py

##import modules
import arcpy, string, os, datetime, pyodbc

##measure The Start Time
startTime = datetime.datetime.now()

##banner
print "***\nMARKETING EFFECTIVENESS\n\n\nProject Workspace: \\atalgisau01\\projects\\AT16\\AT16027\n\nSusan Jones\n16 January 2016\n***"

##get Features
print "\ntodo: Define The Features"
gdb = r"\\atalgisau01\projects\AT16\AT16027\ProjectData.gdb"
distance = 17000 #define distance search threshold
stops = "\\\\atalgisau01\\admin\\Maintenance\\connections\\dba@AT@atalgissdbp01.sde\\AT.GISADMIN.PT_IVUGTFSStop_DV"
cau = "\\\\atalgisau01\\admin\\Maintenance\\connections\\dba@EXT@atalgissdbp01.sde\\EXT.GISADMIN.StatsNZ_BdyCensusAreaUnit_XS"
wards = "\\\\atalgisau01\\admin\\Maintenance\\connections\\dba@EXT@atalgissdbp01.sde\\EXT.GISADMIN.AucklandCouncil_Ward"
suburbs = "\\\\atalgisau01\\admin\\Maintenance\\connections\\dba@AT@atalgissdbp01.sde\\AT.GISADMIN.PJ_AucklandRegion_NZFS_SubSuburbs_TE"

##settings
print "\ntodo: Settings"
arcpy.env.overwriteOutput = 1
arcpy.env.workspace = gdb

##spatial Join stops with CAU
startTask = datetime.datetime.now()
print "\n1. todo: Process Census Area Unit"
sql = "CAUDescription not like 'Ocean%' and CAUDescription not like '%Harbour'"
arcpy.MakeFeatureLayer_management(in_features = stops, out_layer = "stopsLyr")
print str(arcpy.GetCount_management("stopsLyr")) + " features"
arcpy.MakeFeatureLayer_management(in_features = cau, out_layer = "cauLyr", where_clause = sql)
if arcpy.Exists("zones"):
    arcpy.Delete_management(in_data = "zones")
arcpy.SpatialJoin_analysis (target_features = "stopsLyr",
                            join_features = "cauLyr",
                            out_feature_class = "zones",
                            join_type = "KEEP_ALL",
                            match_option = "WITHIN_A_DISTANCE",
                            search_radius = distance,
                            distance_field_name = "DISTANCE")
arcpy.MakeFeatureLayer_management(in_features = "zones", out_layer = "zonesLyr")
fields = arcpy.ListFields("zonesLyr")
fields = ["STOPID", "STOPNAME","CAUDESCRIPTION", "DISTANCE"]
recs = arcpy.da.SearchCursor(in_table = "zonesLyr", field_names = fields)
cauList = []
for rec in recs:
    cauList.append([rec[0], rec[1], rec[2], rec[3]])
print str(len(cauList)) + " joined"
arcpy.Delete_management(in_data = "zones")
arcpy.Delete_management(in_data = "zonesLyr")
endTask = datetime.datetime.now()
print "elapsed " + str(endTask - startTask)

##spatial Join stops with Wards
startTask = datetime.datetime.now()
print "\n2. todo: Process Ward"
print str(arcpy.GetCount_management("stopsLyr")) + " features"
arcpy.MakeFeatureLayer_management(in_features = wards, out_layer = "cauLyr")
arcpy.SpatialJoin_analysis (target_features = "stopsLyr",
                            join_features = "cauLyr",
                            out_feature_class = "zones",
                            join_type = "KEEP_ALL",
                            match_option = "WITHIN_A_DISTANCE",
                            search_radius = distance,
                            distance_field_name = "DISTANCE")
arcpy.MakeFeatureLayer_management(in_features = "zones", out_layer = "zonesLyr")
fields = ["STOPID", "WARD", "DISTANCE"]
recs = arcpy.da.SearchCursor(in_table = "zonesLyr", field_names = fields)
wardList = []
for rec in recs:
    wardList.append([rec[0], rec[1], rec[2]])
print str(len(wardList)) + " joined"
arcpy.Delete_management(in_data = "zones")
arcpy.Delete_management(in_data = "zonesLyr")
endTask = datetime.datetime.now()
print "elapsed " + str(endTask - startTask)

##spatial Join stops with Suburbs
startTask = datetime.datetime.now()
print "\n3. todo: Process Suburbs"
print str(arcpy.GetCount_management("stopsLyr")) + " features"
sql = "SUBURB_4TH IS NOT NULL"
arcpy.MakeFeatureLayer_management(in_features = suburbs, out_layer = "cauLyr", where_clause = sql)
arcpy.SpatialJoin_analysis (target_features = "stopsLyr",
                            join_features = "cauLyr",
                            out_feature_class = "zones",
                            join_type = "KEEP_ALL",
                            match_option = "WITHIN_A_DISTANCE",
                            search_radius = distance,
                            distance_field_name = "DISTANCE")
arcpy.MakeFeatureLayer_management(in_features = "zones", out_layer = "zonesLyr")
fields = ["STOPID", "SUBURB_4TH", "DISTANCE"]
recs = arcpy.da.SearchCursor(in_table = "zonesLyr", field_names = fields)
suburbList = []
for rec in recs:
    suburbList.append([rec[0], rec[1], rec[2]])
print str(len(suburbList)) + " joined"
arcpy.Delete_management(in_data = "zones")
arcpy.Delete_management(in_data = "zonesLyr")
endTask = datetime.datetime.now()
print "elapsed " + str(endTask - startTask)

##cauList, wardList, suburbList
startTask = datetime.datetime.now()
print "\n3. todo: Populate IVUStopsOverlay.csv"
if os.path.exists(r"\\atalgisau01\projects\AT16\AT16027\03_Outputs\IVUStopsOverlay.csv"):
    os.remove(r"\\atalgisau01\projects\AT16\AT16027\03_Outputs\IVUStopsOverlay.csv")
fs = open("\\\\atalgisau01\\projects\\AT16\\AT16027\\03_Outputs\\IVUStopsOverlay.csv", "w")
f = 0
fs.write("StopID,StopName,CAU,CAU_Distance,Ward,Ward_Distance,Suburb,Suburb_Distance\n")
while f < len(cauList):
    fs.write(str(cauList[f][0])+","+str(cauList[f][1]+","+str(cauList[f][2])+","+str(cauList[f][3])+","))
    fs.write(str(wardList[f][1])+","+str(wardList[f][2])+",")
    fs.write(str(suburbList[f][1])+","+str(suburbList[f][2])+"\n")
    f += 1
fs.close()
print "\\\\atalgisau01\\projects\\AT16\\AT16027\\03_Outputs\\IVUStopsOverlay.csv"
endTask = datetime.datetime.now()
print "elapsed " + str(endTask - startTask)

##update the gis_gtfs_Stop_attributes table
startTask = datetime.datetime.now()
print "\n4. todo: Update gis_gtfs_Stopattributes"
areaTbl = "\\\\atalgisau01\\projects\\AT16\\AT16027\\03_Outputs\\IVUStopsOverlay.csv"
cnxn = pyodbc.connect(driver = '{SQL Server}', server = 'atalsdbu01', database = 'arta_staging', trusted_connection = 'yes')
cursor = cnxn.cursor()

arcpy.MakeTableView_management(in_table = areaTbl, out_view = "areaTbl")
fields = ["StopID", "CAU", "WARD", "SUBURB"]
recs = arcpy.da.SearchCursor(in_table = "areaTbl", field_names = fields)

##update Records
for rec in recs:
    #update records
    updateSql = "UPDATE gis_gtfs_Stopattributes SET area_unit = \'" + rec[1] + "\', ward = \'" + string.replace(rec[2], " - ", "-") + "\', suburb = \'" + rec[3] + "\' WHERE Stop_Id = " + str(rec[0]) + ";"
    cnxn.execute(updateSql)
cnxn.commit()
del recs
endTask = datetime.datetime.now()
print "elapsed " + str(endTask - startTask)

#cleanup
arcpy.Delete_management(in_data = "cauLyr")
arcpy.Delete_management(in_data = "stopsLyr")
arcpy.Delete_management(in_data = "stopsTbl")
arcpy.Delete_management(in_data = "areaTbl")

##completed
print "\ncompleted"

##measure The Elapsed Time
endTime = datetime.datetime.now()
print "\nelapsed " + str(endTime - startTime)
