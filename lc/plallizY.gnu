reset

# functions:
pi=3.14
z=0.356
cc=3.e8
ckm=cc/1000 ## km/s
ccm=cc*100 ## cm/s
cca=cc*10**10 ##angstrom /s
t0=57982.528

# with x is lumh [erg/s /Hz]
mabs(x)=2.5*log10((3.08568 * 10**24 * 10**-5)**2*4*pi) -2.5*23-2.5*log10(x)

# PLOT
#set term pngcairo font "Helvetica,14"  
set encoding iso_8859_1 
set terminal postscript eps enhanced color font "Helvetica,28"
set output "lc_allzY.eps"
set size 1.6,1.4
#set lmargin 6
#set bmargin 3.5
set border -1 lw 2

set logscale y
unset logscale y2
unset logscale x
unset logscale x2


set xlabel "time [d]" offset 0,0.5
set x2label "time [hrs]" offset 0,-0.5
#set xlabel "time [hrs]"
###set ylabel "Luminosity [erg/s/Hz]" offset 0.5,0.0
set ylabel  "{/Times=30 L_{/Symbol n} [erg/s/Hz] }"  

set y2label "Absolute magnitude [AB]" offset 0.0,0.0

set ytics  nomirror  #font "Helvetica,28"
set y2tics  nomirror #font "Helvetica,28"
set xtics  nomirror  #font "Helvetica,28"
set x2tics  nomirror #font "Helvetica,28"
set tics scale 2
#set mxtics 10    
#set mx2tics 10    
#set mytics 5  
set my2tics 5
#set format x "%.0e"
#set format x2 "%.0e"
set format y2 "%.0f"
set format y "10^{%L}"


xmin=0.3
xmax=12.0 # 35.0
set xrange [xmin:xmax]
set x2range [xmin*24.0:xmax*24.0]
ymin=5e23
ymax=5e27
set yrange [ymin:ymax]
set y2range [mabs(ymin):mabs(ymax)]

pl \
   "<(grep 'micGeneric_Bessell.U'      GRB0lc.dat | sort -gk4)" u ($4-t0):2 w l lt 1 lw 4 lc rgb "blue"   title "U",\
   "<(grep 'micGeneric_Bessell.R'      GRB0lc.dat | sort -gk4)" u ($4-t0):2 w l lt 1 lw 4 lc rgb "green" title "R",\
   "<(grep 'micSLOAN_SDSS.z'          GRB0lc.dat | sort -gk4)" u ($4-t0):2 w l lw 4 lc rgb "red"  title "z",\
   "<(grep 'micParanal_HAWKI.Y'       GRB0lc.dat | sort -gk4)" u ($4-t0):2 w l lw 4 lc rgb "orange"  title "Y",\
   "<(grep 'micParanal_HAWKI.J'        GRB0lc.dat | sort -gk4)" u ($4-t0):2 w l lt 1 lw 4 lc rgb "brown"  title "J",\
   "<(grep 'micParanal_HAWKI.H'        GRB0lc.dat | sort -gk4)" u ($4-t0):2 w l lt 1 lw 4 lc rgb "black"  title "H",\
   "<(grep 'micParanal_HAWKI.Ks'       GRB0lc.dat | sort -gk4)" u ($4-t0):2 w l lt 1 lw 4 lc rgb "violet" title "Ks",\
   x*0  notitle w l axis x1y2,\
   x*0  notitle w l axis x2y1


#pl \
#   "<(grep 'micSwift_UVOT.UVU'    GRB0lc.dat | sort -gk4)" u ($4-t0):2 w l lw 4 lc rgb "blue"   title "u",\
#   "<(grep 'micSLOAN_SDSS.g'      GRB0lc.dat | sort -gk4)" u ($4-t0):2 w l lw 4 lc rgb "green"  title "g",\
#   "<(grep 'micSLOAN_SDSS.r'      GRB0lc.dat | sort -gk4)" u ($4-t0):2 w l lw 4 lc rgb "red"    title "r",\
#   "<(grep 'micSLOAN_SDSS.i'      GRB0lc.dat | sort -gk4)" u ($4-t0):2 w l lw 4 lc rgb "orange" title "i",\
#   "<(grep 'micSLOAN_SDSS.z'      GRB0lc.dat | sort -gk4)" u ($4-t0):2 w l lw 4 lc rgb "olive"  title "z",\
#   "<(grep 'micParanal_HAWKI.J'   GRB0lc.dat | sort -gk4)" u ($4-t0):2 w l lw 4 lc rgb "brown"  title "J",\
#   "<(grep 'micParanal_HAWKI.H'   GRB0lc.dat | sort -gk4)" u ($4-t0):2 w l lw 4 lc rgb "black"  title "H",\
#   "<(grep 'micParanal_HAWKI.Ks'  GRB0lc.dat | sort -gk4)" u ($4-t0):2 w l lw 4 lc rgb "violet" title "Ks",\
#   x*0  notitle w l axis x1y2,\
#   x*0  notitle w l axis x2y1

set term pngcairo font "Helvetica,14"  
set encoding iso_8859_1 
set output "lc_allzY.png"
set size 1,1
replot


set term wxt
replot































