#! /usr/bin/python

import time
import calendar
import urllib
import math
from subprocess import Popen, PIPE

GNUPLOT_SCRIPT = """reset
set term svg size 600 480 dynamic fname 'Helvetica'
set xdata time
set xlabel "Time"
set timefmt "%Y-%m-%d-%H-%M"
set format x "%l%p"
set yrange [-0.02:{}]
set ytics border nomirror format '% g"'
set y2tics border nomirror format '% gdegF'
set grid y2tics
set title "Last 12 hours rain and temperature at UW weather station"

plot "-" using 1:2 axes x1y2 smooth bezier lt 1 lw 2 notitle,\\
"-" using 1:2 axes x1y1 smooth bezier lt 3 lw 2 notitle
"""

def read_data(datafile):
    """Convert weather csv file to array"""

    data = []

    # the first two lines are headers
    datafile.next()
    datafile.next()

    for line in datafile:
        row = line.split(',')

        # date and time
        parsed_time = time.strptime(row[1]+' '+row[2],"%Y-%m-%d %H:%M")
        gmt_time=calendar.timegm(parsed_time)
        local_time=time.localtime(gmt_time)

        data.append([time.strftime("%Y-%m-%d-%H-%M", local_time),
            row[3], row[5].strip()])

    return data

def gnuplot_cmd(data):
    """Return generator for the data to be fed into gnuplot"""

    max_rain = float(data[-1][2])

    yield GNUPLOT_SCRIPT.format(math.ceil(max_rain + 0.05))

    # temperature
    for row in data:
        if row[1][:3] <> "0.0":
            yield row[0] + " " + row[1]
    yield "end\n"

    # rain
    for row in data:
        yield row[0] + " " + row[2]
    yield "end"

def doupdate(plotfilename):
    #grab the rawdata from atmos.washington.edu
    rawdata = urllib.urlopen("http://www-k12.atmos.washington.edu/k12/grayskies/plot_nw_wx.cgi?Measurement=Temperature&Measurement=SumRain&station=UWA&interval=12&connect=dataonly")
    data = read_data(rawdata)
    rawdata.close()

    #run gnuplot
    process = Popen(["gnuplot"],stdin=PIPE,stdout=PIPE)
    graph = process.communicate("\n".join(gnuplot_cmd(data)))[0]

    # replace some text in the labels
    graph=graph.replace("<text> 0pm</text>","<text>noon</text>",1)
    graph=graph.replace("<text> 0am</text>","<text>midnight</text>",1)
    graph=graph.replace("pm</text>","</text>")
    graph=graph.replace("am</text>","</text>")
    graph=graph.replace("degF","&#xb0;")
    # this line is necessary because gnuplot makes funny svgs
    graph=graph.replace("\n xmlns:xlink=",'\n xmlns="http://www.w3.org/2000/svg"\n xmlns:xlink=',1)

    #output graph
    print graph

    #save graph
    graphfile=open(plotfilename,'w')
    graphfile.write(graph)
    graphfile.close()


def servegraph(plotfilename):
    graphfile = open(plotfilename,'r')
    print graphfile.read()
    graphfile.close()

if __name__ == "__main__":
    doupdate('weather.svg')

#     rawdata = urllib.urlopen("http://www-k12.atmos.washington.edu/k12/grayskies/plot_nw_wx.cgi?Measurement=Temperature&Measurement=SumRain&station=UWA&interval=12&connect=dataonly")
#     data = read_data(rawdata)
#     rawdata.close()
#     for line in gnuplot_cmd(data):
#         print line
