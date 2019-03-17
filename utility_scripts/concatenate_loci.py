# a little script to concatenate lots of nexus files in a folder
# and write a new one.
# cd to the infile before running

from Bio.Nexus import Nexus
from Bio import AlignIO
import os

infile  = "/Users/roblanfear/Desktop/prot_nex/"

file_list = [x for x in os.walk(infile)][0][2]
print(file_list)
file_list.remove(".DS_Store") # thanks Mac
nexi =  [(fname, Nexus.Nexus(fname)) for fname in file_list]
combined = Nexus.combine(nexi)
outfile = os.path.join(infile, "alignment.nex")
outfile = open(outfile, 'w')

combined.write_nexus_data(outfile)

outfile.close()