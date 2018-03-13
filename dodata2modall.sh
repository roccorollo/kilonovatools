

#for i in spec_sequence_Sep6/timesmooth/*dat; 
for i in superspectra/*dat; 
do  name=$(basename $i) ; 
	echo $name; 
	python data2mod.py $i superkn170817model_43p66mpc_${name} 0.0098;
done

#remove last 5 epochs from spectra:
rm superkn170817model_43p66mpc_supernewXSGW0829_smooth.dat
rm superkn170817model_43p66mpc_supernewXSGW0830_smooth.dat
rm superkn170817model_43p66mpc_supernewXSGW0831_smooth.dat
rm superkn170817model_43p66mpc_supernewXSGW0901_smooth.dat
rm superkn170817model_43p66mpc_supernewXSGW0902_smooth.dat

# keep only photometry from 0.5,1 , 2.5 and 4.5 days
mkdir mmm123456
mv superkn170817model_43p66mpc_supersed_time579* mmm123456/
mv mmm/superkn170817model_43p66mpc_supersed_time57983.03.dat ./
mv mmm/superkn170817model_43p66mpc_supersed_time57983.53.dat ./
mv mmm/superkn170817model_43p66mpc_supersed_time57984.95.dat ./
mv mmm/superkn170817model_43p66mpc_supersed_time57987.03.dat ./

rm -rf mmm123456

cp -r /home/rossi/work/kilonova/kilonovamodels/gw170817superspectra 
cp -r /home/rossi/work/kilonova/kilonovamodels/gw170817superspectra_old 
rm gw170817superspectra/*
mv superkn170817model_43p66mpc_* gw170817superspectra/

