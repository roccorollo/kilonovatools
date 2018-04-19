reset

set logscale y

set xlabel "time [d]"
set ylabel "Luminosity [erg/s/Hz]"

set term pngcairo font "Helvetica,14"  
set output "lc_all.png"
pl "<(grep 'micParanal_HAWKI.J' 130603Blc.dat)" u 4:2 w p lw 2 title "",\
   "<(grep 'micParanal_HAWKI.H' 130603Blc.dat)" u 4:2 w l lw 2 title "",\
   "<(grep 'micParanal_HAWKI.H' 130603Blc.dat)" u 4:2 w l lw 2 title ""







































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


