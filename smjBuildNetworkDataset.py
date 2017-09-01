#smjBuildNetworkDataset.py

#import Modules
import arcpy, datetime, string

print "***\nUPDATE NETWORK DATASET\nSusan Jones\nAuckland Transport\n***"

start = datetime.datetime.now()

print "Checking out Network Analyst"
arcpy.CheckOutExtension("Network")

#define Data Sources
srcRCL = r'D:\TMP\gisadmin@atalgissdbu01.sde\AC.GISADMIN.ATNet_Sj\AC.GISADMIN.RORoadCL'
srcInts = r'D:\TMP\gisadmin@atalgissdbu01.sde\AC.GISADMIN.ATNet_Sj\AC.GISADMIN.ROIntersections'
srcTurns = r'D:\TMP\gisadmin@atalgissdbu01.sde\AC.GISADMIN.ATNet_Sj\AC.GISADMIN.RO_Turn1'
srcFeatures = [srcRCL, srcInts, srcTurns]

#define Data Sources
destRCL = r'D:\TMP\testNetwork.gdb\ATNet_Sj\RORoadCL'
destInts = r'D:\TMP\testNetwork.gdb\ATNet_Sj\ROIntersections'
destTurns = r'D:\TMP\testNetwork.gdb\ATNet_Sj\RO_Turn1'
destFeatures = [destRCL, destInts, destTurns]


#define Destination Sources
arcpy.env.workspace = r'D:\TMP\gisadmin@atalgissdbu01.sde'
##nd = r'D:\TMP\testNetwork.gdb\ATNet_Sj\ATNet_Sj_ND'
##turnFeatures = r'D:\TMP\testNetwork.gdb\ATNet_Sj\RO_Turn1'

#environment
arcpy.env.overwriteOutput = 1
edit = arcpy.da.Editor(r'D:\TMP\gisadmin@atalgissdbu01.sde')


#todo: delete Features
#print "todo: DELETE FEATURES"
#edit.startEditing(True, True)

#loop fc
for fc in srcFeatures:
    #edit.startOperation()
    arcpy.DeleteFeatures_management(fc)
    #edit.stopOperation()


#save Edits
print "saving Edits"
#edit.stopEditing(True)




#todo: snapping Environment
print "Make Snapping Environment"
#arcpy.Snap_edit("srcInts", [["RCL", "VERTEX", "5"]])


#todo: insert Into destRCL
print "Update " + srcRCL
edit.startEditing(True, True)
flds = arcpy.ListFields(destRCL)
recs = arcpy.da.SearchCursor(destRCL, "*")
irecs = arcpy.InsertCursor(srcRCL, "*")

for rec in recs:
    i = 0
    print "Next"
    edit.startOperation()
    irec = irecs.newRow()
    while i < len(rec) - 1:
        irec = rec[i]
        i += 1
    irecs.insertRow(irec)
    edit.stopOperation()    
    

print "done"

#save Edits
print "saving Edits"
edit.stopEditing(True)


###establish Editing Environments
##edit.startEditing(True, True)
##edit.startOperation()
##
###update the edge references in turn features using the geometry
##print "\nupdating Turns..."
##bg = datetime.datetime.now()
##arcpy.na.UpdateByGeometry(turnFeatures)
##edit.stopOperation()
##
###save Edits
##edit.stopEditing(True)
##
##print str(datetime.datetime.now() - bg)
##
#build Network
##print "\nbuild Network..."
##bg = datetime.datetime.now()
##arcpy.na.BuildNetwork(nd)
##print str(datetime.datetime.now() - bg)
##
###describe Network
##print arcpy.Describe(nd).supportsTurns

print "Checking in Network Analyst"
arcpy.CheckInExtension("Network")

#tool Completion Time
print str(datetime.datetime.now() - start)

#completed
print "completed"
