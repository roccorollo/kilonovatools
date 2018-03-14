import matplotlib.pyplot as plt
import grbflux2lum
import numpy as np
import pandas as pd
import os

GRB,z,filt,nueffgrb,flux,fluxerr,dhour=grbflux2lum.read_db()
lum,lumerr,dhour_rf,nueffgrbz=grbflux2lum.lumlcgrb(flux,fluxerr,z,dhour,nueffgrb)
#grbflux2lum.printoutput(GRB,filt,nueffgrbz,dhour_rf,lum,lumerr,flux,fluxerr)
grbflux2lum.printoutput(GRB,filt,nueffgrbz,dhour_rf,lum,lumerr,flux,fluxerr)

#id=raw_input(' Which GRB do you want to plot? [e.g. 130603B]:') or '130603B'
#fil=raw_input(' in which filter? [e.g. r*]:') or 'r*'

#pathgrb="./GRB_DATA/"
#pathkn='../kilonovatools/lc/'
pathkn='./lc/'
pathplot='./PLOTS/'

ex='n'
setfilter='y'
#changegrb='y'

filterlist=['B','b*','g','V','r*','R','Rc','I','i*','J','H','K','Ks','Y','z*','Z','F814W','F160W']
colorlist=['navy','blue','green','darkgreen','red','crimson','darksalmon','tan','magenta','gold','orange','coral','lime','plum','maroon','turquoise','cyan','rosybrown']


while ex == 'n':
    print 'last GRB:',id
    print GRB

    id=raw_input(' Which GRB do you want to plot? [e.g. 130603B]:') or '130603B'

    print ''
    print 'Filters available for this GRB'
    filtgrb=filt[np.where(GRB == id)]
    zgrb=z[np.where(GRB == id)]
    zgrb0=zgrb[0]
    print filtgrb, zgrb0

    # prende il file con la KN riscalata al GRB selezionato
    filename=pathkn+id+'lc.dat'
    datakn=pd.read_csv(filename,comment='#', sep='\t',skiprows=None,skip_blank_lines=True)
    print ''
    print 'DATI DELLA KN RISCALATA AL GRB SELEZIONATO (',id,')'
    print datakn
    datakn_array=datakn.values

    #setfilter='y'

    #while setfilter == 'y':

    filtgrb_n=[]
    k=0
    for fil in filtgrb:
        filtgrb_n.append(fil)

        #print filtgrb
        #fil=raw_input(' in which filter? [e.g. r*]:') or 'r*'

        # -- Definisco il filtro per la kn
        filkn='.'+fil

        if '*'in fil:
            filkn = '.'+fil[:-1]

        if fil == 'F160W':
            filkn='f160w'
        if fil == 'F814W':
            filkn='f814w'

        if fil == 'Rc':
            filkn='R_Cousin'

        print ''
        print 'PLOTTING GRB',id,' IN FILTER ',fil
        print ''

        s=colorlist[filterlist.index(fil)]
        print ''
        print 's=',s
        print ''

        #for i in range(0,len(datakn_array[:,2])):
        #    datakngrb=datakn_array[np.where('.'+fil in datakn_array[i,2])]

        listkngrb=[]
        for i in range(0,len(datakn_array[:,2])):
            if (filkn in datakn_array[i,2]):
                listkngrb.append(datakn_array[i])

        datakngrb=np.array(listkngrb)
        print 'KN data in this filter'
        print datakngrb
        print ''

        #setfilter=raw_input('Is KN lum in this filter good (>0) ? [n/y] default y:') or 'y'

        #if setfilter == 'y':

        print ''
        print 'Plot in filter ', fil, 'with color ',s
        print ''
        #datakngrbflat=datakngrb.flatten()


        lumkngrb=datakngrb[:,1]
        timekngrb_hr=(datakngrb[:,3]-57982.528)*24.0

        if lumkngrb[0] > 0:

            ykn0=lumkngrb[np.where(lumkngrb > 0)]
            xkn0=timekngrb_hr[np.where(lumkngrb > 0)]
            indexkn=np.argsort(xkn0)
            ykn=ykn0[indexkn]
            xkn=xkn0[indexkn]
            #print ''
            #print 'KN data in filt ',fil, xkn,ykn

            # creo un vettore x con i tempi del GRB e della kN nel filtro X
            timegrb_hr=np.array(dhour_rf[np.where((GRB == id) & (filt == fil))])
            lumgrb=np.array(lum[np.where((GRB == id) & (filt == fil))])
            dlumgrb=np.array(lumerr[np.where((GRB == id) & (filt == fil))])

            x0grb=timegrb_hr[np.where(dlumgrb > 0)]
            y0grb=lumgrb[np.where(dlumgrb > 0)]
            dy0grb=dlumgrb[np.where(dlumgrb > 0)]
            index=np.argsort(x0grb)
            xgrb=x0grb[index]
            ygrb=y0grb[index]
            dygrb=dy0grb[index]

            #print 'xgrb,ygrb', xgrb,ygrb,fil

            xgrb_ul=timegrb_hr[np.where(dlumgrb == 0)]
            ygrb_ul=lumgrb[np.where(dlumgrb == 0)]

            x=np.append(timegrb_hr,xkn)

            # creo un vettore y con le Lum. del GRB e della kN nel filtro X

            y=np.append(lumgrb,ykn)

            print 'timegrb,xkn in filter ',fil
            print timegrb_hr,xkn
            print 'x,y',x,y
            # Plotta la kn

            #plt.loglog(xgrb,ygrb,'*',label='GRB in '+fil)
            if k==0:
            #plt.loglog(xkn,ykn,'k:')
                plt.loglog(x,y,'.',color=s,label=filtgrb_n[k])
            if k>0:
                plt.loglog(x,y,'.',color=s,label=filtgrb_n[k] if filtgrb_n[k] != filtgrb_n[k-1] else '')

            #plt.loglog(x,y,'.',color=s,label=fil)
            plt.loglog(xkn,ykn,':',color=s)

            # plotta i dati con errore definito
            for i in dygrb:
                if i>0:
                    #plt.loglog(xgrb,ygrb,color=s)
                    plt.loglog(xgrb,ygrb,'o',color=s)
                    plt.errorbar(xgrb, ygrb, yerr=dygrb,fmt='o',color=s)

            # plotta gli upper limits
            plt.loglog(xgrb_ul,ygrb_ul,'v',color=s)
            plt.xlabel('rest frame time [hrs]')
            plt.ylabel('Ln [erg/s Hz]')
            #plt.title('GRB'+id+' observed in the filter '+fil)
            plt.title('GRB'+id+' and KN170817 at z='+str(zgrb0))
            #plt.legend()
            #plt.show()

        else:
            print 'La lum della KN in questo filtro = NAN'
            print datakngrb

        k=k+1

    plt.legend()
    plt.show()

    # Definisce i file di output
    #outfilegrb=pathgrb+id+"_"+fil+".dat"

    #outfile=pathplot+'GRB'+id+'_KN_'+fil+'.png'
    outfile=pathplot+'GRB'+id+'_KN.png'
    #plt.legend()
    #plt.show()

    #if os.path.isfile(outfile):
    #    os.system('rm '+outfile)
    #if not os.path.isfile(outfile):
    plt.savefig(outfile)

    #print filtgrb

    #setfilter=raw_input('Stay with this GRB and another filter? [n/y] default y:') or 'y'


    # Se cambio GRB pulisce i plot e resetta

    changegrb=raw_input('Change GRB? [n/y] default y, if no then exit:') or 'y'
    plt.clf()
    plt.close()
    ex=raw_input('Would you like to exit? [n/y] default n:') or 'n'
