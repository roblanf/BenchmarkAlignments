# python -m pytest, test cmd
# python -m pytest -x, stop after one failure
# python -m pytest -s, see print messages
# python -m pytest > ..path\pytest_log.txt, record the output.
import os
import pandas as pd
from Bio.Nexus import Nexus
import numpy as np
import itertools
from datetime import datetime
 

folder = "processing\\nex\\datasets" # prettier
files = os.listdir(folder)
alignment_file = os.path.join(folder, "alignment.nex")
charset_file = os.path.join(folder, "charset.csv")
df = pd.read_csv(charset_file)

aln = Nexus.Nexus()
aln.read(alignment_file)
all_sites = set(range(1, aln.nchar + 1))

def test_charpart_keys():
    x = df   
    
    assert 'alignment_name' in x.columns, "There should be a column named 'alignment_name'."
    assert 'partition_name' in x.columns, "There should be a column named 'partition_name'."
    assert 'partition_start' in x.columns, "There should be a column named 'partition_start'."
    assert 'partition_end' in x.columns, "There should be a column named 'partition_end'."
    assert 'partition_skip' in x.columns, "There should be a column named 'partition_skip'."
    assert 'locus_name' in x.columns, "There should be a column named 'locus_name'."
    assert 'codon_position' in x.columns, "There should be a column named 'codon_position'."
    assert 'genome' in x.columns, "There should be a column named 'genome'."
    assert 'data_type' in x.columns, "There should be a column named 'data_type'."
    print('\n\tcharset columns correct')
    

def test_partititons():
    x = df
    
    sites_range = []
    for i in range(len(x)):
        sites_list = list(np.arange(x.partition_start[i],x.partition_end[i] + 1, x.partition_skip[i]))
        sites_range = sites_range + sites_list
    sites = set(sites_range)
    
    assert all_sites.difference(sites) == set(), "The partitions charpartition does not cover the following sites: {}".format(all_sites.difference(sites))     
    assert sites.difference(all_sites) == set(), "The partitions charpartition has unexpected sites: {}".format(sites.difference(all_sites)) 
    print('\tpartitions sites correct')


def test_loci():
    x = df
    
    for i in range(len(x)):
        assert x.partition_name[i].split('_')[0] == x.locus_name[i], "The partition name {} doesn't match the locus name.".format(x.partition_name[i].split('_')[0])
    print('\tloci sites correct')


def test_genomes():
    x = df
    candi_gen_list = ['bacterial', 'chloroplast', 'dsDNA', 'dsRNA', 'mitochondrial', 'nuclear', 'ssDNA', 'ssRNA']
     
    assert all(gen in candi_gen_list for gen in x.genome), "unexpect name(s) in charset genomes: {}".format([gen for gen in x.genomes if gen not in candi_gen_list])
    print('\tgenomes sites correct')

now = datetime.now()
print('\npytest running date and time: ' + now.strftime('%Y-%m-%d %H:%M:%S'))