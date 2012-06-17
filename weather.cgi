#! /usr/local/bin/python2.5

from weather import *
import os

print "Content-Type: image/svg+xml;\n"

#file names
plotfilename = "weather.svg"
lastupdate = "lastupdate"

#begin execution
try:
    lastupdatetime=os.stat(lastupdate).st_mtime
    #if i have updated in the last 7 minutes
    if (time.time()-lastupdatetime)<420 and \
        os.stat(plotfilename).st_mtime>=lastupdatetime:
        redrawgraph=False
    else:
        redrawgraph=True
except:
        redrawgraph=True

if redrawgraph:
    # mark as updated
    open(lastupdate,'w').close()
    doupdate(plotfilename)
else:
    servegraph(plotfilename)
