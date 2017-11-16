# server
Server to host NetCDF files and provide a WML interface. To start:

1. clone repository: `git clone https://github.com/ReGIS-org/server.git`
1. go to server directory: `cd server`
1. start webdav and docker container: `docker-compose up -d`
1. go to upload directory: `cd ..`
1. copy netcdf file to webdav container: `curl -T tos_O1_2001-2002.nc http://webdav:vadbew@localhost:8888/`
1. upload file from webdav container to ncwms: `python upload.py`
1. check if the upload succeeded: go to http://localhost/ncWMS/admin/ in a web browser (user/password: ncwms/ncwms)

Notes:

* in order for `docker-compose` to run, the docker deamon must be running, for example: `sudo service docker start`
* example netcdf files can be downloaded from: http://www.unidata.ucar.edu/software/netcdf/examples/files.html
* the name of the expected netcdf file is specified in the file `server/formdata.json` (on line 2)
