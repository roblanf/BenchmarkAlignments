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

# let's keep it simple and use a dictionary here
dataset = {"name":"NA",
          "study_DOI":"NA",
          "study_year":"NA",
          "dataset_DOI":"NA",
          "license":"NA",
          "root_age_timetree_mya":"NA",
          "root_age_study_mya":"NA",
          "clade_latin":"NA",
          "clade_english":"NA",
          "taxon_ID":"NA",
          "n_taxa":"NA",
          "n_sites":"NA",
          "n_datablocks":"NA",
          "gc_proportion":"NA",
          "gap_proportion":"NA",
          "a_proportion":"NA",
          "c_proportion":"NA",
          "g_proportion":"NA",
          "t_proportion":"NA"
          }

# read each file and extract the things you want, writing a csv as you go
results = []
warnings = 0
for folder in dataset_folders:

    folder = os.path.realpath(folder) # prettier
    logging.info("Checking %s" %folder)
    result = dataset.copy()
    result["name"] = os.path.basename(folder)
    
    # 1. Check that the two files exist, at least in principle (maybe they're empty)
    files = os.listdir(folder)
    if files.count("README.yaml") != 1: 
        logging.error("couldn't find a YAML file for %s" %folder)
        raise ValueError
    if files.count("alignment.nex") != 1: 
        logging.error("couldn't find alignment.phy file for %s" %folder)
        raise ValueError

    # clean up the folder: remove all files except the two we want
    extras = set(files) - set(['alignment.nex', 'README.yaml'])
    if extras:
        logging.info("Removing %d additional files", len(extras))
        for f in extras:
            os.remove(os.path.join(folder, f))
                
    # 2. parse the yaml file
    yaml_file = os.path.join(folder, "README.yaml")
    check_yaml(yaml_file)

    # 3. add yaml data to the result for this dataset
    result = add_yaml(yaml_file, result)

    # 4. check the alignment file
    alignment_file = os.path.join(folder, "alignment.nex")
    aln = check_alignment(alignment_file)
    result = add_alignment(aln, result)

    results.append(result)

logging.info("Database contains %d datasets" % ( len(dataset_folders)))


# now write it out
f = open('summary.csv','wb')
headers = dataset.keys()
w = csv.DictWriter(f, headers, extrasaction='ignore')
w.writeheader()

for r in results: 
    w.writerow(r)
    
f.close()
