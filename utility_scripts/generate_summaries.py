# generates AMAS summaries for all datasets, only where they are missing

#import AMAS
from Bio.Nexus import Nexus
import os
import shutil
#import glob

cores = 4

#all_files = glob.glob(os.path.abspath(os.path.join(os.getcwd(),'..','datasets','**')), recursive=False)

#print(all_files)



f = r"C:\Users\u7151703\Desktop\research\datasets\processing\nex\datasets"
    
alnf = os.path.join(f, 'alignment.nex')
        
print(alnf)
    
sumf = os.path.join(f, "alignment.nex-summary.txt")
taxf = os.path.join(f, "alignment.nex-seq-summary.txt")
    
if os.path.isfile(sumf)==True and os.path.isfile(taxf)==True:
    pass
else:
    # get the data type
    dat = Nexus.Nexus()
    dat.read(alnf)
    if dat.datatype == 'nucleotide':
        data_type = 'dna'
    if dat.datatype == 'protein':
        data_type = 'aa'
        
    # get the AMAS summaries
    #aln = AMAS.MetaAlignment(in_files=[alnf], data_type=data_type,in_format="nexus", cores=cores) #bug
    #aln.write_summaries(sumf)
    #aln.write_taxa_summaries(taxf)

    cmd = r'python C:\Users\u7151703\Desktop\research\code\BenchmarkAlignments\utility_scripts\AMAS.py summary -f nexus -d '+data_type+' -i '+alnf+' -c '+str(cores)+' -s'   
    os.system(cmd)
    shutil.move('summary.txt', sumf)

