#taskScheduler.py

print "***\nTask Scheduler\n***"

import xml, string, os, arcpy, datetime, re
from xml.dom.minidom import parse

#define xml Elements to pull
def parseXML(xmlTaskFile):
    argumentList=[]
    #parse File
    doc = parse(xmlTaskFile)

    #get Principal
    principal = doc.getElementsByTagName('UserId')[0].childNodes[0].data

    #get CalendarTrigger
    startTime = doc.getElementsByTagName('StartBoundary')[0].childNodes[0].data
    startTime = startTime[11:]

    #get Processes
    recs = doc.getElementsByTagName('Exec')
    for rec in recs:

        #todo: check if there are arguments and construct the cmd
        if len(rec.getElementsByTagName("Arguments")) == 1:
            ags = rec.getElementsByTagName("Arguments")[0].childNodes[0].data
        else: ags = ""
        cmd = rec.getElementsByTagName("Command")[0].childNodes[0].data

        argumentList.append([startTime, principal, cmd, ags])

    #return
    return argumentList



#todo: declare Parameters
jobList = []
xmlLocation = r"\\atalgisau01\ADMIN\Maintenance\Scheduled Tasks"
os.chdir(xmlLocation)


#work Through the shceduled jobs
wScheduled = open("TaskScheduler.csv", 'w')
fs = os.listdir(xmlLocation)
for f in fs:

    if f.find("xml") > -1:

        print f

        job = parseXML(xmlTaskFile = f)
        jobList = jobList + job

#jobs
wScheduled.write("TimeScheduled,Principal,Command,Arguement\n")
for j in jobList: wScheduled.write(str(j[0])+","+j[1]+","+j[2]+","+j[3]+"\n")


wScheduled.close()

print "\nCompleted"

