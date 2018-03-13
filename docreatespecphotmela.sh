

for i in spec_sequence_Sep6/timesmooth/n*dat ; 
do name=$(basename $i ); 
	echo $name; 
	python dospectophot.py $i trasm/ mic ; 
done


head="# MJD           Exp.    Mag     Err     System  EbvCorr filter"

# for each filter

odir="XSspectophot"
mkdir $odir
for t in trasm/*dat
do trname=$(basename $t | awk -F".dat" '{print $1}');
 oname="XSspectophot_${trname}.dat" 
 printf "%s\n" "$head" > $odir/${oname} 
 grep -v ^"-99" newXS*dat  | grep "${trname}" | awk -v f=$trname '{OFS="\t"; print $NF,-99,$3,-99,"#AB","no",f}'   >> $odir/${oname} 
done

