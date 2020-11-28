# convert a file full of alignments to nexus format
# just change the input format in the loop as appropriate
# and the alphabet

from Bio.Alphabet import generic_protein
from Bio import AlignIO
import os

infile  = "/Users/roblanfear/Dropbox/Projects_Current/benchmark_alignments_in_progress/Sanchez-Baracaldo_2017/loci"
outdir = "/Users/roblanfear/Dropbox/Projects_Current/benchmark_alignments_in_progress/Sanchez-Baracaldo_2017/loci_nex"

file_list = [x for x in os.walk(infile)][0][2]

try:
	file_list.remove(".DS_Store") # thanks Mac
except:
	pass

for f in file_list:
	print(f)
	a = AlignIO.read(open(os.path.join(infile, f)), "fasta")
	a._alphabet = generic_protein

	name = os.path.basename(f)
	outfile = os.path.join(outdir, name)

	AlignIO.write(a, outfile, "nexus")