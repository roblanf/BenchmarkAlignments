What's this?
------------

PartitionFinder datasets is a repository of datasets that are set up to be used with 
PartitionFinder (www.robertlanfear.com/partitionfinder), which is a program for performing
model selection and partitioning scheme selection. The point of this repository is to have 
a central place for all the datasets, to facilitate the development of new methods and 
algorithms for model selection in phylogenetics. 

All of the datasets are publicly available. Each folder here contains a published 
alignment of DNA or amino acid sequences, with information about the original study.

 
What's in the folders?
----------------------

Folder names have the first author, then the year of publication. If a single study has 
>1 dataset, then it will have an additional letter suffix, e.g. Lanfear_2012a.

Inside each folder is:
    1. A README file which contains the reference to the original paper and/or the dataset
       itself, plus any additional comments on the data (e.g. Taxon, number of spp, number
       of sites, etc).
    2. An alignment file in phylip format. This will be the original alignment described
       in the README, converted if necessary into phylip format.
    3. A partitionfinder.cfg file which describes the dataset for a PartitionFinder run.
       Most of the settings in this file are arbitrary, and are all identical. The only 
       settings that are not arbitrary/identical are the alignment name, and the
       description of the data blocks.
    4. Optionally, another file: commandlines.txt, which contains a series of example
       commandlines which demonstrate different types of analysis that can be carried out 
       in PartitionFinder using this dataset

All of the datasets in this file are publicly available, and links to the original data,
or descriptions of how it was obtained, are provided in the README file of each folder.
 
Can I use these datasets?
-------------------------
Yes. All of the original datasets are publicly available and can be re-used. If you use any
of the datasets, you MUST cite each original study, and the original datasets if they have 
their own DOIs. I provide copies of them here, as well as links to the original source of 
the data, and references for the original publication and the dataset if it has a separate
reference. 

I DO NOT own the copyright to these datasets, but all of them are in the public domain 
and some have their own licences.

Everything here that is not a dataset (the partitionfinder.cfg files and the README in 
each folder) is released under a CC-BY 3.0 license: 
http://creativecommons.org/licenses/by/3.0/deed.en_US)
full text here: http://creativecommons.org/licenses/by/3.0/legalcode

Attribution
-----------
If you use ANY of the datasets here, make sure to reference three things: 
    1. the original study,
    2. the dataset itself if the dataset has its own DOI (e.g. data dryad datasets have 
       their own DOI's and should be referenced separately). 
    3. This repository (github.com/roblanf/PartitionFinder_datasets)

This is essential to reward and acknowledge those who spend weeks and months in the field, 
laboriously chasing frogs/flied/lizards etc., then are kind enough to share their data 
with the world so that people like me (and you, if you're reading this) can re-use them 
for other things.

If you have any questions, or would like your dataset to be included here, or removed,
please contact me. Contact details are at www.robertlanfear.com/contact

Rob Lanfear
March 2012