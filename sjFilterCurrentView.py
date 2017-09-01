#gisFilterCurrentView.py

#import Modules
import arcpy, string, datetime

print("***\nfilter Current View\n***\n")
start = datetime.datetime.now()

#todo: set Parameters
arcpy.env.workspace = r"\\atalgisau01\ADMIN\Maintenance\connections\gisadmin@EXT@atalgissdbp01.sde"
fc = "EXT.GISADMIN.MediaSuite_MYWorksite_XR"
todaysDate = datetime.date.today()
sql = "EndDate < \'" + str(todaysDate) + "\'" #todo: select rows that are still valid
arcpy.MakeFeatureLayer_management(in_features = fc, out_layer = "worksites", where_clause = sql) #work with feature layer
fields = ["StartDate", "EndDate"]

#todo: delete non-current Worksites
##recs = arcpy.da.UpdateCursor(in_table = "worksites", field_names = fields)
##print(arcpy.GetCount_management("worksites"))
##for rec in recs: recs.deleteRow()
##del recs
arcpy.Delete_management(in_data = "worksites") #delete the feature Layer

end = datetime.datetime.now()

print("elapsed " + str(end - start))

print("\ncompleted")

