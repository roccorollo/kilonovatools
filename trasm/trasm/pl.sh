# do the plots
for i in *dat;
#for i in micUKIRT_UKIDSS.Z.dat
do
inp=$i
name=$(echo $i | awk -F".dat" '{print $1}')
echo $name
out="plot${name}.png"
cp pl.gnu plot${name}.gnu
perl -p -i -e "s,_NAM_,$name,g" plot${name}.gnu
perl -p -i -e "s,_INP_,$inp,g" plot${name}.gnu
perl -p -i -e "s,_OUT_,$out,g" plot${name}.gnu
gnuplot	plot${name}.gnu
rm plot${name}.gnu

done



