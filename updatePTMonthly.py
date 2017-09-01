#updatePTMonthly.py

print "***\nRun Monthly Public Transport Transaction Reports for Luke\n***"

import string, os
from datetime import datetime, timedelta, time

#todo: executiables
fme = "\"C:\\Program Files\\FME\\fme.exe\""
package = r"\\atalgisau01\PROJECTS\AT14\AT14043\Scripts\HOPHeatMaps1_DW_DataExtract_16052016.fmw"
#package = r"\\atalgisau01\PROJECTS\AT14\AT14043\Scripts\HOPHeatMaps3_CreateStationPoints_16052016.fmw"
package = r"\\atalgisau01\PROJECTS\AT14\AT14043\Scripts\HOPHeatMaps4_SummariseByCAU_16052016.fmw"


#todo: build up the datetime object of last month
hours = 24*30*-1
monthAgo = str(datetime.today() + timedelta(hours=hours))
yr = monthAgo[0:4]
mnth = monthAgo[5:7]
timePeriod = yr + "/" + mnth

#todo: excute an fme package - process CAU
start = datetime.today()
executeString = fme + " " + package + "  --varTimePeriod " + timePeriod
print executeString
os.system(executeString)
end = datetime.today()
print  end - start


#todo: excute an fme package - process GRID
package = r"\\atalgisau01\PROJECTS\AT14\AT14043\Scripts\HOPHeatMaps5_SummariseByGRID_16052016.fmw"
start = datetime.today()
executeString = fme + " " + package + "  --varTimePeriod " + timePeriod
print executeString
os.system(executeString)
end = datetime.today()
print  end - start


print "\ncompleted"
