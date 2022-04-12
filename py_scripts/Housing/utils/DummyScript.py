    
from pickle import NONE
from seatable_api import Base, context
from seatable_api.date_utils import dateutils

class TableDef:
    HOST = "Hosts"
    VOLUNTEERS = "Volunteers"
    REFUGEES = "Refugees"

class ViewDef:
    DEFAULT = "Default View"
    SIMPLEMATCHING = "Simple Matching"

class Database:
    def __init__(self, base=Base, tableName=str):
        self._base      = base
        self._tableName = tableName
        self._defEntry = {}
        listOfTables = self._base.get_metadata().get('tables')
        for t in listOfTables:
            if t['name'] == tableName:
                self._tableID= t['_id']        
                self._listOfViews = t['views']
                break

    def setDefEntry(self, entry):
        self._defEntry =  entry  
    def getDefEntry(self):
        return self._defEntry
    def getAllRows(self):
        rows = self._base.list_rows(self._tableName, view_name=None, order_by=None, desc=False, start=None, limit=None) 
        if len(rows)>0:
            return rows
        else:
            print(print.__name__ + " Table does not exist")
            return {}
    def getAllRowsOfView(self, viewName):
        rows = self._base.list_rows(self._tableName, view_name=viewName, order_by=None, desc=False, start=None, limit=None) 
        if len(rows)>0:
            return rows
        else:
            print(print.__name__ + " View does not exist") 
            return {}    
    def appendRow(self, row_data):
        return self._base.append_row(self._tableName, row_data)
    def getRowByGenId(self, id):
        rows = self.getAllRows()
        for r in rows:
            if r.get('ID')==id:
                return r
        print(print.__name__ + " Gen ID does not exist") 
        return {}
    def getRowIdOfGenId(self, genID):
        row = self.getRowByGenId(genID)
        if '_id' in row.keys():          
            return row['_id']
        else:
            print(print.__name__ + " Row ID does not exist")  
            return "ID Not Existing"
    def getGenIdOfRowId(self, id):
        row = self.getRowByRowId(id)
        if 'ID' in row.keys():          
            return row['ID'] 
        else:
            return "ID Not Existing"
    
    def getRowByRowId(self, id):
        row = self._base.get_row(self._tableName, id)
        if len(row)>0:
            return row
        else:
            print(print.__name__ + " Row does not exist") 
            return {}
    def batchUpdate(self, rows_data):
        if len(rows_data)>0:
            newStructure = []
            for r in rows_data:
                newEntry={'row_id':r['_id']}
                row = {}
                for key, value in r.items():
                    if key.rfind('_') == -1:
                        row.update({key:value})
                newEntry.update({'row':row })
            newStructure.append(newEntry)
            self._base.batch_update_rows(self._tableName, newStructure)
        else:
            print(print.__name__ +" Batch Update got empty row_data")
    def updateRowCell(self, Id, column, value):
        row = self._base.get_row(self._tableName,Id)
        if len(row)>0:
            row[column] = value
            self._base.update_row(self._tableName, Id, row) 
        else:
            print(print.__name__ + " Row does not exist")           
    def updateTimeStamp(self, columnName, Id):
        row = self._base.get_row(self._tableName,Id)
        if len(row)>0:
            row[columnName]= dateutils.now()
            self._base.update_row(self._tableName, Id, row)
        else:
            print(print.__name__ + " Row does not exist")
    def getTimeDiff(self, columnName, Id, unit='H'):
        row = self._base.get_row(self._tableName,Id)
        if len(row)>0:
            dt = dateutils.datediff(row[columnName], dateutils.now(), unit)
            return dt
        else: return NONE
    
    

class HostDatabase(Database):
    def __init__(self, base=Base):
        super().__init__(base, TableDef.HOST)
        super().setDefEntry({  
                    "Status":   "Open",           
                    "Name":     "Johnny Doe",
                    "Telefon":  "12345678",
                    "Email":    "johnny@doe.de",
                    "Date":     dateutils.date(2022, 1, 1),
                    "Adresse":  "Seaview Road 100",
                    "City":     "Hintertupfingen",
                    "Max. Number Guests":  1,
                    "Duration": "Up to 3 Months",
                    "Accomodation Type": "Shared Room",
                    "Welcoming":    ["Dogs", "Cats", "Babys", "Females"]})
    
class RefugeeDatabase(Database):
    def __init__(self, base=Base):
        super().__init__(base, TableDef.REFUGEES)
        super().setDefEntry({    
                    "Status":   "Open",           
                    "Name":     "Jimmy Doe",
                    "Telefon":  "12345678",
                    "Email":    "johnny@doe.de",
                    "Date":     dateutils.date(2022, 1, 1),
                    "Adresse":  "Seaview Road 100",
                    "City":     "Hintertupfingen",
                    "N People":  1,
                    "Duration": "Up to 3 Months",
                    "Accomodation Type": "Shared Room",
                    "Short Description":  ["Mom with Kids", "Cat/s", "Baby/s"]})
    
class HostingBase:
    def __init__(self, base=Base):
        self._base = base
        self._hosts = HostDatabase(base,TableDef.HOST)
        self._refugees = RefugeeDatabase(base,TableDef.REFUGEES)
 
def initBase():
    server_url = context.server_url or 'https://cloud.seatable.io'
    api_token = context.api_token or 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkdGFibGVfdXVpZCI6IjljNDNhNTU4LWIzNmEtNGMyMy1iM2Y0LTQ0MThmMDRkY2QwZSIsImFwcF9uYW1lIjoiNzdXcC5weSIsImV4cCI6MTY0OTYxODQwNn0.CspygVRHeRt2ivLDpCLRdK4wp4e8WlIc2Q3oxCYptzo'
    base = Base(api_token, server_url)
    base.auth(with_socket_io=False)
    return base        
        
base = initBase()
hosts = HostDatabase(base)
refugees = RefugeeDatabase(base)

 ############### Add your Script below - Above is just the library ##################################
