#sjCalculateRasterCalalog.py


#todo: import moduless
import arcpy, os, string

print "***\nCalculate Raster Extents\n***"

#parameters
folder = r"d:\tmp"
fn = folder + os.path.sep + "rCatalog.csv"

#processing Variables
arcpy.env.workspace = folder

if os.path.exists(fn):
    os.remove(fn)
fs = open(fn, "w")
fs.write("IMAGE,XMIN,YMIN,XMAX,YMAX\n")

rsts = arcpy.ListRasters("*.jpg")
for rst in rsts:
##    newfn = string.replace(rst, ".jpg", ".tif")
##    arcpy.CopyRaster_management(rst, newfn)
    ext = arcpy.Describe(rst).extent
    extDetails = folder + os.path.sep + rst + "," + str(ext.XMin) + "," + str(ext.XMax) + "," + str(ext.YMin) + "," + str(ext.YMax) + "\n"
    fs.write(extDetails)

fs.close()

print "completed"
