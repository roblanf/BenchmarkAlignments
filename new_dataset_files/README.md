How to add a dataset
====================

What you need
-------------

1. A DNA or amino acid alignment from a published paper

2. Information on the loci in that alignment, including codon positions


What you do
-----------

1. Make a new folder in the /datasets folder

2. Name it after the first author and year of publication (e.g. Brown_2012)

3. Copy the README.yaml and partitionfinder.cfg files from this folder into that one

4. Fill in the README and .cfg files


Before you commit a new dataset
-------------------------------

1. Check you have completed the ENTIRE README.yaml file

2. Check that the dataset actually runs in PartitionFinder. The run doesn't have to finish
    but it has to get started.

3. Run the generate_csv.py script - this performs some basic checks on your addition, and 
    adds it to the summary file. 

4. DO NOT commit incomplete datasets, or any that generate warnings when you run the 
    script. Fix all errors first, then commit.

Conventions
-----------

When naming datablocks, provide as much information as possible, and label as many 
datablocks as you possibly can. The best example of this is the mtgenome dataset in the 
/datasets/Leavitt_2013 file. Take a look at the 87 meticulously annotated data blocks.

Other than the data_blocks and the alignment name, leave all other aspects of the .cfg 
file the same.

In the README.yaml file, fill out everything. But most importantly, make sure you get the
reference and the DOI of the origial manuscript and the original dataset (if it has one).

Don't change the structure of the yaml file, or delete any entries. Leave things blank if 
you have no information.

If the dataset isn't publicly available, don't put it in the repository.

For datasets without explicit licenses, always contact the owners of the dataset to ask 
whether we can put it in the repository, and whether we can release it under a CC0 license.
If they don't agree, don't put it in the repository. Assume that data sets on TreeBase are
O.K., since they're already publicly available.