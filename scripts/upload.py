import pycurl
import json
from urllib.parse import urlencode

with open('./formdata.json') as f:
    post_data = json.load(f)

c = pycurl.Curl()
post_fields = urlencode(post_data)
c.setopt(c.POSTFIELDS, post_fields)
#c.setopt(c.URL, 'http://ncwms:ncwms@localhost/ncWMS/admin/updateConfig')
c.setopt(c.URL, 'http://ncwms:ncwms@localhost/ncWMS/admin/addData')
c.perform()
