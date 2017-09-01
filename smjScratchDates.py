#smjScratchDates.py

#import modules
import datetime, string, os

print "***\nPublic Transport Stuff\n***"

#get current date and time
#print datetime.datetime.now() ##2016-05-18 08:28:37.071000

#get Time a month ago

pastDate = str(datetime.datetime.now() + datetime.timedelta(days = -30)) ##2016-04-18 08:35:34.039000
TimePeriod =  "\"" + pastDate[0:4] + "/" + pastDate[5:7] + "\"" ## 2016/04

script = "\\\\atalgisau01\\PROJECTS\\AT14\\AT14043\\Scripts\\HOPHeatMaps1_DW_DataExtract_16052016.fmw"
cmd = "\"C:\\Program Files\\FME\\fme.exe\" " + script + " " + TimePeriod

start = datetime.datetime.now()

#todo: run HOPHeatMaps1_DW_DataExtract_16052016.fmw
print cmd
os.system(cmd)

end = datetime.datetime.now()
print end - start

#print cmd

print "\nCompleted"
