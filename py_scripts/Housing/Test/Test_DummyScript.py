import sys
import os
sys.path.append(os.getcwd())


from seatable_api import Base, context
import utils.DummyScript as ds
from utils.DummyScript import HostDatabase as Hosts
from utils.DummyScript import RefugeeDatabase as Refugees
from utils.DummyScript import TableDef, ViewDef

def initBase():
    server_url = context.server_url or 'https://cloud.seatable.io'
    api_token = context.api_token or 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkdGFibGVfdXVpZCI6IjljNDNhNTU4LWIzNmEtNGMyMy1iM2Y0LTQ0MThmMDRkY2QwZSIsImFwcF9uYW1lIjoiNzdXcC5weSIsImV4cCI6MTY0OTYxODQwNn0.CspygVRHeRt2ivLDpCLRdK4wp4e8WlIc2Q3oxCYptzo'
    base = Base(api_token, server_url)
    base.auth()
    return base
    

if __name__ == "__main__":
    base = initBase()
    hosts = Hosts(base)
    refugees = Refugees(base)
    
    print("******** Hosts Test **************")

    hosts.appendRow(hosts.getDefEntry())
    print("All Rows: \n")
    print(hosts.getAllRows())
    print ("\n")
    print("All Rows of View: \n")
    print(hosts.getAllRowsOfView(ViewDef.SIMPLEMATCHING))
    print("\n")
    genId = "H-000001"
    rowId = hosts.getRowIdOfGenId(genId)
    print("Get Row By Gen Id " + genId +": " + rowId)
    genId = hosts.getGenIdOfRowId(rowId)
    print("Get Gen Id by Row Id " + rowId +": " + genId)
    hosts.updateTimeStamp("Date",rowId)
    print("Diff after update is " + genId + " is: " + str(hosts.getTimeDiff("Date", rowId)))
    rows_data = (hosts.getAllRowsOfView("Simple View"))
    hosts.batchUpdate(rows_data)
    print("All Rows after Batch Update: \n")
    print(hosts.getAllRows()) 
    
    print("******** Refugee Test **************")
    
    refugees.appendRow(refugees.getDefEntry())
    print("All Rows: \n")
    print(refugees.getAllRows())
    print ("\n")
    print("All Rows of View: \n")
    print(refugees.getAllRowsOfView((ViewDef.SIMPLEMATCHING))
    print("\n")
    genId = "R-000002"
    rowId = refugees.getRowIdOfGenId(genId)
    print("Get Row By Gen Id " + genId +": " + rowId)
    genId = refugees.getGenIdOfRowId(rowId)
    print("Get Gen Id by Row Id " + rowId +": " + genId)
    refugees.updateTimeStamp("Date",rowId)
    print("Diff after update is " + genId + " is: " + str(refugees.getTimeDiff("Date", rowId)))
    rows_data = (refugees.getAllRowsOfView((ViewDef.SIMPLEMATCHING))
    refugees.batchUpdate(rows_data)
    print("All Rows after Batch Update: \n")
    print(refugees.getAllRows()) 
    
    
    
    
    
    
    
    
