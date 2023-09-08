# python -m pytest, test cmd
# python -m pytest -x, stop after one failure
# python -m pytest -s, see print messages
# python -m pytest > ..path\pytest_log.txt, record the output. Mine: C:\Users\u7151703\Desktop\research\datasets\processing\nex\datasets\pytest_log.txt
import os
import pandas as pd
from Bio.Nexus import Nexus
import itertools
from datetime import datetime
 

folder = r"C:\Users\u7151703\Desktop\research\datasets\processing\nex\datasets" # prettier    
files = os.listdir(folder)
alignment_file = os.path.join(folder, "alignment.nex")
charset_file = os.path.join(folder, "charset.csv")
df = pd.read_csv(charset_file)

def test_charpart_keys():
    x = df   
    
    assert 'partitions' in x.columns, "There should be a column named 'partitions'."
    assert 'loci' in x.columns, "There should be a column named 'loci'."
    assert 'genomes' in x.columns, "There should be a column named 'genomes'."
    print('\n\tcharset columns correct')
    

def test_partititons():
    aln = Nexus.Nexus()
    aln.read(alignment_file)
    all_sites = set(range(aln.nchar))
    
    x = df.dropna(subset=['partitions'])
    
    site_length = 0
    sites_range = []
    for i in range(len(x)):
        site_length = site_length + x.par_end[i] + 1 - x.par_start[i]
        sites_range.append(range(int(x.par_start[i]) - 1, int(x.par_end[i])))
    sites = set((itertools.chain.from_iterable(sites_range)))
    
    #assert site_length == len(all_sites), "The partitions charpartition has {} more/less site(s) than the number of sites in the alignment".format(abs(site_length - len(all_sites)))
    assert all_sites.difference(sites) == set(), "The partitions charpartition does not cover the following sites: {}".format(all_sites.difference(sites))     
    assert sites.difference(all_sites) == set(), "The partitions charpartition has unexpected sites: {}".format(sites.difference(all_sites)) 
    print('\tpartitions sites correct')


def test_loci():
    aln = Nexus.Nexus()
    aln.read(alignment_file)
    all_sites = set(range(aln.nchar))
    
    x = df.dropna(subset=['loci'])
    
    site_length = 0
    sites_range = []
    for i in range(len(x)):
        site_length = site_length + x.loci_end[i] + 1 - x.loci_start[i]
        sites_range.append(range(int(x.loci_start[i]) - 1, int(x.loci_end[i])))
    sites = set((itertools.chain.from_iterable(sites_range)))
    
    assert site_length == len(all_sites), "The loci charpartition has {} more/less site(s) than the number of sites in the alignment".format(abs(site_length - len(all_sites)))
    assert all_sites.difference(sites) == set(), "The loci charpartition does not cover the following sites: {}".format(all_sites.difference(sites))     
    assert sites.difference(all_sites) == set(), "The loci charpartition has unexpected sites: {}".format(sites.difference(all_sites)) 
    print('\tloci sites correct')


def test_genomes():
    aln = Nexus.Nexus()
    aln.read(alignment_file)
    all_sites = set(range(aln.nchar))
    
    x = df.dropna(subset=['genomes'])
    
    site_length = 0
    sites_range = []
    for i in range(len(x)):
        site_length = site_length + x.gen_end[i] + 1 - x.gen_start[i]
        sites_range.append(range(int(x.gen_start[i]) - 1, int(x.gen_end[i])))
    sites = set((itertools.chain.from_iterable(sites_range)))
    
    assert site_length == len(all_sites), "The genomes charpartition has {} more/less site(s) than the number of sites in the alignment".format(abs(site_length - len(all_sites)))
    assert all_sites.difference(sites) == set(), "The genomes charpartition does not cover the following sites: {}".format(all_sites.difference(sites))     
    assert sites.difference(all_sites) == set(), "The genomes charpartition has unexpected sites: {}".format(sites.difference(all_sites)) 
    print('\tgenomes sites correct')

now = datetime.now()
print('\npytest running date and time: ' + now.strftime('%Y-%m-%d %H:%M:%S'))