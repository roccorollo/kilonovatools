reset


set xlabel "wavelength [A]"
set ylabel "Luminosity [erg/s/A]"

set term pngcairo font "Helvetica,14"  
set output "model_GW170817fromXSdata_1dot5days.png"
pl "kn170817model_43p66mpc_newXSGW0818_smooth.dat" u 1:2 w l title""

set term wxt
replot




