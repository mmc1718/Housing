import sys
import os
sys.path.append(os.getcwd())


from seatable_api import Base, context
import utils.DummyScript

def initBase():
    server_url = context.server_url or 'https://cloud.seatable.io'
    api_token = context.api_token or 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkdGFibGVfdXVpZCI6IjljNDNhNTU4LWIzNmEtNGMyMy1iM2Y0LTQ0MThmMDRkY2QwZSIsImFwcF9uYW1lIjoiNzdXcC5weSIsImV4cCI6MTY0OTU0MTc1OX0.A_KArbYBe51j8eDtv-zygF3F4lNLnCexUhjFwj5NoPE'
    base = Base(api_token, server_url)
    base.auth()
    return base
    

if __name__ == "__main__":
    base = initBase()
    hostingBase = utils.DummyScript.HostingBase(base)
    h= hostingBase.getHostByID('H-000001')

    
    
    
