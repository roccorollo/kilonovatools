reset


set xlabel "wavelength[A]"
set ylabel "Transmission"
set title "_NAM_"

set term pngcairo 
set output "_OUT_"
set font "Helvetica 14"
plot "_INP_" u 1:2 w l lc rgb "blue" lw 2

set term wxt
replot
