from amas import AMAS
from Bio.Nexus import Nexus
import os
import glob

all_files = glob.glob(os.path.abspath(os.path.join(os.getcwd(),'..','datasets','**')), recursive=False)

print(all_files)

for f in all_files:
	alnf = os.path.join(f, 'alignment.nex')

	# get the data type
	dat = Nexus.Nexus()
	dat.read(alnf)
	if(dat.datatype=='nucleotide'): type = 'dna'
	if(dat.datatype=='protein'): type= 'aa'

	# get the AMAS summaries
	aln = AMAS.MetaAlignment(in_files=[alnf], data_type=type,in_format="nexus", cores=1)
	sumf = os.path.join(f, "alignment.nex-summary.txt")
	aln.write_summaries(sumf)
	aln.write_taxa_summaries()
