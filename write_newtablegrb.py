import grbflux2lum
import os

GRB,z,filt,filt_old,nueffgrb,flux,fluxerr,dhour=grbflux2lum.read_db()

#outfile='tablegrb_simplified.txt'
outfile='tablegrb.txt'

if os.path.isfile(outfile):
#       os.system('rm '+path1+'newmodel_alphafix.txt')
        os.system('rm '+outfile)
if not os.path.isfile(outfile):
        os.system('touch '+outfile)
        out_file = open(outfile,"a")
        out_file.write("GRB z dhour flux fluxerr filtold filtnew"+"\n")
        out_file.close()

out_file = open(outfile,"a")
for i in range(len(GRB)):
    out_file.write(str(GRB[i])+"\t"+str(z[i])+"\t"+str(dhour[i])+"\t"+str(flux[i])+"\t"+str(fluxerr[i])+"\t"+str(filt_old[i])+"\t"+str(filt[i])+"\n")

out_file.close()
