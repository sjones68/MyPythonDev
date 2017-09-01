import arcpy

print 'List Installations'
for install in arcpy.ListInstallations():
    print(install)
