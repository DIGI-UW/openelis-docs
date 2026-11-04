import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from frlib import *
req('PUT','/rest/api/content/1679458382/move/append/1641447437')
print(get('/api/v2/folders/1679458382')['parentId'])
