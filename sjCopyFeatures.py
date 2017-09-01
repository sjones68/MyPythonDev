#sjCopyFeatures.py

print "Copy Features..."

#import Modules
import arcpy, datetime

arcpy.env.overwriteOutput = 1

#parameters
src = r'D:\TEMP\StravaDatabase.gdb\AllCycleEvents'
dest = r'\\atalgisau01\PROJECTS\AT14\AT14215\03_Outputs\StravaDatabase.gdb\AllCycleEvents'

start =  datetime.datetime.now()
print start

#todo:copy Features
print "Copying..."
arcpy.CopyFeatures_management( src, dest)

end =  datetime.datetime.now()
print "Elapsed:\t" + str(end - start)

print "completed"

