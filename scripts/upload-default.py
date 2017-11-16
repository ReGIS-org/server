#!/usr/bin/python3 -W all
# upload-default.py: default upload of netcdf file to ncwms
# usage: upload-default.py
# notes: 1. does not require ncwms to be changed
#        2. information of uploaded file is read from local formdata.json file
#        3. uses pycurl, see http://pycurl.io/docs/latest/quickstart.html
# 20171114 erikt(at)xs4all.nl

import json
import pycurl
import re
from lxml import html
from io import BytesIO
from urllib.parse import urlencode

GETURL = "http://ncwms:ncwms@localhost/ncWMS/admin/"
POSTURL = GETURL+"updateConfig"
FORMDATAFILE = "formdata.json"
KEYS = ["copyright","id","location","moreinfo","queryable","reader","title","updateinterval"]

postData = {}

def readFormData(formDataFile):
    with open(FORMDATAFILE) as f:
        postdata = json.load(f)
        f.close()
    return(postdata)

def doGet(url):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL,url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    body = buffer.getvalue()
    body = body.decode('iso-8859-1')
    return(body)

def doPost(url,postfields):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL,url)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.POSTFIELDS, postfields)
    c.perform()
    c.close()
    body = buffer.getvalue()
    if body: print(body.decode('iso-8859-1'))

def getFormInputData(body):
    tree = html.fromstring(body)
    elements = tree.xpath('//input')
    data = {}
    for e in elements:
        name = e.xpath('@name')[0]
        value = ""
        if len(e.xpath('@value')) > 0: value = e.xpath('@value')[0]
        for key in KEYS:
            if re.match("^dataset\..*\."+key+"$",name):
                name = re.sub("^dataset\.","",name)
                name = re.sub("\."+key+"$","",name)
                if not re.match("^new\d+$",name): 
                    if not name in data: data[name] = {}
                    data[name][key] = value
    return(data)

def getFormSelectData(body):
    tree = html.fromstring(body)
    elements = tree.xpath('//select')
    data = {}
    key = "updateinterval"
    for e in elements: 
        name = e.xpath('@name')[0]
        if re.match("^dataset\..*\."+key+"$",name):
            for o in e.xpath('.//option'):
                if o.xpath('@selected'):
                    name = re.sub("^dataset\.","",name)
                    name = re.sub("\."+key+"$","",name)
                    if not name in data: data[name] = {}
                    data[name][key] = o.xpath('@value')[0]
    return(data)

def addData(inData,outData):
    for name in inData:
        for key in KEYS:
            outDataKey = "dataset."+name+"."+key
            if not key in inData[name] and not outDataKey in outData: 
                inData[name][key] = "MISSING!"
            elif key in inData[name]:
                outData[outDataKey] = inData[name][key]
    return(outData)

def main():
    body = doGet(GETURL)
    postData = readFormData(FORMDATAFILE)
    dataInput = getFormInputData(body)
    postData = addData(dataInput,postData)
    dataSelect = getFormSelectData(body)
    postData = addData(dataSelect,postData)
    postFields = urlencode(postData)
    doPost(POSTURL,postFields)

if __name__ == "__main__":
    main()
