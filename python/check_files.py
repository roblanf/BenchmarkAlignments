# performs basic checks on the DB, and builds a CSV file ...

import os
import logging
import csv
import glob
from util_functions import *

logging.basicConfig(format='%(levelname)s:\t%(asctime)s:\t%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

# first we get a list of all the datasets
# each one is a dataset that SHOULD have an associated .yaml readme
dataset_folders = [x[0] for x in os.walk(os.path.join(os.getcwd(), "../datasets"))][1:]

#logging.info("Found these %d datasets %s" %(len(dataset_folders), dataset_folders))

# read each file and extract the things you want, writing a csv as you go
warnings = 0

for folder in dataset_folders:

    folder = os.path.realpath(folder) # prettier
    logging.info("Checking %s" %folder)
    zipflag = 0
    
    # 1. Check that the two files exist, at least in principle (maybe they're empty)
    files = os.listdir(folder)
    if files.count("README.yaml") != 1: 
        logging.error("couldn't find a YAML file for %s" %folder)
        raise ValueError

    if files.count("alignment.nex.tar.gz") == 1:
        command = "tar -zxvf %s -C %s" %(os.path.join(folder, "alignment.nex.tar.gz"), folder)
        os.system(command)
        zipflag = 1
        files = os.listdir(folder)


    if files.count("alignment.nex") != 1:
        logging.error("couldn't find alignment.nex file for %s" %folder)
        raise ValueError

    # clean up the folder: remove all files except the two we want
    extras = set(files) - set(['alignment.nex', 'README.yaml', 'alignment.nex-seq-summary.txt', 'alignment.nex-summary.txt', 'alignment.nex.tar.gz'])
    if extras:
        logging.info("Removing %d additional files", len(extras))
        for f in extras:
            os.remove(os.path.join(folder, f))
                
    # 2. parse the yaml file
    yaml_file = os.path.join(folder, "README.yaml")
    check_yaml(yaml_file)

    # 4. check the alignment file
    alignment_file = os.path.join(folder, "alignment.nex")
    aln = check_alignment(alignment_file)

    # 5. clean up the unzipped file if necessary
    if zipflag==1:
        os.system("rm %s" %(os.path.join(folder, "alignment.nex")))

logging.info("Database contains %d datasets" % ( len(dataset_folders)))

