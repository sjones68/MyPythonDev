#scheduledTasks.py

#import Modules
from xml.dom import minidom

#banner
print "***\nScheduled Tasks on ATALGISAU01\n\nSusan Jones\n****"


#files
xmlFile = r"\\atalgisau01\ADMIN\Maintenance\Scheduled Tasks\ATALSGISAU01_Scheduled_Tasks.xml"
outFile = r"\\atalgisau01\ADMIN\Maintenance\Scheduled Tasks\ATALSGISAU01_Scheduled_Tasks.txt"

fs = open(outFile, 'w')
fs.write("***\nScheduled Tasks on ATALGISAU01\n\nSusan Jones\n****\n\n")

doc = minidom.parse(xmlFile)
node = doc.documentElement


#TODO: Cycle through All Jobs
jobs = doc.getElementsByTagName("Exec")
for job in jobs:

    if job.getElementsByTagName("Command"):
        command = job.getElementsByTagName("Command")[0].childNodes[0].data

    if job.getElementsByTagName("Arguments"):
        arguments = job.getElementsByTagName("Arguments")[0].childNodes[0].data

    if job.getElementsByTagName("WorkingDirectory"):
        workingdirectory = job.getElementsByTagName("WorkingDirectory")[0].childNodes[0].data

    commandString = command + " " + arguments 

    #print the Command String
    print commandString + "\n"
    fs.write(commandString + "\n\n")


#TODO: Cleanup
del doc

fs.close()

#complete
print "\ncompleted"
