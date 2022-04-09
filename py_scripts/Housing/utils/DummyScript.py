    
from seatable_api import Base, context
from seatable_api.date_utils import dateutils


_HOST_TABLE = "Hosts"
_HR_TABLE = "HR"
_REFUGEE_TABLE = "Refugees"


class Database:
    def __init__(self, base=Base, tableName=str):
        self._base      = base
        self._tableName = tableName
    def getAllRows(self):
        return self._base.list_rows(self._tableName, view_name=None, order_by=None, desc=False, start=None, limit=None) 
    def getAllRowsOfView(self, viewName):
        return self._base.list_rows(self._tableName, view_name=viewName, order_by=None, desc=False, start=None, limit=None)
    def getBase(self):
        return self._base
    def appendRow(self, row_data):
        return self._base.append_row(self._tableName, row_data)
    def getRowByGeneratedID(self, id):
        rows = self.getAllRows()
        for r in rows:
            if r.get('ID')==id:
                return r
    def getTableIdofGeneratedID(self, genID):
        return self.getRowByGeneratedID(genID).get('row_id')
    def getRowByTableId(self, id):
        return self._base.get_row(self._tableName, id)
    def batchUpdate(self, rows_data):
        self._base.batch_update_rows(self._tableName, rows_data)
    #def updateTimeStamp()
    #getTimeSinceLatestDate()    
    #addLinkList
    #createLinkListAppliedFilter
    #clearLinkList 
    #appendLinkList
    #getContactData
    
    


class HostingBase:
    def __init__(self, base=Base):
        self._base = base
        self._hosts = Database(base,_HOST_TABLE)
        self._refugees = Database(base,_REFUGEE_TABLE)
        self._defHostEntry = {    
                "Name":     "John Doe",
                "City":     "Hintertupfingen",
                "NGuests":  1,
                "Date":     dateutils.date(1999, 1, 1),
                "Email":    "john@doe.de",
                "Phone":    "01234567890"}
        self._defRefugeeEntry = {    
                "Name":     "John Doe",
                "City":     "Hintertupfingen",
                "NGuests":  1,
                "Date":     dateutils.date(1999, 1, 1),
                "Email":    "john@doe.de",
                "Phone":    "01234567890"}   