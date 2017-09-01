#smjConvertSmartrakToFeatureclass.py

#purpose:
#spatialize Smartrak Data

#susan jones
#14 August 2014

#banner
print '***\nConvert Smartrak to featureclass\n***'

#import Modules
import arcpy, os, string

#parameters
gdb = r'D:\TEMP\Smartrak.gdb'
tbl = 'fact_Smartrak_GetHistoryForPeriod'
##SmartrakLongitude, SmartrakLatitude
fc = 'Smartrak'

#env
arcpy.env.workspace = gdb
arcpy.env.overwriteOutput = 1
sr = arcpy.SpatialReference(4326)

#create fc
print 'check and create ' + fc
#if arcpy.Exists(fc):
#    arcpy.Delete_management(fc)
#arcpy.CreateFeatureclass_management( out_path = gdb, out_name = fc, geometry_type = 'point', spatial_reference = sr )

#schema
print 'recreate Schema from ' + tbl
flds = arcpy.ListFields(tbl)
#for fld in flds:
#    ##print 'adding ' + fld.name + '...'
#    if not string.upper(fld.name) in ['OBJECTID']:
#        arcpy.AddField_management( in_table = fc, field_name = fld.name, field_type = fld.type, field_precision = fld.precision, field_scale = fld.scale, field_length = fld.length)

#cycle through table cursor
n = 0
print 'make Table Cursor for ' + tbl
arcpy.MakeTableView_management(in_table = tbl, out_view = 'smartrak')
recs = arcpy.SearchCursor(dataset = 'smartrak')
insrecs = arcpy.InsertCursor( dataset = fc)
n += 1
for rec in recs:
    if n % 1000 == 0:
        print str(n) + ' processed'
    pt = arcpy.Point()
    pt.x = rec.SmartrakLongitude
    pt.y = rec.SmartrakLatitude
    #array = arcpy.Array(pt)
    insrec = insrecs.newRow()
    #insrec.shape = pt
    for fld in flds:
        if not string.upper(fld.name) in ['OBJECTID']:
            insrec.setValue( fld.name, rec.getValue(fld.name))
    insrecs.insertRow(insrec)
    n += 1


#garbase collection
print 'garbage Collection ...'
del insrec
del insrecs
del recs
del pt
del array



#completed
print 'done'
