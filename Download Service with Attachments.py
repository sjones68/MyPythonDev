import arcpy, urllib, urllib2, json, os, math, sys, linecache

# Check if ArcGIS for Desktop Standard license is available
getAttachments = arcpy.GetParameterAsText(8)
if getAttachments == 'true':
    try:
        import arceditor
    except:
        msg = 'ArcGIS for Desktop Standarad license is required to extract attachments'
        arcpy.AddError(msg)
        sys.exit()

# Function to handle errors
def PrintException(error):
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    arcpy.AddError(error + ':  FILE: {}, LINE: {} \n\t "{}": {}'.format(filename, lineno, line.strip(), exc_obj))
    sys.exit()

from arcpy import env
env.overwriteOutput = 1
env.workspace = env.scratchGDB

hostedFeatureService = arcpy.GetParameterAsText(0)
agsService = arcpy.GetParameterAsText(1)

baseURL = arcpy.GetParameterAsText(2) + "/query"

agsFeatures = arcpy.GetParameterAsText(3)
agsTable = arcpy.GetParameterAsText(4)

username = arcpy.GetParameterAsText(5)
password = arcpy.GetParameterAsText(6)

# Generate token for hosted feature service
if hostedFeatureService == 'true':
    try:
        arcpy.AddMessage('\nGenerating Token\n')
        tokenURL = 'https://www.arcgis.com/sharing/rest/generateToken'
        params = {'f': 'pjson', 'username': username, 'password': password, 'referer': 'http://www.arcgis.com'}
        req = urllib2.Request(tokenURL, urllib.urlencode(params))
        response = urllib2.urlopen(req)
        data = json.load(response)
        token = data['token']
    except:
        token = ''

# Genereate token for AGS feature service
if agsService == 'true':
    try:
        arcpy.AddMessage('\nGenerating Token\n')
        server = baseURL.split("//")[1].split("/")[0]
        tokenURL = 'http://' + server + '/arcgis/admin/generateToken'
        params = {'username': username, 'password': password, 'client': 'requestip', 'f': 'pjson'}
        req = urllib2.Request(tokenURL, urllib.urlencode(params))
        response = urllib2.urlopen(req)
        data = json.load(response)
        token = data['token']
    except:
        token = ''
        pass

# Return largest ObjectID
params = {'where': '1=1', 'returnIdsOnly': 'true', 'token': token, 'f': 'json'}
req = urllib2.Request(baseURL, urllib.urlencode(params))
response = urllib2.urlopen(req)
data = json.load(response)
try:
    data['objectIds'].sort()
except:
    arcpy.AddError("\nURL is incorrect.  Or, Service is secure, please enter username and password.\n")
    sys.exit()

count = len(data['objectIds'])
iteration = int(data['objectIds'][-1])
minOID = int(data['objectIds'][0]) - 1
OID = data['objectIdFieldName']

# Check to see if downloading a feature or tabular data
if agsFeatures != 'true' and agsTable != 'true':
    arcpy.AddError("\nPlease check 'Downloading Feature Data' or 'Downloading Tabular Data'\n")
    sys.exit()

# Code for downloading feature data
if agsFeatures == 'true':
    if count < 1000:
        x = iteration
        y = minOID
        where = OID + '>' + str(y) + 'AND ' + OID + '<=' + str(x)
        fields ='*'

        query = "?where={}&outFields={}&returnGeometry=true&f=json&token={}".format(where, fields, token)
        fsURL = baseURL + query
        fs = arcpy.FeatureSet()

        try:
            fs.load(fsURL)
        except Exception, e:
            arcpy.AddError("Error loading features: " + str(e))
            sys.exit()

        arcpy.AddMessage('Copying features with ObjectIDs from ' + str(y) + ' to ' + str(x))
        outputFC = arcpy.GetParameterAsText(7)
        desc = arcpy.Describe(os.path.dirname(outputFC))
        if desc.workspaceFactoryProgID == 'esriDataSourcesGDB.SdeWorkspaceFactory.1':
            outputFC2 = outputFC.split(".")[-1]
            try:
                arcpy.FeatureClassToFeatureClass_conversion(fs, os.path.dirname(outputFC), outputFC2)
            except:
                PrintException("Error Copying Features")
        else:
            try:
                arcpy.FeatureClassToFeatureClass_conversion(fs, os.path.dirname(outputFC), os.path.basename(outputFC))
            except:
                PrintException("Error Copying Features")



    else:
        newIteration = (math.ceil(iteration/1000.0) * 1000)
        x = minOID + 1000
        y = minOID
        firstTime = 'True'

        while y <= newIteration:
            where = OID + '>' + str(y) + 'AND ' + OID + '<=' + str(x)
            fields ='*'

            query = "?where={}&outFields={}&returnGeometry=true&f=json&token={}".format(where, fields, token)
            fsURL = baseURL + query

            fs = arcpy.FeatureSet()

            try:
                fs.load(fsURL)

                if firstTime == 'True':
                    arcpy.AddMessage('Copying features with ObjectIDs from ' + str(y) + ' to ' + str(x))
                    outputFC = arcpy.GetParameterAsText(7)
                    desc = arcpy.Describe(os.path.dirname(outputFC))
                    if desc.workspaceFactoryProgID == 'esriDataSourcesGDB.SdeWorkspaceFactory.1':
                        outputFC2 = outputFC.split(".")[-1]
                        try:
                            arcpy.FeatureClassToFeatureClass_conversion(fs, os.path.dirname(outputFC), outputFC2)
                        except:
                            PrintException("Error Copying Features")
                    else:
                        try:
                            arcpy.FeatureClassToFeatureClass_conversion(fs, os.path.dirname(outputFC), os.path.basename(outputFC))
                        except:
                            PrintException("Error Copying Features")
                            sys.exit()
                    firstTime = 'False'
                else:
                    desc = arcpy.Describe(os.path.dirname(outputFC))
                    if desc.workspaceFactoryProgID == 'esriDataSourcesGDB.SdeWorkspaceFactory.1':
                        arcpy.AddMessage('Copying features with ObjectIDs from ' + str(y) + ' to ' + str(x))
                        insertRows = arcpy.da.InsertCursor(outputFC, ["*","SHAPE@"])
                        searchRows = arcpy.da.SearchCursor(fs, ["*","SHAPE@"])
                        for searchRow in searchRows:
                            fieldList = list(searchRow)
                            insertRows.insertRow(fieldList)
                    elif desc.workspaceFactoryProgID == '':
                        arcpy.AddMessage('Copying features with ObjectIDs from ' + str(y) + ' to ' + str(x))
                        try:
                            arcpy.Append_management(fs, outputFC, "NO_TEST")
                        except:
                            PrintException("Error Copying Features")
                    else:
                        arcpy.AddMessage('Copying features with ObjectIDs from ' + str(y) + ' to ' + str(x))
                        try:
                            arcpy.Append_management(fs, outputFC)
                        except:
                            PrintException("Error Copying Features")
            except:
                pass

            x += 1000
            y += 1000

    try:
        del searchRow, searchRows, insertRows
    except:
        pass

# Code for downloading tabular data
if agsTable == 'true':
    if count < 1000:
        x = iteration
        y = minOID
        where = OID + '>' + str(y) + 'AND ' + OID + '<=' + str(x)
        fields ='*'

        query = "?where={}&outFields={}&returnGeometry=true&f=json&token={}".format(where, fields, token)
        fsURL = baseURL + query

        fs = arcpy.RecordSet()
        try:
            fs.load(fsURL)
        except:
            PrintException("Error Loading Features")

        arcpy.AddMessage('Copying features with ObjectIDs from ' + str(y) + ' to ' + str(x))
        outputFC = arcpy.GetParameterAsText(7)
        desc = arcpy.Describe(os.path.dirname(outputFC))
        if desc.workspaceFactoryProgID == 'esriDataSourcesGDB.SdeWorkspaceFactory.1':
            outputFC2 = outputFC.split(".")[-1]
            try:
                arcpy.TableToTable_conversion(fs, os.path.dirname(outputFC), outputFC2)
            except:
                PrintException("Error Copying Features")
        else:
            try:
                arcpy.TableToTable_conversion(fs, os.path.dirname(outputFC), os.path.basename(outputFC))
            except:
                PrintException("Error Copying Features")

    else:
        newIteration = (math.ceil(iteration/1000.0) * 1000)
        x = minOID + 1000
        y = minOID
        firstTime = 'True'

        while y <= newIteration:
            where = OID + '>' + str(y) + 'AND ' + OID + '<=' + str(x)
            fields ='*'

            query = "?where={}&outFields={}&f=json&token={}".format(where, fields, token)
            fsURL = baseURL + query

            fs = arcpy.RecordSet()

            try:
                fs.load(fsURL)

                if firstTime == 'True':
                    arcpy.AddMessage('Copying features with ObjectIDs from ' + str(y) + ' to ' + str(x))
                    outputFC = arcpy.GetParameterAsText(7)
                    desc = arcpy.Describe(os.path.dirname(outputFC))
                    if desc.workspaceFactoryProgID == 'esriDataSourcesGDB.SdeWorkspaceFactory.1':
                        outputFC2 = outputFC.split(".")[-1]
                        try:
                            arcpy.TableToTable_conversion(fs, os.path.dirname(outputFC), outputFC2)
                        except:
                            PrintException("Error Copying Features")
                    else:
                        try:
                            arcpy.TableToTable_conversion(fs, os.path.dirname(outputFC), os.path.basename(outputFC))
                        except:
                            PrintException("Error Copying Features")
                    firstTime = 'False'
                else:
                    desc = arcpy.Describe(os.path.dirname(outputFC))
                    arcpy.AddMessage('Copying features with ObjectIDs from ' + str(y) + ' to ' + str(x))
                    try:
                        arcpy.Append_management(fs, outputFC)
                    except:
                        PrintException("Error Copying Features")
            except:
                pass

            x += 1000
            y += 1000

    try:
        del searchRow, searchRows, insertRows
    except:
        pass

# Code for retrieving attachments
if getAttachments == 'true':
    # Create Replica to retrieve attachments
    arcpy.AddMessage("\nRetrieving Attachments\n")
    cwd = arcpy.GetParameterAsText(9)
    crUrl = baseURL[0:-7] + 'createReplica'
    crValues = {'f' : 'json',
    'layers' : '0',
    'returnAttachments' : 'true',
    'supportsAttachmentsSyncDirection': 'bidirectional',
    'token' : token }
    crData = urllib.urlencode(crValues)
    crRequest = urllib2.Request(crUrl, crData)
    crResponse = urllib2.urlopen(crRequest)
    crJson = json.load(crResponse)
    try:
        crJson['URL'] = 'https:' + crJson['URL'].split(":")[-1]
        replicaUrl = crJson['URL'] + '?token=' + token
    except Exception, e:
        ##PrintException(str(e))
        arcpy.AddWarning("\nService does not have 'Sync' operation enabled\n")
        sys.exit()
    urllib.urlretrieve(replicaUrl, cwd + os.sep + 'myLayer.json')

    f = open(cwd + os.sep + 'myLayer.json')
    lines = f.readlines()
    f.close()

    for line in lines:
        if not 'attachments' in line:
            arcpy.AddWarning("\nService does not contain attachments\n")
            sys.exit()
            os.remove(cwd + os.sep + 'myLayer.json')
            sys.exit()

    # Get Attachment
    with open(cwd + os.sep + 'myLayer.json') as data_file:
        data = json.load(data_file)

    dict = {}
    x = 0
    while x <= count:
        try:
            dict[data['layers'][0]['features'][x]['attributes'][OID]] = data['layers'][0]['features'][x]['attributes']['GlobalID']
            x += 1
        except KeyError:
            dict[data['layers'][0]['features'][x]['attributes'][OID]] = data['layers'][0]['features'][x]['attributes']['GLOBALID']
            x += 1
        except IndexError:
            x += 1
            pass

    fc = arcpy.GetParameterAsText(7)
    try:
        arcpy.AddField_management(fc, "GlobalID_Str", "TEXT")
    except:
        PrintException("Error Adding Field")

    dictList = list(dict.keys())
    dictList.sort()

    x = 1
    y = 0
    while x <= count:
        with arcpy.da.UpdateCursor(fc, ["OID@", "GlobalID_Str"], "OBJECTID = " + str(x)) as cursor:
            for row in cursor:
                row[1] = dict[dictList[y]]
                cursor.updateRow(row)
        x += 1
        y += 1

    try:
        arcpy.EnableAttachments_management(fc)
    except:
        PrintException("Error Adding Attachments")
    try:
        arcpy.AddField_management(fc + "__ATTACH", "GlobalID_Str", "TEXT")
        arcpy.AddField_management(fc + "__ATTACH", "PhotoPath", "TEXT")
    except:
        PrintException("Error Adding Field")

    # Add Attachments
    # Create Match Table
    try:
        for x in data['layers'][0]['attachments']:
            gaUrl = x['url']
            gaFolder = cwd + os.sep + x['parentGlobalId']
            if not os.path.exists(gaFolder):
                os.makedirs(gaFolder)
            gaName = x['name']
            gaValues = {'token' : token }
            gaData = urllib.urlencode(gaValues)
            try:
                urllib.urlretrieve(url=gaUrl + '/' + gaName, filename=os.path.join(gaFolder, gaName),data=gaData)
            except:
                PrintException("Error Retrieving Attachments")

        rows = arcpy.da.InsertCursor(fc + "__ATTACH", ["GlobalID_Str", "PhotoPath"])
        hasrow = False
        for cmtX in data['layers'][0]['attachments']:
            rows.insertRow((cmtX['parentGlobalId'], cwd + os.sep +cmtX['parentGlobalId'] + os.sep + cmtX['name']))
            hasrow = True

        if hasrow == True:
            del rows
            try:
                arcpy.AddAttachments_management(fc, 'GlobalID_Str', fc + '__ATTACH', 'GlobalID_Str', 'PhotoPath')
            except:
                PrintException("Error Retrieving Attachments")

        try:
            arcpy.MakeTableView_management(fc + '__ATTACH', "tblView")
            arcpy.SelectLayerByAttribute_management("tblView", "NEW_SELECTION", "DATA_SIZE = 0")
            arcpy.DeleteRows_management("tblView")
            arcpy.DeleteField_management(fc + '__ATTACH', 'GlobalID_Str')
            arcpy.DeleteField_management(fc + '__ATTACH', 'PhotoPath')
        except Exception, e:
            arcpy.AddWarning("Error: " + str(e))
            pass
    except KeyError:
        pass

    os.remove(cwd + os.sep + 'myLayer.json')


