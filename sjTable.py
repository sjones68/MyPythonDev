#sjTable.py


#import Modules
import arcpy, string

#banner
print '***\nWorking with Domains and Table\n***\n'

#declare parameters
maxLength = 0
tbl = r'D:\TMP\ScratchGDB.gdb\Area_Unit_2016_Generalised_Version'

arcpy.MakeTableView_management(tbl, "tbl")
fields = ["au2016_name"]


#todo: find the maximum length of the description
recs = arcpy.da.SearchCursor(in_table = "tbl", field_names = fields)
for rec in recs:
    if len(rec[0]) > maxLength:
        largestVal = rec[0]
        maxLength = len(rec[0])
        
print '\nRecommendation: Make the description field ' + str(maxLength) + ' varchar (' + largestVal + ')'

#garbage collection
del rec
del recs
arcpy.Delete_management("tbl")


print '\ncompleted - because Susan is very cool'
