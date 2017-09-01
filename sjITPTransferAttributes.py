#sjITPTransferAttributes.py

#import the modules
import arcpy, os, string, pyodbc, decimal

#transferProject - transfer project attributes
def transferProject(table, fields, destination, projectList, connection, data):
    #todo: 
    print("\nTransfer " + table + " to " + destination)
    fl = open("d:\\tmp\\tblProject.sql", "w")
    #todo: get a list of projects
    #projectList = string.replace(str(projectList), "[", "(").replace("]", ")")
    sql = "select distinct tpkprj from " + destination
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    #checkList
    checkList = []
    for row in rows: checkList.append(int(row[0]))
    print("Rows to Update: " + str(len(rows)))
    #todo: generate Update Statements
    fl.write("\n--Process " + destination + "\n")
    fl.write("\n--Generate Update Statements\n")
    for d in data:
        if int(d[0]) in checkList:
            sql = "UPDATE " + destination + " SET ProjectNo = \'" + str(d[1]) + "\'"  
            sql = sql + ", ProjectName = \'" + str(d[2]) + "\'" 
            sql = sql + ", ProjectDesc = \'" + str(d[3]) + "\'" 
            sql = sql + ", ProjectManager = \'" + str(d[4]) + "\'" 
            #sql = sql + ", StartDate = " + str(d[5]) 
            #sql = sql + ", EndDate = " + str(d[6]) 
            #sql = sql + ", ProjectTypeID = " + str(d[7]) 
            sql = sql + " WHERE TPKPRJ = " + str(int(d[0])) + ";"
            fl.write(sql+"\n")
            #cursor.execute(sql)
            #connection.commit()
    #todo: generate Insert Statements
    fl.write("\n--Generate Insert Statements\n")
    for d in data:
        if not int(d[0]) in checkList:
            sql = "INSERT INTO " + destination + "(TPKPRJ, ProjectNo, ProjectName, ProjectDesc, ProjectManager)"
            sql = sql +  " VALUES ( " + str(int(d[0])) + ",\'" + str(d[1]) + "\',\'" + str(d[2]) + "\',\'" + str(d[3]) + "\',\'" + str(d[4]) + "\');"
            fl.write(sql+"\n")
            #cursor.execute(sql)
            #connection.commit()
    #Cleanup
    fl.close()
    del data
    del rows
    del connection

#transferProjectFinancial - transfer project financial attributes
def transferProjectFinancial(table, fields, destination, projectList, connection, data):
    #todo: 
    print("\nTransfer " + table + " to " + destination)
    fl = open("d:\\tmp\\tblProjectFinancial.sql", "w")
    #todo: get a list of projects
    #projectList = string.replace(str(projectList), "[", "(").replace("]", ")")
    sql = "select distinct tpkprj from " + destination 
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    #checkList
    checkList = []
    for row in rows: checkList.append(int(row[0]))
    print("Rows to Update: " + str(len(rows)))
    #todo: generate Update Statements
    fl.write("\n--Generate Update Statements\n")
    for d in data:
        if int(d[0]) in checkList:
            sql = "UPDATE " + destination + " SET Amount = " + str("%.2f" % d[1])  
            sql = sql + ", VersionTypeID = " + str(d[2]) 
            sql = sql + " WHERE TPKPRJ = " + str(int(d[0])) + ";"
            fl.write(sql+"\n")
            #cursor.execute(sql)
            #connection.commit()
    #todo: generate Insert Statements
    fl.write("\n--Process " + destination + "\n")
    fl.write("\n--Generate Insert Statements\n")
    for d in data:
        if not int(d[0]) in checkList:
            sql = "INSERT INTO " + destination + "(TPKPRJ, Amount, VersionTypeID)"
            sql = sql +  " VALUES ( " + str(int(d[0])) + ",\'" + str(round(d[1],2)) + "\'," + str(d[2]) + ");"
            fl.write(sql+"\n")
            #cursor.execute(sql)
            #connection.commit()
    #Cleanup
    fl.close()
    del data
    del rows
    del connection

#transferProjectPhase - transfer project phase attributes
def transferProjectPhase(table, fields, destination, projectList, connection, data):
    #todo: 
    print("\nTransfer " + table + " to " + destination)
    fl = open("d:\\tmp\\tblProjectPhase.sql", "w")
    #todo: get a list of projects
    #projectList = string.replace(str(projectList), "[", "(").replace("]", ")")
    sql = "select distinct tpkprj from " + destination
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    #checkList
    checkList = []
    for row in rows: checkList.append(int(row[0]))
    print("Rows to Update: " + str(len(rows)))
    #todo: generate Update Statements
    fl.write("\n--Process " + destination + "\n")
    fl.write("\n--Generate Update Statements\n")
    for d in data:
        if int(d[0]) in checkList:
            sql = "UPDATE " + destination + " SET PhaseID = " + str(int(d[1])) + ""  
            sql = sql + " WHERE TPKPRJ = " + str(int(d[0])) + ";"
            fl.write(sql+"\n")
            #cursor.execute(sql)
            #connection.commit()
    #todo: generate Insert Statements
    fl.write("\n--Generate Insert Statements\n")
    for d in data:
        if not int(d[0]) in checkList:
            sql = "INSERT INTO " + destination + "(TPKPRJ, PhaseID)"
            sql = sql +  " VALUES ( " + str(int(d[0])) + "," + str(int(d[1])) + ");"
            fl.write(sql+"\n")
            #cursor.execute(sql)
            #connection.commit()
    #Cleanup
    fl.close()
    del data
    del rows
    del connection

#transferLocalBoard - transfer local board attributes
def transferLocalBoard(table, fields, destination, projectList, connection, data):
    #todo: 
    print("\nTransfer " + table + " to " + destination)
    fl = open("d:\\tmp\\tblLocalBoard.sql", "w")
    #todo: get a list of projects
    #projectList = string.replace(str(projectList), "[", "(").replace("]", ")")
    sql = "select distinct tpkprj from " + destination
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    #checkList
    checkList = []
    for row in rows: checkList.append(int(row[0]))
    print("Rows to Update: " + str(len(rows)))
    #todo: generate Update Statements
    fl.write("\n--Process " + destination + "\n")
    fl.write("\n--Generate Update Statements\n")
    for d in data:
        if int(d[0]) in checkList:
            sql = "UPDATE " + destination + " SET LocalBoardID = " + str(int(d[1])) + ""  
            sql = sql + " WHERE TPKPRJ = " + str(int(d[0])) + ";"
            fl.write(sql+"\n")
            #cursor.execute(sql)
            #connection.commit()
    #todo: generate Insert Statements
    fl.write("\n--Generate Insert Statements\n")
    for d in data:
        if not int(d[0]) in checkList:
            sql = "INSERT INTO " + destination + "(TPKPRJ, LocalBoardID)"
            sql = sql +  " VALUES ( " + str(int(d[0])) + "," + str(int(d[1])) + ");"
            fl.write(sql+"\n")
            #cursor.execute(sql)
            #connection.commit()
    #Cleanup
    fl.close()
    del data
    del rows
    del connection


#Start Here

#banner
print("***\nTransfer ITP Projects to ITP Database\n*")

#get The Existing Project Codes
cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 10.0};SERVER=ATSDBLOBAT04\SQL04A;DATABASE=ITP;Trusted_Connection=yes;')
sql = "select distinct TPKPRJ from dbo.CDD_tblProject order by TPKPRJ;"
cursor = cnxn.cursor()
cursor.execute(sql)
rows = cursor.fetchall()
tpkprjList = []
for row in rows:
    tpkprjList.append(int(row.TPKPRJ))
tpkprjList.sort()
del rows
del cursor

#parameters
xls = r'd:\tmp\MIW NST 20170309.xlsx'

print("\nTransfer records: " + xls)

#fetch The Tables
arcpy.env.workspace = xls

tables = arcpy.ListTables("*")

n = 0
for table in tables:

    #todo: exclude Erroneous Sheets
    if table.find("Sheet") == -1:


        #tblProject$
        if table == "tblProject$": 
            n += 1
            ds = []
            recs = arcpy.SearchCursor(dataset = table)
            for rec in recs:
                ds.append([rec.TPKPRJ, rec.SAP_WBS, rec.ProjectName, rec.ProejctDesc, rec.PM, rec.StartDate, rec.EndDate, rec.ProgramType])
            del recs
            transferProject(table, arcpy.ListFields(dataset = table), "dbo.CDD_tblProject", tpkprjList, cnxn, ds)
            del ds

        #tbl_ProjectFinancial$
        if table == "tbl_ProjectFinancial$": 
            n += 1
            ds = []
            recs = arcpy.SearchCursor(dataset = table)
            for rec in recs:
                ds.append([rec.TPKPRJ, decimal.Decimal(rec.Amount), int(rec.VersionTypeID)])
            del recs
            transferProjectFinancial(table, arcpy.ListFields(dataset = table), "dbo.CDD_tblProjectFinancial", tpkprjList, cnxn, ds)
            del ds

        #tbl_ProjectPhase$
        if table == "tbl_ProjectPhase$": 
            n += 1
            ds = []
            recs = arcpy.SearchCursor(dataset = table)
            for rec in recs:
                ds.append([rec.TPKPRJ, int(rec.PhaseDB)])
            del recs
            transferProjectPhase(table, arcpy.ListFields(dataset = table), "dbo.CDD_tblProjectPhase", tpkprjList, cnxn, ds)
            del ds

        #tlkpLocalBoard$
        if table == "tlkpLocalBoard$": 
            n += 1
            ds = []
            recs = arcpy.SearchCursor(dataset = table)
            for rec in recs:
                ds.append([rec.TPKPRJ, int(rec.LocalBoardID)])
            del recs
            transferLocalBoard(table, arcpy.ListFields(dataset = table), "dbo.CDD_tblProjectLocalBoard", tpkprjList, cnxn, ds)
            del ds


#report The Number of Table
print("\nTotal number of tables: " + str((n)))

#completed
print("\ncompleted")
