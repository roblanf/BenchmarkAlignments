library('seqinr')
library('ape')

input = '~/Documents/github/PartitionedAlignments/datasets/Duchene_2015a/alignment.nex'

al <- as.alignment(read.nexus.data(input))

GC.content(as.DNAbin(al))