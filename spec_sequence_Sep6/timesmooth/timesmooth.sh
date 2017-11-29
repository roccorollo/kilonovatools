
ut="# PARAMETER UT     ";
mjd="## PARAMETER MJD    "
pha="# PARAMETER PHASE  "

for f in X*dat; 
do printf "%s\n" "$ut"> new$f; 
   printf "%s\n" "$mjd">> new$f; 
   printf "%s\n" "$pha">> new$f; 
   cat $f >> new$f; 
done
