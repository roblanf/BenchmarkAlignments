# performs basic checks on the DB, and builds a CSV file ...

import yaml
import os
import logging
import csv
import glob


# first we get a list of all the datasets
# each one is a dataset that SHOULD have an associated .yaml readme
dataset_folders = [x[0] for x in os.walk(os.path.join(os.getcwd(), "datasets"))][1:]

dataset = {"has_yaml":"no",
		  "has_alignment":"no",
		  "has_cfg":"no",
		  "study_DOI":"NA",
		  "dataset_DOI":"NA",
		  "mitochondrial":"NA",
		  "nuclear":"NA",
		  "chloroplast":"NA",
		  "datatype":"NA",
		  "taxa":"NA",
		  "sites":"NA",
		  "datablocks":"NA",
		  "tree_inference":"NA",
		  "clade_latin":"NA",
		  "clade_english":"NA"}

headers = ["has_yaml", "has_alignment", "has_cfg", "study_DOI", "dataset_DOI", "mitochondrial", "nuclear", "chloroplast",
		  "datatype", "taxa", "sites", "datablocks", "tree_inference", "clade_latin", "clade_english"]

# read each file and extract the things you want, writing a csv as you go
results = []
for folder in dataset_folders:
	logging.info("Checking %s" %folder)

	result = dataset.copy()

	# 1. Check that the three files exist, at least in principle (maybe they're empty)
	files = os.listdir(folder)
	if files.count("README.yaml") == 1: 
		result["has_yaml"] = 'yes'
	else:
		logging.warning("couldn't find a YAML file for %s" %folder)

	if len(glob.glob(os.path.join(folder, "*.phy"))) > 0: 
		result["has_alignment"] = 'yes'
	else:
		logging.warning("couldn't find a .phy file for %s" %folder)

	if files.count("partition_finder.cfg") == 1: 
		result["has_cfg"] = 'yes'
	else:
		logging.warning("couldn't find a .cfg file for %s" %folder)


	# 2. parse that yaml file
	if result["has_yaml"] == 'yes':
		try:
			with open(os.path.join(folder, "README.yaml"), 'r') as f:
				doc = yaml.load(f)

			d = doc['dataset']
			result["study_DOI"] 	=  doc['study']['DOI']
			result["dataset_DOI"] 	=  d['DOI']
			result["mitochondrial"] =  d['mitochondrial']
			result["nuclear"] 		=  d['nuclear']
			result["chloroplast"] 	=  d['chloroplast']
			result["datatype"] 		=  d['datatype']
			result["taxa"]			=  d['number of taxa']
			result["sites"]			=  d['number of sites']
			result["datablocks"]	=  d['number of data blocks']
			result["tree_inference"]=  d['used for tree inference']
			result["clade_latin"]	=  d['study clade']['latin']
			result["clade_english"]	=  d['study clade']['english']


		except Exception, e:
			logging.warning("YAML file for %s is badly formatted, please fix" %folder)
			logging.warning("The problem is this: %s" %e)

	results.append(result)


# now write it out
f = open('summary.csv','wb')
w = csv.DictWriter(f, headers, extrasaction='ignore')
w.writeheader()
for r in results: 
	w.writerow(r)

f.close()