########### Python 2.7 #############
import httplib, urllib, base64

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': 'b4d1ffe16a62475699e0f4907068b7ac',
}

params = urllib.urlencode({
    # Request parameters
    'callback': '{string}',
})

try:
    conn = httplib.HTTPSConnection('api.at.govt.nz')
    conn.request("GET", "/v2/gtfs/routes/geosearch?lat={lat}&lng={lng}&distance={distance}&%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################

########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': 'b4d1ffe16a62475699e0f4907068b7ac',
}

params = urllib.parse.urlencode({
    # Request parameters
    'callback': '{string}',
})

try:
    conn = http.client.HTTPSConnection('api.at.govt.nz')
    conn.request("GET", "/v2/gtfs/routes/geosearch?lat={lat}&lng={lng}&distance={distance}&%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################
