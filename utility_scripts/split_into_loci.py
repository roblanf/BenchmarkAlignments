#!/usr/bin/env python3

# recursively find all benchmark alignment files and output information on individual loci
from Bio.Nexus import Nexus
import glob
import os
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-i", "--infolder", dest="infolder",
                    help="input file - input folder alignment from Benchmark Alignments database")

parser.add_argument("-o", "--outfolder", dest="outfolder",
                    help="output folder - existing folder to which to ouput single-locus alignments. Note that ")

args = parser.parse_args()


print(args)

alignments = glob.glob(os.path.join(args.infolder, '**', '*.nex'), recursive=True)

try:
    os.mkdir(args.outfolder)
    print("Directory ", args.outfolder,  "created") 
except FileExistsError:
    print("Directory ", args.outfolder,  " already exists")

for infile in alignments:

	print("Extracting loci from ", infile)

	aln = Nexus.Nexus()

	aln.read(infile)

	# first we get everything except the genomes
	all_charsets = list(aln.charsets.keys())

	# delete genome charsets
	charsets = list(filter(lambda x:'genome' not in x, all_charsets))

	# merge all loci with 1st, 2nd, and 3rd sites
	endings = ["_1stpos", "_2ndpos", "_3rdpos"]
	loci = {}
	for c in charsets:

		# a key for the locus dict
		key = c
		# the sites for this key
		c_sites = aln.charsets[key]

		for e in endings:
			if c.endswith(e):
				new_key = c[:-len(e)]
				break
		else:
			new_key = key

		# add the sites to any existing sites for that locus
		all_sites = loci.setdefault(new_key, [])
		all_sites += c_sites
		loci[new_key] = all_sites

	aln_folder = os.path.basename(os.path.dirname(infile))

	# prepend the alignment name to the output files
	out_path = os.path.join(args.outfolder, aln_folder)	

	# output loci
	aln.write_nexus_data_partitions(filename=out_path, charpartition=loci)