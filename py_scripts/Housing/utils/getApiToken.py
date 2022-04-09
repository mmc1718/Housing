from seatable_api import Base
import  os

# Import this Script in Seatable to get current API Token for local debugging

server_url = os.environ.get('dtable_web_url')
api_token = os.environ.get('api_token')
print( "**** This is your valid API-Token for local debugging ****\n\n" + str(api_token))
