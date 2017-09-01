#sjCheckTables.py


#todo: check TimePeriod

#import Modules
import arcpy, string, os
import datetime

print "***\nCheck The Data\n***"

#todo: set Parameters
fme = r"c:\apps\FME\fme.exe"
gdb = r"\\atalgisau01\Projects\AT14\AT14043\Data\NonSDEDataSource.gdb"
sde = r"\\atalgisau01\admin\Maintenance\connections\gisadmin@GIS@atalgissdbu01.sde"
arcpy.env.workspace = gdb
arcpy.env.overwriteOutput = 1

#todo: set Parameters
arcpy.env.workspace = gdb
arcpy.env.overwriteOutput = 1


#todo: varTimePeriod
varTimePeriod = str(datetime.datetime.now() - datetime.timedelta(hours = (24*30)))
varTimePeriod = varTimePeriod[0:4] + "/" +  varTimePeriod[5:7]
fld = "TimePeriod"
strWhere = fld + " = \'" + varTimePeriod + "\'"
print strWhere


#todo: 1. PT HOP: Create EDW Data Extract
print "\ntodo: 1. PT HOP: Create EDW Data Extract"
start = datetime.datetime.now()
package = r"\\atalgisau01\PROJECTS\AT14\AT14043\Scripts\HOPHeatMaps1_DW_DataExtract_16052016.fmw" 
cmd = fme + " " + package + " --varTimePeriod " + varTimePeriod
#os.system(cmd)
print cmd
end = datetime.datetime.now()
print 'elapsed ' + str(end - start)


#todo: 2. PT HOP: Create Station Points
print "\ntodo: 2. PT HOP: Create Station Points"
start = datetime.datetime.now()
package = r"\\atalgisau01\PROJECTS\AT14\AT14043\Scripts\HOPHeatMaps3_CreateStationPoints_16052016.fmw"
cmd = fme + " " + package
#os.system(cmd)
print cmd
end = datetime.datetime.now()
print 'elapsed ' + str(end - start)


#todo: 3. PT HOP: Create Pivot Tables
print "\ntodo: 3. PT HOP: Create Pivot Tables"
start = datetime.datetime.now()
package = r"\\atalgisau01\PROJECTS\AT14\AT14043\Scripts\HOPHeatMaps2_PivotTables_16052016.fmw"
cmd = fme + " " + package
#os.system(cmd)
print cmd
end = datetime.datetime.now()
print 'elapsed ' + str(end - start)


#todo: 4. PT HOP: Summarise by Census Area Unit
print "\ntodo: 4. PT HOP: Summarise by Census Area Unit"
start = datetime.datetime.now()
package = r"\\atalgisau01\PROJECTS\AT14\AT14043\Scripts\HOPHeatMaps4_SummariseByCAU_16052016.fmw."
cmd = fme + " " + package + " --varTimePeriod " + varTimePeriod
os.system(cmd)
print cmd
end = datetime.datetime.now()
print 'elapsed ' + str(end - start)


#todo: 5. PT HOP: Summarise by Grid
print "\ntodo: 5. PT HOP: Summarise by Grid"
start = datetime.datetime.now()
package = r"\\atalgisau01\PROJECTS\AT14\AT14043\Scripts\HOPHeatMaps4_SummariseByGrid_16052016.fmw."
cmd = fme + " " + package
os.system(cmd)
print cmd
end = datetime.datetime.now()
print 'elapsed ' + str(end - start)




#todo: 6. Load the PT HOP Tables in ArcSDE
print "\ntodo: 6. Load the PT HOP Tables in ArcSDE"

#define table to be updated in ArcSDE Database
tables = []
tables.append("AT_Operations_PT_Stop_UniqueTransactionsBus")
tables.append("AT_Operations_PT_Stop_UniqueTransactionsAllModes")
tables.append("AT_Operations_PT_Stop_StoredValueTopup")
tables.append("AT_Operations_PT_Stop_DistinctHOPCardBus")
tables.append("AT_Operations_PT_Stop_DistinctHOPCardAllModes")
tables.append("AT_Operations_PT_Grid_UniqueTransactionsBus")
tables.append("AT_Operations_PT_Grid_UniqueTransactionsAllModes")
tables.append("AT_Operations_PT_Grid_DistinctHOPCardAllModes")
tables.append("AT_Operations_PT_Grid_DistinctHOPCardBus")
tables.append("AT_Operations_PT_Grid_DistinctHOPCardAllModes")
tables.append("AT_Operations_PT_CAU_UniqueTransactionsBusTrain")
tables.append("AT_Operations_PT_CAU_UniqueTransactionsBus")
tables.append("AT_Operations_PT_CAU_UniqueTransactionsAllModes")

#cycle through all the tables refreshing the ArcSDE datasource
for table in tables:

    try:
        start = datetime.datetime.now()
        #source SDE Tables
        SDETable = sde + os.path.sep + "GIS.GISADMIN." + table
        #arcpy.MakeTableView_management(in_table = SDETable, out_view = "SDETable", where_clause = strWhere)
        #todo: delete Features
        #arcpy.DeleteRows_management(in_rows = "SDETable")
        #todo: append Features
        #arcpy.MakeTableView_management(in_table = table, out_view = "GDBTable", where_clause = strWhere)
        #arcpy.Append_management(inputs = "GDBTable", target = "SDETable", schema_type = "TEST")
        end = datetime.datetime.now()
        #print table + " loaded in " + str(end - start) + " seconds (" + str(arcpy.GetCount_management("GDBTable")) + ")"
        #cleanup in_memory tables
        #arcpy.Delete_management("GDBTable")
        #arcpy.Delete_management("SDETable")

    except:
        print "cannot process " + table
       

print "\n***\ncompleted"
