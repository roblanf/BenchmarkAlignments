# convert a file full of alignments to nexus format
# just change the input format in the loop as appropriate
# and the alphabet

import os
import shutil
import argparse

def conver_to_nexus(inpath, outdir, rootpath, informat):

    outpath = os.path.join(inpath, outdir)
    if not os.path.isdir(outpath):
        os.makedirs(outpath)

    file_list = [x for x in os.walk(inpath)][0][2]


    for f in file_list:
        cmd = r'python AMAS.py convert -d aa -f ' + informat + ' -i '+ inpath + '\\' + f +' -u nexus'
        os.system(cmd)
        fnex = f + '-out.nex'
        
        outfile = os.path.join(outpath, fnex)
        shutil.move(fnex, outfile)
    

        
        
# running
parser = argparse.ArgumentParser(description='')
parser.add_argument('--inpath', '-i', help='', 
                    default = r"C:\Users\u7151703\Desktop\research\datasets\processing")
parser.add_argument('--outdir', '-o', help='', 
                    default = "nex")
parser.add_argument('--rootpath', '-r', help='', 
                    default = r"C:\Users\u7151703")
parser.add_argument('--informat', '-f', help='', 
                    default = 'phylip')
args = parser.parse_args()

if __name__ == '__main__':
    try:
       conver_to_nexus(args.inpath, args.outdir, args.rootpath, args.informat)
    except Exception as e:
        print(e)
