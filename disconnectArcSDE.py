#disconnectArcSDEProcesses.py

#Purpsoe:
#get rid of schema locking

#import Modules
import arcpy, string

#banner
print "Disconnect All AreSDE Processes"

#todo: set the parameters
gdb = r"Database Connections\sde@preprod.sde"
usernames = ['SDE']

#todo: Loop throught the current connections hitting the db
users = arcpy.ListUsers(sde_workspace = gdb)
for user in users:

    #todo: disconnect all users
    if user.Name not in usernames:
        #arcpy.DisconnectUser(sde_workspace = gdb, users = user.ID)
        print user.Name
