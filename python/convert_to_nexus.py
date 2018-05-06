# convert a file full of alignments to nexus format
# just change the input format in the loop as appropriate
# and the alphabet

from Bio.Alphabet import generic_protein
from Bio import AlignIO
import os

infile  = "/Users/roblanfear/Downloads/alignments/0DP-4593_single_genes"
outdir = "/Users/roblanfear/Downloads/alignments/nexus"

file_list = [x for x in os.walk(infile)][0][2]

for f in file_list:

	a = AlignIO.read(open(f), "fasta")
	a._alphabet = generic_protein

	name = os.path.basename(f)
	outfile = os.path.join(outdir, name)

	AlignIO.write(a, outfile, "nexus")