from Bio.Nexus import Nexus
import os
import shutil
import argparse


def gen_smy(inpath, cores):        
    alnf = os.path.join(inpath, 'alignment.nex')        
    sumf = os.path.join(inpath, "alignment.nex-summary.txt")
    taxf = os.path.join(inpath, "alignment.nex-seq-summary.txt")
        
    if os.path.isfile(sumf)==True and os.path.isfile(taxf)==True:
        pass
    else:
        # get the data type
        dat = Nexus.Nexus()
        dat.read(alnf)
        if dat.datatype == 'dna':
            data_type = 'dna'
        if dat.datatype == 'protein':
            data_type = 'aa'
               
        cmd = 'python AMAS.py summary -f nexus -d '+data_type+' -i '+alnf+' -c '+str(cores)+' -s'   
        os.system(cmd)
        shutil.move('summary.txt', sumf)


# running
parser = argparse.ArgumentParser(description='')
parser.add_argument('--inpath', '-i', help='', 
                    required = True)
parser.add_argument('--cores', '-c', help='', 
                    default = 1)
args = parser.parse_args()

if __name__ == '__main__':
    try:
       gen_smy(args.inpath, args.cores)
    except Exception as e:
        print(e)  
