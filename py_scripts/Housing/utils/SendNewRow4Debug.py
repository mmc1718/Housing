from pickle import NONE
from seatable_api import Base, context
from seatable_api.date_utils import dateutils
import json
from seatable_api.constants import UPDATE_DTABLE

# Constants of Table Names
class TableDef:
    HOST = "Hosts"
    VOLUNTEERS = "Volunteers"
    REFUGEES = "Refugees"

# Constants of View Names
class ViewDef:
    DEFAULT = "Default View"
    SIMPLEMATCHING = "Simple Matching"

# Parent Class/ Library of a Seatable Table that provides common getter and setter functions for more convient scripting
class Database:
    def __init__(self, base=Base, tableName=str):
        self._base      = base # the base of that table
        self._tableName = tableName # The table name as string
        self._dummyRow = {} # A default entry can be used inital declaration of a row or for debugging proposes.
        self._columns = self._base.list_columns(self._tableName, ViewDef.DEFAULT)
        # Getting meta data to get the table name and id
        listOfTables = self._base.get_metadata().get('tables') 
        for t in listOfTables:
            if t['name'] == tableName:
                self._tableID= t['_id']
                break
            
    # Used to init of dummy Row. A default entry can be used inital declaration of a row or for debugging proposes.
    # #param     row    A dict with column names as keys and their dummy/default values          
    def setDummyRow(self, row):
        self._dummyRow =  row 
        
    # Get dummy/ default row
    # Returns dict of row  
    def getDummyRow(self):
        return self._dummyRow
    
    # Gets all rows of a table 
    # #return List of row dicts
    def getAllRows(self):
        rows = self._base.list_rows(self._tableName, view_name=None, order_by=None, desc=False, start=None, limit=None) 
        if len(rows)>0:
            return rows
        else:
            print(self.getAllRows.__name__ + " Table does not exist")
            return {}
        
    # Gets all  rows in a table view 
    # #param   viewName     String of view name or its related const of defView class
    # #return List of row dicts
    def getAllRowsOfView(self, viewName):
        rows = self._base.list_rows(self._tableName, view_name=viewName, order_by=None, desc=False, start=None, limit=None) 
        if len(rows)>0:
            return rows
        else:
            print(self.getAllRowsOfView.__name__ + " View does not exist") 
            return {}
        
    # Appends a new row to table
    # #param   row_data     A single line dict with column names as keys and their dummy/default values
    def appendRow(self, row_data):
        self._base.append_row(self._tableName, row_data)
    
    # Gets row by generated ID (H-0000001, R-000004 or similar)
    # #param   id    Generated ID (H-0000001, R-000004 or similar)
    # #returns dict of row 
    def getRowByGenId(self, id):
        rows = self.getAllRows()
        for r in rows:
            if r.get('ID')==id:
                return r
        print(self.getRowByGenId.__name__ + " Gen ID does not exist") 
        return {}
    
    # Gets row id of a generated ID (H-0000001, R-000004 or similar)
    # #param   id    Generated ID (H-0000001, R-000004 or similar)
    # #returns seatable id of the row
    def getRowIdOfGenId(self, genID):
        row = self.getRowByGenId(genID)
        if '_id' in row.keys():          
            return row['_id']
        else:
            print(self.getRowIdOfGenId.__name__ + " Row ID does not exist")  
            return "ID Not Existing"
     
    # Returns generated id (H-0000001, R-000004 or similar) of row ID 
    # #param   id    seatable row id
    def getGenIdOfRowId(self, id):
        row = self.getRowByRowId(id)
        if 'ID' in row.keys():          
            return row['ID'] 
        else:
            return "ID Not Existing"
    
    
    # Returns single line dict of a seatable row id 
    # #param   id    seatable row id
    def getRowByRowId(self, id):
        row = self._base.get_row(self._tableName, id)
        if len(row)>0:
            return row
        else:
            print(self.getRowByRowId.__name__ + " Row does not exist") 
            return {}
        
    # Updates muliple rows at once
    # #param   rows_data    list of single line row dicts
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
            print(self.batchUpdate.__name__ +" Batch Update got empty row_data")
            
    # Sets cell value and updates it in database
    # #param   id       seatable row id
    # #param   columnName   column name as string
    # #param   value    value to be set
              
    def setRowCellValue(self, Id, columnName, value, datatype = "text"):
        if self.isColumnOfType(columnName, datatype):
            row = self._base.get_row(self._tableName,Id)
            if len(row)>0:
                row[columnName] = value
                self._base.update_row(self._tableName, Id, row) 
            else:
                print(self.setRowCellValue.__name__ + " Row does not exist")
        else: 
            print(self.setRowCellValue.__name__ + " Column is not of datatype")
        
    # Checks if column is of a specific type for sanity checks
    # #param columnName  Name of column as string
    # #param datatype   Name of datatype as string
    # #returns true if column is of type
    def isColumnOfType(self, columnName, datatype=''):
        for c in self._columns:
            if c['name'] == columnName and c['type'] == datatype:
                return True
        return False
            
    # Sets cell value and updates it in database
    # #param   id       seatable row id
    # #param   column   column name as string
    # #param   value    value to be set                            
    def setDateToNow(self, columnName, Id):
        if self.isColumnOfType(columnName, 'date'):
            row = self._base.get_row(self._tableName,Id)
            if len(row)>0:
                row[columnName]= dateutils.now()
                self._base.update_row(self._tableName, Id, row)                
            else:
                print(self.setDateToNow.__name__ + " Row does not exist")
        else:
            print(self.setDateToNow.__name__ + " Cell is not of type Date")

    # Sets cell value and updates it in database
    # #param   Id       seatable row id
    # #param   columnName   column name as string
    # #param   unit    unit of the time diff. 'H' = Hours, is default, 'S' = Seconds, 'D' = Days, 'M' = Months
    # #returns time difference in parsed unit                  
    def getTimeDiff(self, columnName, Id, unit='H'):
        if self.isColumnOfType(columnName, 'date'):   
            row = self._base.get_row(self._tableName,Id)
            if len(row)>0:
                dt = dateutils.datediff(row[columnName], dateutils.now(), unit)
                return dt
            else:
                print(self.setDateToNow.__name__ + " Cell is not of type Date")
        return NONE
    # Gets the latest added row of table
    # # returns dict of row    
    def getLatestAddedRow(self):   
        q = 'SELECT * FROM ' + self._tableName + ' ORDER BY _ctime DESC'           
        rows = self._base.query(q)
        return rows[0]
    
    # Gets the latest modified row of table
    # # returns dict of row
    def getLatestUpdatedRow(self):
        q = 'SELECT * FROM ' + self._tableName + ' ORDER BY _mtime DESC'           
        rows = self._base.query(q)
        return rows[0]
        

    
    
# This is a class for a Host Table which is a child of Database. Add here functions and members that are specific for the Host usecases
class HostDatabase(Database):
    def __init__(self, base=Base):
        super().__init__(base, TableDef.HOST)
        super().setDummyRow({  
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

# This is a class for a Refugee Table which is a child of Database. Add here functions and members that are specific for the Refugee usecases    
class RefugeeDatabase(Database):
    def __init__(self, base=Base):
        super().__init__(base, TableDef.REFUGEES)
        super().setDummyRow({    
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


 
def initStaticBase():
    server_url = context.server_url or 'https://cloud.seatable.io'
    api_token = context.api_token or 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkdGFibGVfdXVpZCI6IjljNDNhNTU4LWIzNmEtNGMyMy1iM2Y0LTQ0MThmMDRkY2QwZSIsImFwcF9uYW1lIjoiNzdXcC5weSIsImV4cCI6MTY0OTk2MjAxOX0.rS0R9-wiSSd1Az5VHWYDS6zwLVVKoAzTt0QVxBsCRGE'
    base = Base(api_token, server_url)
    base.auth(with_socket_io=False)
    hosts = HostDatabase(base)
    refugees = RefugeeDatabase(base)
    return hosts, refugees      

def initSocketIOBase():
    server_url = context.server_url or 'https://cloud.seatable.io'
    api_token = context.api_token or 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkdGFibGVfdXVpZCI6IjljNDNhNTU4LWIzNmEtNGMyMy1iM2Y0LTQ0MThmMDRkY2QwZSIsImFwcF9uYW1lIjoiNzdXcC5weSIsImV4cCI6MTY0OTk2MjAxOX0.rS0R9-wiSSd1Az5VHWYDS6zwLVVKoAzTt0QVxBsCRGE'
    base = Base(api_token, server_url)
    base.auth(with_socket_io= True)
    hosts = HostDatabase(base)
    refugees = RefugeeDatabase(base)
    return hosts, refugees    

#ENUM of DebugMode. Needed for Template Handling
class DebugMode:
    ### Use this when working in your IDE (PyCharm, Visual Code, ...) for debugging scripts
    STATICLOCAL = 0
    ### Use this when working in your IDE (PyCharm, Visual Code, ...) and debugging events like 'insert_row', 'update_row' locally.
    ### Note that socketIO is not working properly in Cloud. It doesn't reset event objects after function execution
    ### The Workaround is to use STATICLOCAL Mode and the datebase functions getLatestAddedRow() and getLatestUpdatedRow() instead
    EVENTBASED = 1
    ### Switch to this mode to use your script in the cloud when it shall be executed manually per Button or similar. Otherwise, it would not work!
    SEATABLECLOUD = 2

######################## Enter your Script in the run function  ##################################

def run(hosts, refugees, var=None):
    if MODE is DebugMode.EVENTBASED:
        rows = var
    elif MODE is DebugMode.STATICLOCAL:
        row = {}
    elif MODE is DebugMode.SEATABLECLOUD:
        row = {}
       
    hosts.appendRow(hosts.getDefEntry()) 

###########  Select MODE of your current development ################

MODE = DebugMode.STATICLOCAL 

############### Add your Script Above - This is template code that shall not be modified ##################################

if MODE is DebugMode.EVENTBASED:
        hosts, refugees = initSocketIOBase()
elif MODE is DebugMode.STATICLOCAL:
        hosts, refugees = initStaticBase()
        run( hosts, refugees) 
elif MODE is DebugMode.SEATABLECLOUD:
        hosts, refugees = initStaticBase()
        run( hosts, refugees)    

# this is the socketio on_event function. If a change is made in the table this function is called
# #param data row/s that are modified
# #index index of row
def on_update_seatable(data, index, *args):
    if MODE is DebugMode.EVENTBASED:
        try:
            data = json.loads(data)
        except:
            print("Something went wrong with data decode.")
            return
        
        if (data['op_type'] == 'insert_row'):
            receiver_rows  = [hosts.getRowByRowId(data['row_id'])]
            run(receiver_rows)

if MODE  is DebugMode.EVENTBASED:
    hosts._base.socketIO.on(UPDATE_DTABLE, on_update_seatable)
    hosts._base.socketIO.wait()  # forever 