# translate a bunch of alignments
# cd to the folder with the alignments to be translated first

import os

# input file, can't be NEXUS alignments
infile  = "/Users/roblanfear/Dropbox/Projects_Current/benchmark_alignments_in_progress/Wu_2018_aa/cds_aa"
outdir = "/Users/roblanfear/Dropbox/Projects_Current/benchmark_alignments_in_progress/Wu_2018_aa/cds_aa_nex"

file_list = [x for x in os.walk(infile)][0][2]

try:
	file_list.remove(".DS_Store") # thanks Mac
except:
	pass

for f in file_list:
	print(f)

	name = os.path.basename(f)
	outfile = os.path.join(outdir, name)

	print(name, outfile)

	cmd = "~/Desktop/iqtree -st NT2AA -s %s -ao %s" %(name, outfile)

	os.system(cmd)