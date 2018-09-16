# generates AMAS summaries for all datasets, only where they are missing

import AMAS
from Bio.Nexus import Nexus
import os
import glob

cores = 4

all_files = glob.glob(os.path.abspath(os.path.join(os.getcwd(),'..','datasets','**')), recursive=False)

print(all_files)

for f in all_files:
	alnf = os.path.join(f, 'alignment.nex')

	print(alnf)

	sumf = os.path.join(f, "alignment.nex-summary.txt")
	taxf = os.path.join(f, "alignment.nex-seq-summary.txt")

	if os.path.isfile(sumf)==True and os.path.isfile(taxf)==True:
		pass
	else:
		splitflag = 1
		if(os.path.isfile(f)):
			splitflag = 0

		if(splitflag==1):
			# make the alignment
			folder = os.path.dirname(alnf)
			command = "cat %s > %s" %(os.path.join(folder, 'alignment_split', 'alignment.nex.*'), os.path.join(folder, 'alignment.nex'))
			os.system(command)


		# get the data type
		dat = Nexus.Nexus()
		dat.read(alnf)
		if(dat.datatype=='nucleotide'): type = 'dna'
		if(dat.datatype=='protein'): type= 'aa'

		# get the AMAS summaries
		aln = AMAS.MetaAlignment(in_files=[alnf], data_type=type,in_format="nexus", cores=cores)
		aln.write_summaries(sumf)
		aln.write_taxa_summaries()

		# remove a large alignment if you made one
		if(splitflag==1):
			os.system("rm %s" %(os.path.join(folder, "alignment.nex")))

