#! /usr/bin/python

import os,time,calendar,csv

print "Content-Type: image/svg+xml;\n"

def doupdate():
	global datafilename,lastupdate

	#grab the rawdata from atmos.washington.edu
	rawdata = os.popen('curl -s "http://www-k12.atmos.washington.edu/k12/grayskies/plot_nw_wx.cgi?Measurement=Temperature&station=UWA&interval=12&connect=dataonly"','r')

	#parse the csv data
	data = csv.reader(rawdata)
	data.next() #forget the header
	output = open(datafilename,'w')

	#fix date formats
	for row in data:
		output.write(time.strftime("%Y-%m-%d-%H-%M",
		time.localtime(calendar.timegm(time.strptime(row[1],"%Y-%m-%d %H:%M")))) +
		" " + row[2] + "\n")
	output.close()
	rawdata.close()

	#run gnuplot
	gnuplot = os.popen('./plotData.gnuplot','r')
	gnuplot.close()

def servegraph():
	graphfile = open(plotfilename,'r')
	graph=graphfile.readlines()
	# for some reason, Safari refuses to display the graph unless I
	# insert the following line into the svg file:
	graph.insert(3,'xmlns="http://www.w3.org/2000/svg"\n')
	print "".join(graph)
	graphfile.close()

#file names
datafilename = "data.txt"
plotfilename = "weather.svg"
lastupdate = "lastupdate"

#begin execution
try:
	lastupdatetime=os.stat(lastupdate).st_mtime
	#if i have updated in the last 7 minutes
	if (time.time()-lastupdate)<420 and os.stat(plotfilename).st_mtime>=lastupdatetime:
		redrawgraph=False
	else:
		redrawgraph=True
except:
		redrawgraph=True

if redrawgraph:
	# mark as updated
	open(lastupdate,'w').close()
	doupdate()

servegraph()






