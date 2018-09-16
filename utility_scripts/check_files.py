# performs basic checks on the DB, and builds a CSV file ...

import os
import logging
import csv
import glob
from util_functions import *




logging.basicConfig(format='%(levelname)s:\t%(asctime)s:\t%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

# first we get a list of all the datasets
# each one is a dataset that SHOULD have an associated .yaml readme
dataset_folders = [x[0] for x in walklevel(os.path.join(os.getcwd(), "../datasets"))][1:]


logging.info("Found %d datasets" %(len(dataset_folders)))
for f in dataset_folders:
	logging.info("    %s", f)

# read each file and extract the things you want, writing a csv as you go
warnings = 0

for folder in dataset_folders:

    folder = os.path.realpath(folder) # prettier
    logging.info("Checking %s" %folder)
    splitflag = 0
    
    # 1. Check that the two files exist, at least in principle (maybe they're empty)
    files = os.listdir(folder)
    if files.count("README.yaml") != 1: 
        logging.error("couldn't find a YAML file for %s" %folder)
        raise ValueError
    logging.info("    found YAML file")

    if files.count("alignment_split") == 1: #only here if the alignment is >100MB
    	# so now we make the alignment.nex file so we can check it
        logging.info("    joining split alignments into single alignment.nex")
        command = "cat %s > %s" %(os.path.join(folder, 'alignment_split', 'alignment.nex.*'), os.path.join(folder, 'alignment.nex'))
        os.system(command)
        splitflag = 1
        files = os.listdir(folder)

    if files.count("alignment.nex") != 1:
        logging.error("couldn't find alignment.nex file for %s" %folder)
        raise ValueError

    logging.info("    found alignment.nex file")

    # clean up the folder: remove all files except the two we want
    extras = set(files) - set(['alignment_split', 'alignment.nex', 'README.yaml', 'alignment.nex-seq-summary.txt', 'alignment.nex-summary.txt'])
    if extras:
        logging.info("    removing %d additional file(s)", len(extras))
        for f in extras:
            logging.info("        %s" %(f))
            os.remove(os.path.join(folder, f))
                
    # 2. parse the yaml file
    logging.info("    checking YAML file")
    yaml_file = os.path.join(folder, "README.yaml")
    check_yaml(yaml_file)

    # 4. check the alignment file
    logging.info("    checking alignment.nex file")

    alignment_file = os.path.join(folder, "alignment.nex")
    aln = check_alignment(alignment_file)

    # 5. split up large alignment files if necessary
    # this is coded so that we split up any alignment >100MB, since that's the github limit
    if os.path.getsize(os.path.join(folder, "alignment.nex")) >= 100000000.0:

        if splitflag == 0:
            logging.info("    splitting alignment because it's larger than 100MB")
            os.system('mkdir %s' %(os.path.join(folder, 'alignment_split')))
            command = 'split -b 50m %s %s' %(os.path.join(folder, "alignment.nex"), os.path.join(folder, 'alignment_split', 'alignment.nex.'))
            os.system(command)

        # remove the original, but only if we managed to zip it successfully
        files = os.listdir(os.path.join(folder, 'alignment_split'))
        if files.count("alignment.nex.aa") == 1:
            logging.info("    removing large raw alignment file")
            os.system("rm %s" %(os.path.join(folder, "alignment.nex")))

    logging.info("    done, no errors found")

logging.info("Database contains %d datasets" % ( len(dataset_folders)))
logging.info("All datasets checked and no errors detected")

