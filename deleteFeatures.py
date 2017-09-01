#deleteFeatures.py

print "***\nDELETE FEATUES\n***"

#import modules
import arcpy, os


conn = r'D:\TEMP\me@db@atalgissdbp01.sde'

arcpy.env.workspace = conn
arcpy.env.overwriteOutput = 1


fcs = []
fcs.append(["gisadmin.StatsNZ_BdyMeshblock_XS","CAUYEAR"])
fcs.append(["gisadmin.StatsNZ_BdyCensusAreaUnit_XS","MBYEAR"])

for fc in fcs:

    sql = fc[1] + " = 2006"

    print fc[0]
    print sql

    #arcpy.MakeFeatureLayer_management(in_features = fc[0], out_layer = "tmp", where_clause = sql)

    print arcpy.GetCount_management(fc[0])

    #print fc[1]


print "Completed"
