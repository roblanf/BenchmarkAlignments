# a little script to concatenate lots of nexus files in a folder
# and write a new one.
# cd to the infile before running

from Bio.Nexus import Nexus
import os
import argparse

def concatenate_loci(inpath):


    file_list = [x for x in os.walk(inpath)][0][2]
    print(file_list)

    #full_file_list = [[x, os.path.join(inpath, x)] for x in file_list]
    full_file_list = [[x, os.path.join(inpath, x)] for x in file_list] #

    print("loading files")
    nexi =  [(fname[0], Nexus.Nexus(fname[1])) for fname in full_file_list]

    print("combining alignments")
    combined = Nexus.combine(nexi)

    print("writing output")
    outpath = os.path.join(inpath, 'datasets')
    if not os.path.isdir(outpath):
        os.makedirs(outpath)
    outfile = os.path.join(outpath, "alignment.nex")
    outfile = open(outfile, 'w')
    combined.write_nexus_data(outfile)
    outfile.close()
    


# running
parser = argparse.ArgumentParser(description='')
parser.add_argument('--inpath', '-i', help='', 
                    required = True)
args = parser.parse_args()

if __name__ == '__main__':
    try:
       concatenate_loci(args.inpath)
    except Exception as e:
        print(e)
    