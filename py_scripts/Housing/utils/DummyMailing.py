   
from pickle import NONE
from seatable_api import Base, context
from seatable_api.date_utils import dateutils


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from seatable_api.constants import UPDATE_DTABLE
import json


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
        self._refugees = RefugeeDatabase(base,TableDef.HOST)


############### Add intended Script below - Above is just the library ##################################
        
# Connect to Seatable Cloude
server_url = context.server_url or 'https://cloud.seatable.io'
api_token = context.api_token or 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkdGFibGVfdXVpZCI6IjljNDNhNTU4LWIzNmEtNGMyMy1iM2Y0LTQ0MThmMDRkY2QwZSIsImFwcF9uYW1lIjoiNzdXcC5weSIsImV4cCI6MTY0OTcxNjQ1NH0.sfBvizi8j6UotTFXZ0FRW2zd0ClVyJfGr93YX8B8oRc'
base = Base(api_token, server_url)
base.auth(with_socket_io=True)

# Get Instances of all required tables
hosts = HostDatabase(base)   

def getHMTLWithRowData(row):  
    html = """<html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {
                        background-color: #FFFFFF;
                    }
                    h3 {
                        font-family: Arial, sans-serif;
                        color: #ac0606;
                        text-align: Left;
                    }

                    h5 {
                        font-family: Arial, sans-serif;
                        color: #ac0606;
                        text-align: Left;
                    }
                    p {
                        font-family: Arial, sans-serif;
                        font-size: 14px;
                        text-align: default;
                        color: #333333;
                    }
                    table {
                    border:1px solid #ffffff;
                    border-collapse:collapse;
                    padding:5px;
                }
                table td {
                    font-family: Arial, sans-serif;
                    font-size: 14px;
                    border:1px solid #ffffff;
                    text-align:left;
                    padding:5px;
                    background: #FFFFFFF;
                    color: #333333;
                }
                </style>
            </head>
            <body>
                
                <img src=https://image.jimcdn.com/app/cms/image/transf/dimension=191x10000:format=png/path/s59dccae3060b5b75/image/i6e9239b04936e077/version/1500409958/image.png" alt="image" style="width:80px;height:80px;">
                <h3>Vielen Dank für Ihre Unterstützung!</h3>
                <p>Wir werden sie kontaktieren sobald wir eine Anfrage haben, die auf ihr Profil passt.</p>
                <p>Bitte haben sie etwas Geduld, da es durchaus ein paar Tage dauern kann bis ein passender Match zustande kommt. Im folgenden listen wir ihre Daten noch einmal auf.</p>

                <table>
                    <tbody>
                        <tr>
                            <td>Ihre ID</td>
                            <td>""" + row['ID'] + """</td>
                        </tr>
                        <tr>
                            <td>Name</td>
                            <td>"""+ row['Name'] +"""</td>
                        </tr>
                        <tr>
                            <td>Adresse</td>
                            <td>"""+ row['Adresse'] +"""</td>
                        </tr>
                        <tr>
                            <td>Telefonnummer</td>
                            <td>"""+str(row['Telefon'])+"""</td>
                        </tr>
                        <tr>
                            <td>Date</td>
                            <td>"""+row['Date'] + """</td>
                        </tr>
                        <tr>
                            <td>Max. Anzahl der Gäste</td>
                            <td>"""+ str(row['Max. Number Guests']) + """</td>
                        </tr>
                        <tr>
                            <td>Unterkunft</td>
                            <td> """+ row['Accomodation Type']+"""</td>
                        </tr>
                    </tbody>
                </table>
            <p>Falls sie Fragen haben, ihre Daten ändern wollen oder löschen wollen, schreiben sie bitte an wohnraum@moabit-hilft.de oder rufen sie die Hotline +49 01234567789 an.</p>
            <h5>Ihr Team von der Wohnraum Vermittlung Moabit!</h5> 
            <h5>Impressum</h5>
            <p><b>Moabit hilft e.V.</b><br />Turmstr.21<br />Haus R<br />10559 Berlin<br /><br />Fon +49 30 35057538<br />info@moabit-hilft.com<br />https://www.moabit-hilft.com</p> 
            </body>
        </html>"""

def  sendMail(receiver_rows): 
    # set the parameters required for smtplib
    # the sender and recipient below are for mail transmission.

    username = 'Die Mailaddresse'
    password = 'Das Passwort!'

    # if you want to use the inbox in the table, for example
    # there is a table named Contacts, the table has a column named Email, which stores the email addresses

    #receiver_rows = [{hosts.getRowByGenId('H-000001')},{hosts.getRowByGenId('H-000004)}]
    for row in receiver_rows:
        receiver = ['Your Debug MailAdresse']
        #receiver = row['Email'] # Use this for database
       
        text_html = MIMEText(getHMTLWithRowData(row),'html', 'utf-8')
        msg = MIMEMultipart('mixed')
        msg['From'] = f'"Moabit Hilft" <{username}>'
        msg['To'] = receiver

        msg['Subject'] = "Registrierungsbestätigung"
        msg.attach(text_html)

        try:
            mailServer = smtplib.SMTP('smtp.gmail.com', 587)
            mailServer.ehlo()
            mailServer.starttls()
            mailServer.ehlo()
            mailServer.login(username, password)
            mailServer.sendmail(username, receiver , msg.as_string())
            mailServer.close()
            print ('Email sent to ' + receiver)
        except:
            print ('Something went wrong...')
            
            
def on_update_seatable(data, index, *args):
    try:
        data = json.loads(data)
    except:
        print("Something went wrong with data decode.")
        return
    
    if (data['op_type'] == 'insert_row'):
        receiver_rows  = hosts.getRowByRowId(data['row_id'])
        sendMail(receiver_rows)

base.socketIO.on(UPDATE_DTABLE, on_update_seatable)
base.socketIO.wait()  # forever        