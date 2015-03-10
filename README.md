PartitionFinder datasets repository
===================================

What's this?
------------

A curated repository of DNA and amino acid alignments with comprehensive metadata.

All of the datasets are publicly available. Each folder here contains a published
alignment of DNA or amino acid sequences (alignment.nex), and a file with fairly comprehensive metadata about the original study and the dataset itself (readme.yaml).

There is also a summary.csv file, which includes the important information on all of the datasets, so that you can select just the ones that you want.

What's it for?
--------------

To test, verify, benchmark, and compare software and methods in phylogenetics.

Lots of people around the world are working on developing new methods and software in phylogenetics. But despite the existence of some useful databases (e.g. TreeBase, DataDryad), most new methods and software are only applied to a very small collection of datasets. In my own experience, this is because it's surprisingly difficult to find appropriate datasets from the existing databases.

I hope this repository helps solve that problem. It provides a set of curated datasets with fairly exhaustive metadata (as exhaustive as we could be). This should make it relatively straightforward to test new methods and software on tens or hundreds of datasets.


What's in the folders?
----------------------

Inside each folder is:

1.  A README.yaml file which contains the reference to the original paper and/or the dataset itself, plus any additional comments on the data (e.g. Taxon, number of spp, number of sites, etc).

2.  An alignment file in nexus format. This will be the original alignment described in the README, converted if necessary into phylip format, and with any modifications (e.g. removal of morphological characters) listed in the notes section of the README.yaml.


Can I use these datasets?
-------------------------
Yes. All of the original datasets are publicly available and can be re-used. The datasets themselves are all released under a CC0 license (either because they come from Dryad, or because I have asked the authors whether I can release their data under this license).

Everything here that is not a dataset (the partitionfinder.cfg files and the README in each folder) is released under a CC-BY 3.0 license: http://creativecommons.org/licenses/by/3.0/deed.en_US) full text here: http://creativecommons.org/licenses/by/3.0/legalcode

Attribution
-----------
If you use any of the datasets here, please make sure to reference three things:

1.  The original study,

2.  The dataset itself if the dataset has its own DOI (e.g. data dryad datasets have their own DOI's and should be referenced separately).

3.  This repository (github.com/roblanf/Alignments)

This is essential to reward and acknowledge those who spend weeks and months in the field, laboriously chasing frogs/flied/lizards etc., then are kind enough to share their data with the world so that people like me (and you, if you're reading this) can re-use them
for other things.

If you have any questions, or would like your dataset to be included here, or removed, please contact me. Contact details are at www.robertlanfear.com/contact

Rob Lanfear
March 2015
