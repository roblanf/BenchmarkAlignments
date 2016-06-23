# a little script to concatenate lots of nexus files in a folder
# and write a new one.
from Bio.Nexus import Nexus
import os

infile  = "/Users/robertlanfear/Desktop/turtles-individual-nexus-files-for-loci"


file_list = [x for x in os.walk(infile)][0][2]
nexi =  [(fname, Nexus.Nexus(fname)) for fname in file_list]
combined = Nexus.combine(nexi)
outfile = os.path.join(infile, "alignment.nex")
combined.write_nexus_data(filename=open(outfile, 'w'))