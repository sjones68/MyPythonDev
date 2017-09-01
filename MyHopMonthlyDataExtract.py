#MyHopMonthlyDataExtract.py

#Purpose:
#Extract MyHOP Month;y from the Enterprise Data Warehouse

#Tasks
#1 - Create The EDW Querie
#2 - Open up the ArcSDE Workspace for Editing
#3 - Establish the connection to the Data Warehouse
#4 - Execute the Query and Load the MyHOP Monthly Featureclass
#5 - Cleanup

#Dependency modules;
#1 - arcpy
#2 - pyodbc

#Susan Jones
#2 September 2016


#todo: import Modules
import arcpy, string, os, pyodbc, datetime

#banner
print "***\nMyHOP Monthly Data Extract\n\nSusan Jones\n8 September 2016\n***"

destinationFolder = r""

start = datetime.datetime.now()

#todo: variables
arcpy.env.overwriteOutput = 1
SERVER = "ATALSDBU01"
DB = "ARTA_DW"

#todo: 
print "\nProcess the "

sql = ""
