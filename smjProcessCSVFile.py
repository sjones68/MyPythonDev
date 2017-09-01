#smjProcessCSVFile.py

#purpose:
#format putput in csv file

#todo: process CSV Files
print '***\nprocess KML into CSV Files\n***'

#todo: import Modules
import arcpy, os, string, zipfile

#todo: input datasets
kml = r'D:\TMP\CAFS_Nishant.kmz'
folder = r'd:\tmp' #folder Path
flds = ['FolderPath','Name','Longitude','Latitude']

#todo: environment Variables
arcpy.env.workspace = folder
arcpy.env.overWriteOutput = 1

#todo: check for the texistence of gedatabase
lstStr = string.split(kml, '\\')
lstStr = string.split(lstStr[len(lstStr) - 1], '.')
basename = lstStr[0]
gdb = folder + os.path.sep + basename + '.gdb'
if os.path.exists(gdb):
    print 'deleting ' + gdb
    arcpy.Delete_management(gdb)

#todo: kml to Layer
print 'converting ' + kml
arcpy.KMLToLayer_conversion( kml, folder) 

#todo: cycle cursor, update Longitude and latitude of Placemark\Points
print 'updating Longitude and Latitude'
ds = gdb + os.path.sep + "Placemarks\\Points"
arcpy.AddField_management(in_table = ds, field_name = "Longitude", field_type = "DOUBLE")
arcpy.AddField_management(in_table = ds, field_name = "Latitude", field_type = "DOUBLE")
lstFP = [] #list Of folder paths
n = 0
recs = arcpy.UpdateCursor(ds)
rec = recs.next()
while rec:
    if not rec.FolderPath in lstFP:
        lstFP.append(rec.FolderPath)
    shp = rec.shape.getPart(0)
    rec.Longitude = rec.shape.getPart(0).X
    rec.Latitude = rec.shape.getPart(0).Y
    recs.updateRow(rec)
    n += 1
    rec = recs.next()
del rec
del recs

#todo: make a zipefile
zipF = folder + os.path.sep + basename + '.zip'
print 'archiving into ' + zipF
if os.path.exists(zipF):
    os.remove(zipF)
zf = zipfile.ZipFile(zipF, 'w')

#todo: create CSV output
lstFP.sort()
for fp in lstFP:
    lstStr = string.split(fp, '/')
    fn = "CAFS_" + string.replace(lstStr[len(lstStr)-2], " ", "_") + "_" + string.replace(lstStr[len(lstStr)-1], " ", "_") + ".csv"
    sql = "FolderPath = \'" + fp + "\'"
    arcpy.MakeTableView_management(ds, r"in_memory\vw", sql)
    if os.path.exists(folder + os.path.sep + fn):
        os.remove(folder + os.path.sep + fn)
    f = folder + os.path.sep + fn
    #print f
    fs = open( f, 'w')
    fs.write("FolderPath,Name,Longitude,Latitude\n")
    recs = arcpy.SearchCursor(r"in_memory\vw")
    rec = recs.next()
    ts = 0
    while rec:
        fs.write(str(rec.FolderPath) + ',' + str(rec.Name) + ',' + str(rec.Longitude) + ',' + str(rec.Latitude) + '\n')
        ts += 1
        rec = recs.next()
    fs.close()
    lstStr = string.split(f,'\\')
    #todo: add f to archive
    zf.write(f, lstStr[len(lstStr)-1])
    os.remove(f) #remove f
    del fs #cleanup
    del rec #cleanup
    del recs #cleanup
    #print fn
    arcpy.Delete_management(r"in_memory\vw")

#print n
zf.close()

#todo: cleanup
print 'cleaning Up'
arcpy.Delete_management(gdb)

#complete
print '\ndone'



