#formatSmartrakIntoCSV.py

#Purpose:
#Format the Smartrak json file for csv input
#read the input json -> PARSE -> output csv File

#input: d:\tmp\Smartrak_20160304.txt

#output: d:\tmp\Smartrak_20160304_out.csv

#Susan Jones
#14 September 2016

#import modules
import os, string, datetime

#banner
print "***\nPROCESS SMARTRAK GEOEVENT DATA\n\nSusan Jones\n14 September 2016\n***"

start = datetime.datetime.now()

#todo: declare Parameters
smartrakFile = r"d:\tmp\Smartrak_20160304.txt"
outFile = r"d:\tmp\Smartrak_20160304_out.csv"

#todo: header Line
print "\nheader Line"
headerLine = "vehicleId,"
headerLine = headerLine + "vehicleDescription,"
headerLine = headerLine + "timestamp,"
headerLine = headerLine + "latitude,"
headerLine = headerLine + "longitude,"
headerLine = headerLine + "heading,"
headerLine = headerLine + "speed,"
headerLine = headerLine + "gpsAccuracy,"
headerLine = headerLine + "vehicleStatus,"
headerLine = headerLine + "avlVersion,"
headerLine = headerLine + "messageId,"
headerLine = headerLine + "kilometricPoint,"
headerLine = headerLine + "pisRouteId\n"
print headerLine

#todo: prepare Input and Output files
print "\ntodo: prepare Input and Output files"
fs = open(smartrakFile, 'r')
outFs = open(outFile, 'w')

#todo: write header line
##outFs.write(headerLine)

#todo: process Input File
cnt = 0
print "\ntodo: process Input File"
for ln in fs:


    #todo: work With the json String
    idx = ln.index('[')
    test = ln[idx:]
    test = test.replace('[', '')
    test = test.replace(']', '')
    parseTest = string.split(test, ',')

    #todo: parse each line
    recLine = ''
    for t in parseTest:
        s = t.lstrip(' ')
        ix = s.index('=')

        #todo: build Up the csv Line
        if recLine == '':
            recLine = s[ix+1:]
            
        else:
            newField = s[ix+1:]
            recLine = recLine + ',' + newField

    #todo: write recLine
    outFs.write(recLine)
    cnt += 1
    
#close the file
fs.close()
outFs.close()

end = datetime.datetime.now()

print "\n" + str(cnt) + " features processed"

print "\ncompletion Time:\t" + str(end - start)

print "\ncompleted"
