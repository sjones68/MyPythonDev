#pyProcessScats.py

#Susan Jones
#22 December 2016

#Purpose: process Scats data from raw csv files
# id
# sectionName
# Sequence
# Latitude
# Longitude

#import Modules
import os, arcpy, string, datetime
from operator import itemgetter

startTime = datetime.datetime.now()

#banner
print '***\nProcess SCATS data into a single table\n***\n'
#parameters
arcpy.env.overwriteOutput = 1
arcpy.env.qualifiedFieldNames = 1
folder = r'D:\TMP\SCATS GPS Coordinate\Demo\input\spatial'
gdb = r'D:\TMP\SCATS GPS Coordinate\Demo\output\Scats_Demo_January2016.gdb'
fc = 'Scats'
tbl = 'Scats_Attributes'
tblBus = 'BusAttributes' #Display_Route_Number
routesIVU = "PT_IVUGTFSRoute_DV"  #RouteNumber
n = 0

arcpy.env.workspace = gdb

#1. Fetch Files for Processing (fileList)
print '\n1. Fetch Files for Processing (fileList)'
files = os.listdir(folder)
fileList = []
for f in files:
    if f.find(".csv") > -1:
        fileList.append(folder + os.path.sep + f)

#settings
arcpy.env.workspace = gdb
arcpy.env.overwriteOutput = 1

###2. Spatial Reference
print "\n2. Create Spatial Reference"
sr = arcpy.SpatialReference(4326)


#3. Process csv Files
print '\n1. Process csv Files'
arcpy.MakeFeatureLayer_management(in_features = fc, out_layer = "scatslyr")

##print "\n3. Process csv Files"
##for f in fileList:
##
##    print f + '...'
##
##    #initialise insert Cursor
##    print 'Initialise insert Cursor'
##    insRecs = arcpy.InsertCursor(dataset = "scatslyr")
##        
##    #make csvView
##    arcpy.MakeTableView_management(in_table = f, out_view = "csvView")
##    
##    #find all sectionName
##    sectionsList = []
##    recs = arcpy.SearchCursor(dataset = "csvView")
##    for rec in recs:
##        if not rec.SectionName in sectionsList:
##            sectionsList.append(rec.SectionName)
##    del recs
##    
##    #process sectionNames
##    n = 0
##    for section in sectionsList:
##        sql = "sectionName = \'" + section + "\'"
##        arcpy.MakeTableView_management(in_table = "csvView", out_view = "sectionView", where_clause = sql)
##        recs = arcpy.SearchCursor(dataset = "sectionView")
##        #construct the Polyline
##        features = []
##        pointArray = arcpy.Array()
##        for rec in recs:
##            features.append([rec.id, rec.sectionName, rec.Sequence, rec.Longitude, rec.Latitude])
##            scatsId = rec.Id
##        #sort features    
##        sortedFeatures = sorted(features, key = itemgetter(2))
##        for test in sortedFeatures:
##            pt = arcpy.Point(X = test[3], Y = test[4])
##            pointArray.add(pt)
##        #insert New Line
##        insRec = insRecs.newRow()
##        insRec.setValue("SHAPE", pointArray)
##        insRec.setValue("ID", scatsId)
##        insRec.setValue("SectionName", section)
##        insRecs.insertRow(insRec)
##        n += 1
##        
##    #print feature count
##    print f + ": " + str(n) + ' Features'
##
###cleanup
##del insRecs
##
###print feature count
##print str(n) + ' Features'


#Join Scats Features with Attributes
startTask = datetime.datetime.now()
print '\n2. Join Scats Features with Attributes'
arcpy.MakeTableView_management(in_table = tbl, out_view = "scatstbl")


fields = arcpy.ListFields("scatstbl")
for f in fields:
    print f.name


tables = ["scatstbl", "scatslyr"]
sql = "Scats_Attributes.Id = Scats.Id"
arcpy.MakeQueryTable_management(in_table = tables, out_table = "scatsFeatures", in_key_field_option = "ADD_VIRTUAL_KEY_FIELD", where_clause = sql)
endTask = datetime.datetime.now()
print 'elapsed ' + str(endTask - startTask)

#check and delete
startTask = datetime.datetime.now()
print '\n3. Copy Features to ScatsFeatures'
if arcpy.Exists("Scats_Features"):
    arcpy.Delete_management(in_data = "Scats_Features")
arcpy.CopyFeatures_management(in_features = "scatsFeatures", out_feature_class = "Scats_Features")
print arcpy.GetCount_management("scatsFeatures")
endTask = datetime.datetime.now()
print 'elapsed ' + str(endTask - startTask)



#cleanUp
startTask = datetime.datetime.now()
print '\n4. clean Up'
##arcpy.Delete_management(in_data = "sectionView")
##arcpy.Delete_management(in_data = "csvView")
##arcpy.Delete_management(in_data = "scatslyr")
##arcpy.Delete_management(in_data = "scatstbl")
##arcpy.Delete_management(in_data = "scatsFeatures")

endTask = datetime.datetime.now()
print 'elapsed ' + str(endTask - startTask)



#completed
print '\ncompleted'

#elapsed
endTime = datetime.datetime.now()
print '\nelapsed ' + str(endTime - startTime)
