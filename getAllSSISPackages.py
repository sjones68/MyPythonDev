#getAllSSISPackages.py

#import Modules
import os, string

#banner
print '***\nFetch SSIS Packages\n****'

csvFile = r'd:\tmp\ssisPackagesEDW.csv'
folder = r'\\atalsdbp01\DW'

#open the File for writing
fs = open(csvFile, 'w')
fs.write("FileNo,FileName\n")

#initialise the variables
n = 0
s = 0

#cycle through the 
for subdir, dirs, files in os.walk(folder):
    #cycle Through the list of files
    for f in files:
        #ssis Packages
        if string.find(f, '.dtsx') > -1:
            n += 1
            fs.write(str(n) + "," + subdir + os.path.sep + f + "\n")
            print(subdir + os.path.sep + f)
        #solutions Packages
        if string.find(f, '.sln') > -1:
            s += 1         
fs.close()

#status
print str(s) + '\tsolutions'
print str(n) + '\tssis packages'

#completed
print 'completed'
