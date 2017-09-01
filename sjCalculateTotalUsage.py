#sjCalculateTotalUsage.py

#Purpose:
#Calculate AT Monthly HOP Usage

#Authoring
#Susan Jones
#5 October 2016

#import Modules
import datetime, string, arcpy

#banner
print "***\nCalculate AT Monthly HOP Usage\n\nSusan Jones\n5 October 2016\n***"

#todo: collect And Set Parameters

#worspaces
wsp = r'\\atalgisau01\Projects\AT14\AT14043\Data\NonSDEDataSource.gdb'
stgwsp = r'D:\TMP\Geoprocessing.gdb'

#featureClasses (Hardcoded)
HOPRegionalClassification = r'\\atalgisau01\Projects\AT16\AT16135\ProjectData.gdb\HOP_District'
PTStations = r'D:\TMP\Geoprocessing.gdb\PT_IVUGTFSStop_DV'

arcpy.env.overwriteOutput = 1
arcpy.env.workspace = wsp

#todo: create a Feature Layer for Districts
start = datetime.datetime.now()
print "\ntodo: create a Feature Layer for Districts"
if arcpy.Exists("Districts"):
    arcpy.Delete_management("Districts")
arcpy.MakeFeatureLayer_management(in_features = HOPRegionalClassification, out_layer = "mmHOPRegionalClassification")
arcpy.MakeFeatureLayer_management(in_features = PTStations, out_layer = "mmPTStations")
arcpy.Identity_analysis(in_features = "mmPTStations", identity_features = "mmHOPRegionalClassification", out_feature_class = stgwsp + "\\Districts")
arcpy.MakeFeatureLayer_management(in_features = stgwsp + "\\Districts", out_layer = "mmDistricts")
arcpy.AddIndex_management(in_table = "mmDistricts", fields = "StopId", index_name = "StopIdIdx")
end = datetime.datetime.now()
print "elapsed " + str(end - start)

#list Fields
deleteFields = ["FID_PT_IVUGTFSStop_DV"]
deleteFields.append("STOPLAT")
deleteFields.append("STOPLON")
deleteFields.append("PARENTSTATION")
deleteFields.append("PARENTSTATION")
deleteFields.append("MODE")
deleteFields.append("CREATEBY")
deleteFields.append("CREATEDATE")
deleteFields.append("MODIFYBY")
deleteFields.append("MODIFYDATE")
deleteFields.append("FID_HOP_District")
deleteFields.append("STOPCODE")
deleteFields.append("STOPNAME")
deleteFields.append("STOPDESC")
deleteFields.append("LOCATIONTYPE")

#todo: field Management
start = datetime.datetime.now()
print "\ntodo: field Management"
fields = arcpy.ListFields("mmDistricts")
for field in fields:
    #remove field
    if field.name in deleteFields:
        print "removing " + field.name + "..."
        arcpy.DeleteField_management(in_table = "mmDistricts", drop_field = field.name)
end = datetime.datetime.now()
print "elapsed " + str(end - start)


#todo: cycle Through the Districts
fields = ["district"]
listDistrict = []
recs = arcpy.da.SearchCursor(in_table = "mmDistricts", field_names = fields)
for rec in recs:
    if not rec[0] in listDistrict:
        listDistrict.append(rec[0])
##print listDistrict

#todo: fetch the feature classes
print '\ntodo: fetch the featureclasses'
listFc = []
listFields = []
fcs = arcpy.ListTables()
for fc in fcs:
    listFc.append(fc)
listFc.sort()

#todo: process Featureclasses
print '\ntodo: process Featureclasses'
for fc in listFc:
    if fc.find("AT_Operations_PT_Stop_UniqueTransactionsAllModes") > -1:

        #todo; Notify the feature class processing
        print "\nProcessing " + fc + "..."
        arcpy.MakeTableView_management(in_table = "AT_Operations_PT_Stop_UniqueTransactionsAllModes", out_view = "mmOPS")

        #spatial Join
        print "\nAdd Join"
        arcpy.AddJoin_management(in_layer_or_view = "mmDistricts", in_field = "stopID", join_table = "mmOPS", join_field = "stopID", join_type = "keep_all") #stopID, stopID


        fields = arcpy.ListFields("mmDistricts")
        for field in fields:
            print field.name

        #todo: cycle through [u'', u'South', u'East', u'West', u'Central', u'N/A', u'North']
        print "\ntodo: cycle through [u'', u'South', u'East', u'West', u'Central', u'N/A', u'North']"
        
        listDistrict = ['South', 'East', 'West', 'Central', 'North']
        print "District,tagOnATHOP,paperATHOP,TotalATHOP"
        for district in listDistrict:

            #start = datetime.datetime.now()
        
            #todo: calculate Totals
            sqlQuery = "Districts.DISTRICT = \'" + district + "\'" ## AND AT_Operations_PT_Stop_UniqueTransactionsAllModes.TimePeriod = \'2016/09\'"
            #print sqlQuery  
            
            recs = arcpy.SearchCursor(dataset = "mmDistricts", where_clause = sqlQuery)
            rec = recs.next()
            n = 0
            tagOnATHOP = 0
            paperATHOP = 0
            for rec in recs:

                #tagOn Count
                if rec.getValue("AT_Operations_PT_Stop_UniqueTransactionsAllModes.AdultTagOn") != None:
                    tagOnATHOP = tagOnATHOP + int(rec.getValue("AT_Operations_PT_Stop_UniqueTransactionsAllModes.AdultTagOn"))
                if rec.getValue("AT_Operations_PT_Stop_UniqueTransactionsAllModes.ChildTagOn") != None:
                    tagOnATHOP = tagOnATHOP + int(rec.getValue("AT_Operations_PT_Stop_UniqueTransactionsAllModes.ChildTagOn"))
                if rec.getValue("AT_Operations_PT_Stop_UniqueTransactionsAllModes.SecondaryStudentTagOn") != None:
                    tagOnATHOP = tagOnATHOP + int(rec.getValue("AT_Operations_PT_Stop_UniqueTransactionsAllModes.SecondaryStudentTagOn"))
                if rec.getValue("AT_Operations_PT_Stop_UniqueTransactionsAllModes.TertiaryStudentTagOn") != None:
                    tagOnATHOP = tagOnATHOP + int(rec.getValue("AT_Operations_PT_Stop_UniqueTransactionsAllModes.TertiaryStudentTagOn"))
                if rec.getValue("AT_Operations_PT_Stop_UniqueTransactionsAllModes.SuperGoldTagOn") != None:
                    tagOnATHOP = tagOnATHOP + int(rec.getValue("AT_Operations_PT_Stop_UniqueTransactionsAllModes.SuperGoldTagOn"))


                #paper Count
                if rec.getValue("AT_Operations_PT_Stop_UniqueTransactionsAllModes.AdultPaper") != None:
                    paperATHOP = paperATHOP + int(rec.getValue("AT_Operations_PT_Stop_UniqueTransactionsAllModes.AdultPaper"))
                if rec.getValue("AT_Operations_PT_Stop_UniqueTransactionsAllModes.AccessiblePaper") != None:
                    paperATHOP = paperATHOP + int(rec.getValue("AT_Operations_PT_Stop_UniqueTransactionsAllModes.AccessiblePaper"))
                if rec.getValue("AT_Operations_PT_Stop_UniqueTransactionsAllModes.SecondaryStudentPaper") != None:
                    paperATHOP = paperATHOP + int(rec.getValue("AT_Operations_PT_Stop_UniqueTransactionsAllModes.SecondaryStudentPaper"))
                if rec.getValue("AT_Operations_PT_Stop_UniqueTransactionsAllModes.TertiaryStudentPaper") != None:
                    paperATHOP = paperATHOP + int(rec.getValue("AT_Operations_PT_Stop_UniqueTransactionsAllModes.TertiaryStudentPaper"))
                if rec.getValue("AT_Operations_PT_Stop_UniqueTransactionsAllModes.SuperGoldPaper") != None:
                    paperATHOP = paperATHOP + int(rec.getValue("AT_Operations_PT_Stop_UniqueTransactionsAllModes.SuperGoldPaper"))

                n += 1

            #tagOn Counts
            print district + "," + str(tagOnATHOP) + "," + str(paperATHOP) + "," + str(tagOnATHOP + paperATHOP)
            #print n


            #end = datetime.datetime.now()
            #print "elapsed " + str(end - start)


        #remove Join
        print "\nRemove Join"
        arcpy.RemoveJoin_management(in_layer_or_view = "mmDistricts")
        

#todo: cleanup
print "\ncleanup"
#del recs
arcpy.Delete_management(in_data = "mmHOPRegionalClassification")
arcpy.Delete_management(in_data = "mmPTStations")
arcpy.Delete_management(in_data = "mmDistricts")
arcpy.Delete_management(in_data = "mmOPS")


print '\ncompleted'
