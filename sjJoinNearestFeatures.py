#sjJoinNearestFeatures.py

#modules
import arcpy, os, string, datetime

startTime = datetime.datetime.now()

#banner
print "***\nJoin with Nearest Features\n***"

#fetch Parameters
print "\nfetch Parameters"
arcpy.env.overwriteOutput = 1
scratchWorkspace = r"D:\TMP\Geoprocessing.gdb"
stopFeatures = "\\\\atalgisau01\\admin\\Maintenance\\connections\\dba@AT@atalgissdbp01.sde\\AT.GISADMIN.PT_IVUGTFSStop_DV"
statsFeatures = "\\\\atalgisau01\\admin\\Maintenance\connections\\dba@EXT@atalgissdbp01.sde\\EXT.GISADMIN.StatsNZ_BdyCensusAreaUnit_XS"
csvFile = "d:\\TMP\\StationsCAU.csv"

#check for Existance
arcpy.env.workspace = scratchWorkspace

print "\n1. processing data layers"
if arcpy.Exists("PT_IVUGTFSStop_DV"):
    arcpy.Delete_management("PT_IVUGTFSStop_DV")
arcpy.CopyFeatures_management(stopFeatures, "PT_IVUGTFSStop_DV")
if arcpy.Exists("StopAttributes"):
    arcpy.Delete_management("StopAttributes")
if arcpy.Exists("StatsNZ_BdyCensusAreaUnit_XS"):
    arcpy.Delete_management("StatsNZ_BdyCensusAreaUnit_XS")
arcpy.CopyFeatures_management(statsFeatures, "StatsNZ_BdyCensusAreaUnit_XS")

#make Feature Layers
print "\n2. make Feature Layers"
sql = "CAUDESCRIPTION not like \'Ocean%\'"
#print sql
arcpy.MakeFeatureLayer_management(in_features = "PT_IVUGTFSStop_DV", out_layer = "Stops")
arcpy.MakeFeatureLayer_management(in_features = "StatsNZ_BdyCensusAreaUnit_XS", out_layer = "Census", where_clause = sql)

#join Layers
print "\n3. join Layers"
arcpy.SpatialJoin_analysis(
                target_features = "Stops",
                join_features = "Census",
                out_feature_class = "StopAttributes",
                distance_field_name = "DISTANCE",
                match_option = "WITHIN_A_DISTANCE",
                search_radius = 5000)

#get StopID, CauDescription
print "\n4. get StopID, CauDescription"
fields = ["StopID", "CAUDESCRIPTION"]
sql = "DISTANCE = 0"
stopSet = []
rows = arcpy.da.SearchCursor(in_table = "StopAttributes", field_names = fields)
for row in rows:
    stopSet.append([row[0],row[1]])
del rows

#check the Tuple called stopSet
##print len(stopSet)
##print str(stopSet[0][0]) + "," + stopSet[0][1]  ##eg. 7764,Freemans Bay

#write The file
if os.path.exists(path = csvFile):
    os.remove(csvFile)
fs = open(name = csvFile, mode = "w") ## header Line
fs.write("StopID,CAU\n")
for stop in stopSet:
    fs.write(str(stop[0])+","+str(stop[1])+"\n")
fs.close()

#cleanup
print "\ncleanUp"
arcpy.Delete_management(in_data = "StopAttributes")
arcpy.Delete_management(in_data = "Stops")
arcpy.Delete_management(in_data = "Census")

#completed
print "\ncompleted"

endTime = datetime.datetime.now()
print ("\nelapsed " + str(endTime - startTime))
