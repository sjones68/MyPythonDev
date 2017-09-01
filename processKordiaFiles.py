#processKordiaFiles.py

#proces incoming files from Kodia files to enable real time simulation

#Susan Jones
#16 September 2016

#import modules
import string, os


#todo: convert to decimal minutes
def convertDecimalMinutes(latitude, longitude):
    #latitude
    dm = float(parseFeed[11]) / 100
    deg = float(parseFeed[11][0:3])
    minutes = abs((dm - deg)) 
    seconds = ((minutes - int(minutes)) * 60) / 3600
    ddLat = deg - minutes 

    #longitude
    dm = float(parseFeed[12]) / 100
    deg = float(parseFeed[12][0:3])
    minutes = abs((dm - deg)) 
    seconds = ((minutes - int(minutes)) * 60) / 3600
    ddLong = deg + minutes

    #return
    coords = [ddLong, ddLat]
    return coords



#open File for 
inFile = r"d:\tmp\kordia\june_27_512001263__at_ab_68_001.csv"
fs = open(inFile, 'r')

print "***\nProcess Kordia Feeds\n\nSusan Jones\n16 September 2016\n***"

#fields
#0 - ATON
#1 - Class
#2 - Type of Ship
#3 - MMSI
#4 - IMO
#5 - Call Sign
#6 - Name
#7 - Destination
#8 - Electronic Fixing Devine
#9 - ETA
#10 - Max Draught
#11 - Latitude Decimal Minutes
#12 - Longitude Decimal Minutes
#13 - SOG (knots)
#14 - ROT Deg/min
#15 - COG Deg
#16 - True Heading
#17 - Navigational status
#18 - Message Type
#19 - Port
#20 - Date Time Stamp


f = fs.readline()
print f + "\n"

f = fs.readline()
f = fs.readline()
f = fs.readline()
f = fs.readline()
f = fs.readline()
f = fs.readline()

print f + "\n"
feed = string.replace(f, "\"", "")
parseFeed = string.split(feed, ",")


headerLine = "ATONtype,Classtypeofship,MMSI,IMO,CallSign,Name,Destination,EFD,ETA,MaxDraught,Latitude,Longitude,"
headerLine = headerLine + "SOG,ROT,COG,TrueHeading,NavStatus,MsgType,Port,DateTimeStamp"



#todo: parse The File
print "\nParse the file"
cnt = 0

for f in fs:

    #parse with ,
    feed = string.replace(f, "\"", "")
    parseFeed = string.split(feed, ",")

    #sort Out The coordinates
    if parseFeed[11] <> "" or parseFeed[12] <> "":
        returnXY = convertDecimalMinutes(parseFeed[11], parseFeed[12])
    else:
        returnXY = ["", ""]

    #todo: build up the new string
    orderLine = parseFeed[0] + ','
    orderLine = orderLine + parseFeed[1] + ','
    orderLine = orderLine + parseFeed[2] + ','
    orderLine = orderLine + parseFeed[3] + ','
    orderLine = orderLine + parseFeed[4] + ','
    orderLine = orderLine + parseFeed[5] + ','
    orderLine = orderLine + parseFeed[6] + ','
    orderLine = orderLine + parseFeed[7] + ','
    orderLine = orderLine + parseFeed[8] + ','
    orderLine = orderLine + parseFeed[9] + ','
    orderLine = orderLine + parseFeed[10] + ','

    orderLine = orderLine + str(returnXY[1]) + ','
    orderLine = orderLine + str(returnXY[0]) + ','
    
    orderLine = orderLine + parseFeed[13] + ','
    orderLine = orderLine + parseFeed[14] + ','
    orderLine = orderLine + parseFeed[15] + ','
    orderLine = orderLine + parseFeed[16] + ','
    orderLine = orderLine + parseFeed[17] + ','
    orderLine = orderLine + parseFeed[18] + ','
    orderLine = orderLine + parseFeed[19] + ',\n'

    print parseFeed[19]

    

    
    cnt += 1


print cnt

#cleanUp
fs.close()

print "\ncomplete"

