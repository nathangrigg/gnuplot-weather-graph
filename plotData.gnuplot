#!/usr/bin/gnuplot
reset
set term svg size 600 480 dynamic fname 'Helvetica'
set xdata time
set xlabel "Time"
set ylabel "degrees Fahrenheit"
set timefmt "%Y-%m-%d-%H-%M"
set format x "%l"
set y2tics border
set noytics
set grid y2tics
set title "Last 12 hours temperature at UW weather station"
set output "weather.svg"

plot "data.txt" using 1:2 with lines lt 3 lw 2 notitle
