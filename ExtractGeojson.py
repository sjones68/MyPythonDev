#ExtractGeojson.py

#Extracting GeoJson Features

#import modules
import os, sys, string

print "\nExracting Geojson from a feature collection\nSusan Jones\n24th July 2014"

##Parameter Declarion
n = 0
json_input = sys.argv[1]
print 'Extracting file ' + json_input
folder = sys.argv[2]
print 'Loading features individually into ' + folder

#get base
lstinput = json_input.split('\\')
fn = lstinput[len(lstinput)-1]
lstinput = fn.split('.')
base=lstinput[0]

#Open the geojson file for reading
readf=open(json_input, 'r')
f = readf.readline()
while readf.readline():
    fs = open(folder + os.path.sep+base+str(n)+'.geojson','w')
    fs.write(f)
    f = readf.readline()
    n += 1 #next feature
    fs.close()  
readf.close()

#All Done
print 'completed'















