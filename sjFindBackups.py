#sjFindBackups.py

#purpose - find all backups across a server and create an Inventory

import string, os, sys, datetime


#def purpose:  list backup files
def list_backup_Files(dirs):
    for dir in dirs:
        r = []
        rws = "BACKUP_PATH,DAY_OF_WEEK,CREATED,BACKUP_DURATION\n"
        #walk
        for subdir, dirs, files in os.walk(dir):
            files = os.walk(subdir).next()[2]
            for f in files:
                if f.find(".bak") > 0:
                    fl =  subdir + os.path.sep + f
                    created = datetime.datetime.fromtimestamp(os.path.getctime(fl))
                    modified = datetime.datetime.fromtimestamp(os.path.getmtime(fl))

                    ##Check if backup day is Saturday, Sunday and within 7 days
                    if created.strftime('%A') in ['Saturday', 'Sunday', 'Monday'] and created > datetime.datetime.today() - datetime.timedelta(days = 7):
                        rws = rws + fl + ',' + str(created.strftime('%A')) + ',' + str(created) + "," + str(modified - created) + "\n"
                        print fl

    #return Result
    return rws


#file for Writing
def writeFile(fl, rows):
    if os.path.exists(fl):
        os.remove(fl)
    fs = open(fl, "w")
    fs.write(str(rows))
    fs.close()
            

#banner
print "sjFindBackups\nCreate an inventory of Backups"


#todo: set Parameters
BACKUP_LOCS = []
folder = r"D:\TMP\csvFiles"

#walk through Backup Locations
print "walk through BKP_BI_PRD_01..."
BACKUP_LOCS = []
BACKUP_LOCS.append(r"\\ataihpssp01\BKP_BI_PRD_01")
rows = list_backup_Files(BACKUP_LOCS)
writeFile(folder + os.path.sep + "BKP_BI_PRD_01.csv", rows)

print "walk through AT_SQL_BACKUP..."
BACKUP_LOCS = []
BACKUP_LOCS.append(r"\\ataihpssp01\AT_SQL_BACKUP")
rows = list_backup_Files(BACKUP_LOCS)
writeFile(folder + os.path.sep + "AT_SQL_BACKUP.csv", rows)

print "walk through BKP_SAP_PRD_01..."
BACKUP_LOCS = []
BACKUP_LOCS.append(r"\\ataihpssp01\BKP_SAP_PRD_01")
rows = list_backup_Files(BACKUP_LOCS)
writeFile(folder + os.path.sep + "BKP_SAP_PRD_01.csv", rows)

print "walk through BKP_SAP_DEV_01..."
BACKUP_LOCS = []
BACKUP_LOCS.append(r"\\ataihpssp01\BKP_SAP_DEV_01")
rows = list_backup_Files(BACKUP_LOCS)
writeFile(folder + os.path.sep + "BKP_SAP_DEV_01.csv", rows)

#banner 
print "Completed"
