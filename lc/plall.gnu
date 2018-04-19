reset

# functions:
pi=3.14
z=0.356
cc=3.e8
ckm=cc/1000 ## km/s
ccm=cc*100 ## cm/s
cca=cc*10**10 ##angstrom /s
t0=57982.528

jytol(x)=x*10**(-23) * ( 4 * pi * DL **2 ) / (1+z) #*cca/(ang**2)

# PLOT
set logscale y

set xlabel "time [d]"
#set xlabel "time [hrs]"
set ylabel "Luminosity"
set y2label "AB magnitude"


set xrange [0:15]
set term pngcairo font "Helvetica,14"  
set output "lc_all.png"
pl \
   "<(grep 'micSLOAN_SDSS.g'      170817Alc.dat | sort -gk4)" u ($4-t0):2 w l lw 2 lc 4 title "g",\
   "<(grep 'micSLOAN_SDSS.r'      170817Alc.dat | sort -gk4)" u ($4-t0):2 w l lw 2 lc 5 title "r",\
   "<(grep 'micSLOAN_SDSS.i'      170817Alc.dat | sort -gk4)" u ($4-t0):2 w l lw 2 lc 6 title "i",\
   "<(grep 'micSLOAN_SDSS.z'      170817Alc.dat | sort -gk4)" u ($4-t0):2 w l lw 2 lc 7 title "z",\
   "<(grep 'micParanal_HAWKI.J'   170817Alc.dat | sort -gk4)" u ($4-t0):2 w l lw 2 lc 1 title "J",\
   "<(grep 'micParanal_HAWKI.H'   170817Alc.dat | sort -gk4)" u ($4-t0):2 w l lw 2 lc 2 title "H",\
   "<(grep 'micParanal_HAWKI.Ks'  170817Alc.dat | sort -gk4)" u ($4-t0):2 w l lw 2 lc 3 title "K"


set term wxt
replot







































pi=3.14
z=0.356
cc=3.e8
ckm=cc/1000 ## km/s
ccm=cc*100 ## cm/s
cca=cc*10**10 ##angstrom /s
ang=16500

##jytol(x)=x*10**(-23) * ( 4 * pi * DL **2 ) / (1+z) #*cca/(ang**2)

set xlabel "time [hrs]"
set output "lc_GW170817fromXSdata_Jband_GRB130613Bwmodel.png"
pl [][:1e29]"<(grep 'micParanal_HAWKI.J' 130603Blc.dat)" u (($4-57982.528)*24.):2 w l lw 2 title "model from KN170817",\
   "<(grep 'J' ../grbdata/130603B_J.dat| awk -F ',' '{print $1,$2,$3,$4,$5}')" u ($3):(1.*$4) w p lw 2title "J band",\
   "<(grep 'F160' ../grbdata/130603B_F160Wandrea.dat| awk -F ',' '{print $1,$2,$3,$4,$5}')" u ($3):(1.*$4) w p lw 2 lc rgb "red" title "F160W from Tanvir"



set term wxt
replot


