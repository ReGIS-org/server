import pycurl

# TODO:  get these from configuration
WEBDAV_ADRESS = "http://webdav:vadbew@localhost:8888/"
NCWMS_ADRESS = "http://ncwms:ncwms@localhost/ncWMS/admin/"

def data_get(id = None, skip = None, limit = None) -> str:
    #TODO
    return 'id: {}, skip={}, limit={}'.format(id, skip, limit)

def upload_data(upfile = None, title = None) -> str:
    filename = getFilename(upfile)

    # Upload to the webDAV server
    response_code = uploadToWebdav(upfile=upfile, filename=filename)
    print(response_code)
    # Add the data to the ncWMS server

    # Find out the WMS endpoint
    return 'returned code: {}'.format(response_code)


def getFilename(upfile):
    filename = upfile.filename
    # Check if the filename already exists on the webDAV server
    # TODO
    # If so, rename the file
    # TODO

    return filename

def uploadToWebdav(upfile, filename):
    print(upfile, type(upfile), upfile.filename)
    c = pycurl.Curl()
    c.setopt(c.URL, WEBDAV_ADRESS)
    c.setopt(c.HTTPPOST, [
        ('fileupload', (
            # upload the contents of this file
            # TODO: now it reads the whole file into memory
            c.FORM_BUFFERPTR, upfile.stream.read(),
            c.FORM_FILENAME, filename
        )),
    ])
    c.perform()
    return c.getinfo(pycurl.RESPONSE_CODE)