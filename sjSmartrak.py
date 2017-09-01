#sjSmartrak.py

#Susan Jones
#29 January 2015

#import modules
import arcpy, string, datetime

#banner
print "***\nSmartrak Extraction Checks\n***"

#todo: parameters
dateFld = "dim_transaction_date_key"
wsp = r"\\atalgisau01\d$\projects\SMARTRAK CONGESTION\January\ProjectData.gdb"
fc = r"\\atalgisau01\d$\projects\SMARTRAK CONGESTION\January\ProjectData.gdb\fact_Smartrak_GetHistoryForPeriod_Jan2015"

#todo: set Parameters
arcpy.env.workspace = wsp

###todo: Table Details
##lstFc = string.split(fc,"\\")
##print lstFc[len(lstFc)-1]
##print "Records:\t" + str(arcpy.GetCount_management(fc))

###todo: Get Period
##print "\nreport Data Period"
##periodLst = []
##lstFields = [dateFld]
##arcpy.MakeTableView_management(fc, "Smartrak")
##recs = arcpy.da.SearchCursor(in_table = "Smartrak", field_names = lstFields)
##for rec in recs:
##    if rec[0] not in periodLst:
##        periodLst.append(rec[0])
##periodLst.sort()
##del recs
##
###todo: sorting
##for period in periodLst:
##    print period

#todo: index Building
print "\nbuild Indexes"
indexFields = ["EventHistoryId", "TransactionDate", "TransactionDateTime", "TransactionTime", "dim_transaction_date_key", "RemoteId"]
tbls = arcpy.ListTables()
lstFields = []
for tbl in tbls:
    print tbl
    flds = arcpy.ListFields(tbl)
    for fld in indexFields:
        print fld + "Idx..."
        start = datetime.datetime.now()
        lstField = [fld]
        arcpy.AddIndex_management(in_table = tbl, fields = lstField, index_name = fld + "Idx")
        end = datetime.datetime.now()
        print str(end - start)

#completed
print "\ncompleted"
