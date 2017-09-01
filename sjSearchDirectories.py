#sjSearchDirectories.py

import os, string

#todo: import Modules


#todo: start here
print "***\nTraverse Files\n***"

filePath = "d:\\tmp\\fme_files.csv"

if os.path.exists(filePath):
    os.remove(filePath)

fs = open(filePath, "w")   

#todo: set Parameters
n = 0
folders = ["\\\\atalgisau01\\ADMIN", "\\\\atalgisau01\\Projects", "\\\\atalgisau01\\DATA"]

#todo: Set up
for folder in folders:

    walk_dir = folder

    #todo: walk
    for root, subdirs, files in os.walk(walk_dir):

        #todo: directoroy content
        for file in files:

            #todo: check for fme
            if string.find(file, "fmw") > -1:

                fs.write(root + "\\" + file + "\n")
                n += 1
                
                #todo: increment    
                if n % 100 == 0:
                    print str(n) + " Processed"
                
#todo: Notify
print str(n) + " Processed"

#todo: close the file
fs.close()
