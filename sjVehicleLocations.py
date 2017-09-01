#sjVehicleLocations.py


#parse json from
#https://api.at.govt.nz/v1/public/realtime/vehiclelocations?api_key=e6df7e12-5258-4a90-bccf-aae12decf15e


#banner
print "***\nVehcile Locations\n****"

#import Modules
import json, datetime, time

#parameters
jsonFile = r"d:\tmp\vehiclelocations.json" #from the api
csvFile = "d:\\tmp\\vehiclelocations.csv"

#write File
vf = open(csvFile, 'w')
vf.write("VehicleID,Longtidue,Latitude,Timestamp\n")

print "\n" + jsonFile

n = 0


json_data = open(jsonFile).read()
responses = json.loads(json_data)

for response in responses["response"]["entity"]:

    vehicleId = response["vehicle"]["vehicle"]["id"]
    
    posLongitude = response["vehicle"]["position"]["longitude"]
    posLatitude = response["vehicle"]["position"]["latitude"]


    t = response["vehicle"]["timestamp"]
    timestamp = datetime.datetime.fromtimestamp(int(t)).strftime('%Y-%m-%d %H:%M:%S')


    #print Lines
##    print str(vehicleId) + "," + str(posLongitude) + "," + str(posLatitude) + "," + str(timestamp)
    vf.write(str(vehicleId) + "," + str(posLongitude) + "," + str(posLatitude) + "," + str(timestamp) + "\n")

    n += 1

vf.close()


print "\n" + str(n)


print "\ncompleted"
