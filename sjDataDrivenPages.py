#sjDataDrivenPages.py

#import Modules
import arcpy

arcpy.env.overWriteOutput = 1

#todo: mxd
print 'get MXD'

#todo: HARDCODE BELOW
mxd = arcpy.mapping.MapDocument(r"D:\tmp\ZoneImagesSusan.mxd")

#todo: environment Settings
arcpy.env.rasterStatistics = "None"

#todo get data frame
print 'get Data Frames'
df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
sr = arcpy.SpatialReference(2193)

print df.name

#todo export jpegs
print 'export JPEG'
for pageNum in range(1, mxd.dataDrivenPages.pageCount + 1):

    print 'export ' + str(pageNum) + '...'
    mxd.dataDrivenPages.currentPageID = pageNum

    #todo: HARDCODE BELOW r"D:\tmp\Output"
    arcpy.mapping.ExportToJPEG(mxd, r"D:\tmp\Output" + str(pageNum) + ".jpg", df, df_export_width = 1200, df_export_height = 1600, world_file=True, resolution = 300, color_mode = "24-BIT_TRUE_COLOR")
    arcpy.DefineProjection_management(r"D:\tmp\Output" + str(pageNum) + ".jpg", sr)
    arcpy.BuildPyramids_management(r"D:\tmp\Output" + str(pageNum) + ".jpg")


#todo remove Object
del mxd

#todo my Cool Message
print "Susan is Very cool"
