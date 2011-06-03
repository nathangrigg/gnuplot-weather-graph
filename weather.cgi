#! /usr/bin/python

import os,time,calendar,csv

print "Content-Type: image/svg+xml;\n"

datafilename = "data.txt"
plotfilename = "weather.svg"

if (time.time()-os.stat(datafilename).st_mtime)>420:
	rawdata = os.popen('curl -s "http://www-k12.atmos.washington.edu/k12/grayskies/plot_nw_wx.cgi?Measurement=Temperature&station=UWA&interval=12&connect=dataonly"','r')
	data = csv.reader(rawdata)
	data.next() #forget the header
	output = open(datafilename,'w')
	for row in data:
		output.write(time.strftime("%Y-%m-%d-%H-%M",time.localtime(calendar.timegm(time.strptime(row[1],"%Y-%m-%d %H:%M")))) + " " + row[2] + "\n")
	output.close()
	rawdata.close()
	
	gnuplot = os.popen('./plotData.gnuplot','r')
	gnuplot.close()



graphfile = open(plotfilename,'r')
graph=graphfile.readlines()
# for some reason, Safari refuses to display the graph unless I
# insert the following line into the svg file:
graph.insert(3,'xmlns="http://www.w3.org/2000/svg"\n')
print "".join(graph)
graphfile.close()
