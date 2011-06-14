#! /usr/bin/python

import os,time,calendar,csv,subprocess,urllib
pipe=subprocess.PIPE

print "Content-Type: image/svg+xml;\n"

gnuplot_script="""reset
set term svg size 600 480 dynamic fname 'Helvetica'
set xdata time
set xlabel "Time"
set ylabel "degrees Fahrenheit"
set timefmt "%Y-%m-%d-%H-%M"
set format x "%l%p"
set y2tics border
set noytics
set grid y2tics
set title "Last 12 hours temperature at UW weather station"

plot "-" using 1:2 smooth bezier lt 3 lw 2 notitle
"""

def doupdate():
	global plotfilename
	#grab the rawdata from atmos.washington.edu
	rawdata = urllib.urlopen("http://www-k12.atmos.washington.edu/k12/grayskies/plot_nw_wx.cgi?Measurement=Temperature&station=UWA&interval=12&connect=dataonly")

	#parse the csv data
	data = csv.reader(rawdata)
	data.next() #forget the header

	#fix date formats, process for gnuplot
	gnuplot_data=[gnuplot_script]
	for row in data:
		if row[2][:3]<>"0.0":
			gnuplot_data.append(time.strftime("%Y-%m-%d-%H-%M",
			time.localtime(calendar.timegm(time.strptime(row[1],"%Y-%m-%d %H:%M")))) +
			" " + row[2])

	rawdata.close()

	#run gnuplot
	process = subprocess.Popen(["gnuplot"],stdin=pipe,stdout=pipe)
	graph = process.communicate("\n".join(gnuplot_data))[0]

	graph=graph.replace("<text> 0pm</text>","<text>noon</text>",1)
	graph=graph.replace("<text> 0am</text>","<text>midnight</text>",1)
	graph=graph.replace("pm</text>","</text>")
	graph=graph.replace("am</text>","</text>")
	graph=graph.replace("\n xmlns:xlink=",'\n xmlns="http://www.w3.org/2000/svg"\n xmlns:xlink=',1)

	#output graph
	print graph

	#save graph
	graphfile=open(plotfilename,'w')
	graphfile.write(graph)
	graphfile.close()


def servegraph():
	graphfile = open(plotfilename,'r')
	print graphfile.read()
	graphfile.close()

#file names
plotfilename = "weather.svg"
lastupdate = "lastupdate"
logfile = "log.txt"

#begin execution
try:
	lastupdatetime=os.stat(lastupdate).st_mtime
	#if i have updated in the last 7 minutes
	if (time.time()-lastupdatetime)<420 and os.stat(plotfilename).st_mtime>=lastupdatetime:
		redrawgraph=False
	else:
		redrawgraph=True
except:
		redrawgraph=True

if redrawgraph:
	# mark as updated
	open(lastupdate,'w').close()
	doupdate()
	file=open(logfile,'a')
	file.write(time.strftime("%Y-%m-%d %H:%M:%S\n",time.localtime(time.time())))
	file.close()
else:
	servegraph()






