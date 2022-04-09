    
from seatable_api import Base, context
import datetime


_HOST_TABLE = "Hosts"
_HR_TABLE = "HR"
_REFUGEE_TABLE = "Refugees"



class HostingBase:
    def __init__(self, base=Base):
        self._base = base
    def getAllHosts(self):
        return self._base.list_rows(_HOST_TABLE, view_name=None, order_by=None, desc=False, start=None, limit=None)
    def getAllRefugees(self):
        return self._base.list_rows(_REFUGEE_TABLE, view_name=None, order_by=None, desc=False, start=None, limit=None)
    def getAllHostsOfView(self, viewName):
        return self._base.list_rows(_HOST_TABLE, view_name=viewName, order_by=None, desc=False, start=None, limit=None)
    def getAllRefugeesOfView(self, viewName):
        return self._base.list_rows(_REFUGEE_TABLE, view_name=viewName, order_by=None, desc=False, start=None, limit=None)
    def appendHost(self, row_data):
        return self._base.append_row(_HOST_TABLE, row_data)
    def appendRefugee(self, row_data):
        return self._base.append_row(_REFUGEE_TABLE, row_data)
    def getDefaultHost(self):
        return {    
                "Name":     "John Doe",
                "City":     "Hintertupfingen",
                "NGuests":  1,
                "Date":     datetime.now(),
                "Email":    "john@doe.de",
                "Phone":    "01234567890"}
    def getDefaultRefugee(self):
        return {    
                "Name":     "John Doe",
                "City":     "Hintertupfingen",
                "NGuests":  1,
                "Date":     datetime.now(),
                "Email":    "john@doe.de",
                "Phone":    "01234567890"}    
    def getHostByHostID(self, id):
        hosts = self.getAllHosts()
        for h in hosts:
            if h.get('ID')==id:
                return h
    def getRefugeeByRefugeeID(self, id):
        refs = self.getAllHosts()
        for r in refs:
            if r.get('ID')==id:
                return r
            
    def getTableIdOfHost(self, hostid):
        return self.getHostByHostID(hostid).get('row_id')
    def getTableIdOfRefugee(self, refid):
        return self.getRefugeeByRefugeeID(refid).get('row_id')            
    def getHostByTableId(self, id):
        return self._base.get_row(_HOST_TABLE, id)
    def getRefugeeByTableId(self, id):
        return self._base.get_row(_REFUGEE_TABLE, id)
    def updateHostData(self, rows_data):
        self._base.batch_update_rows(_HOST_TABLE, rows_data)
    def updateRefugeeData(self, rows_data):
        self._base.batch_update_rows(_REFUGEE_TABLE, rows_data)    
        

        
        

