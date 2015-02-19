How to add a dataset
====================

What you need
-------------

1. A DNA, amino acid, morphology, or language alignment from a published paper.

2. Permission to archive that alignment with a CC0 license. (This is important)

3. Lots of additional information on the alignment, including:

    (i) Where the loci are (AKA partition boundaries)

    (ii) Which genome (mitochondrial, nuclear, chloroplast) each locus comes from

    (iii) Codon positions (for protein-coding DNA datasets)

    (iv) Ages of sequences (e.g. for aDNA or virus datasets)


What you do
-----------

1. Convert your alignment to NEXUS format.

2. Copy the partitions information into the correct block in the NEXUS file. (I.e. loci and codon positions)

3. Add information to the NEXUS block on which genome each column comes from.

4. If you have heterochronous data, create an ages.csv file, and populate it with the sampling dates of all taxa.

5. Make a new folder in the /datasets folder

6. Name it after the first author and year of publication (e.g. Brown_2012)

7. Copy the README.yaml into the folder. Fill in ALL fields.

8. Add in the dataset itself, in NEXUS format, and named alignment.nex


Before you commit a new dataset
-------------------------------

1. Check you have completed the ENTIRE README.yaml file

2. Run the generate_csv.py script - this performs some basic checks on your addition, and adds it to the summary file.

4. DO NOT commit incomplete datasets, or any that generate warnings when you run the script. Fix all errors first, then commit.

Conventions
-----------

When naming datablocks, provide as much information as possible, and label as many
datablocks as you possibly can. The best example of this is the mtgenome dataset in the
/datasets/Leavitt_2013 file. Take a look at the 87 meticulously annotated data blocks.

In the README.yaml file, fill out everything. But most importantly, make sure you get the
reference and the DOI of the origial manuscript and the original dataset (if it has one).

Don't change the structure of the yaml file, or delete any entries. Leave things blank if
you have no information.

For datasets without explicit licenses, always contact the owners of the dataset to ask 
whether we can put it in the repository, and whether we can release it under a CC0 license.
If they don't agree, don't put it in the repository. Assume that data sets on TreeBase are
O.K., since they're already publicly available.
