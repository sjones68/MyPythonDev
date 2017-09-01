#getFeatureCount.py


#todo: get The Feature Counts
print "***\nGet Feature Counts\n"


#import Modules
import arcpy, string

#connection string workspace
conn = r"\\atalgisau01\ADMIN\Maintenance\connections\gisadmin@AT@atalgissdbp01.sde"

#todo: feath Parameters
arcpy.env.workspace = conn
arcpy.env.overwriteOutput = 1

#make List of fcs
featureList = []
featureList.append("AT.GISADMIN.PG_MasterProjectArea_TE")
featureList.append("AT.GISADMIN.PG_MasterProjectAreaAll_DV")
featureList.append("AT.GISADMIN.PG_MasterProjectFinancialsAll_DV")
featureList.append("AT.GISADMIN.PG_MasterProjectFinancialsSummary_DV")
featureList.append("AT.GISADMIN.PG_MasterProjectLocation_TE")
featureList.append("AT.GISADMIN.PG_MasterProjectLocationAll_DV")
featureList.append("AT.GISADMIN.PG_MasterProjectPhaseAreaAll_DV")
featureList.append("AT.GISADMIN.PG_MasterProjectPhaseFinancialsAll_DV")
featureList.append("AT.GISADMIN.PG_MasterProjectPhaseFinancialsSummary_DV")
featureList.append("AT.GISADMIN.PG_MasterProjectRoute_TE")

#cycle Through the FeatureClasses
fcs = arcpy.ListFeatureClasses("*PG_*")
for fc in fcs:
    if fc in featureList:
        arcpy.MakeFeatureLayer_management(fc, "fc")
        print str(arcpy.GetCount_management("fc")) + "\t" + fc
        arcpy.Delete_management("fc")

#completed
print "complete"
