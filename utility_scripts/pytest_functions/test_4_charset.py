# python -m pytest, test cmd
# python -m pytest -x, stop after one failure
# python -m pytest -s, see print messages
import os
import pandas as pd
from Bio.Nexus import Nexus
import itertools
 

folder = r"C:\Users\u7151703\Desktop\research\datasets\processing\nex\datasets" # prettier    
files = os.listdir(folder)
yaml_file = os.path.join(folder, "README.yaml")  
alignment_file = os.path.join(folder, "alignment.nex")
charset_file = os.path.join(folder, "charset.xlsx")


def test_charpart_keys():
    x = pd.ExcelFile(charset_file)
    
    assert 'loci' in x.sheet_names, "There should be a sheet named 'loci'."
    assert 'genomes' in x.sheet_names, "There should be a sheet named 'genomes'."
    print('\n\tcharset sheets correct')
    

def test_loci():
    aln = Nexus.Nexus()
    aln.read(alignment_file)
    all_sites = set(range(aln.nchar))
    
    x = pd.read_excel(charset_file, sheet_name= 'loci' , engine='openpyxl')
    
    site_length = 0
    sites_range = []
    for i in range(len(x)):
        site_length = site_length + x.end[i] + 1 - x.start[i]
        sites_range.append(range(x.start[i] - 1, x.end[i]))
    sites = set((itertools.chain.from_iterable(sites_range)))
    
    assert site_length == len(all_sites), "The loci charpartition has {} more/less site(s) than the number of sites in the alignment".format(abs(site_length - len(all_sites)))
    assert all_sites.difference(sites) == set(), "The loci charpartition does not cover the following sites: {}".format(all_sites.difference(sites))     
    assert sites.difference(all_sites) == set(), "The loci charpartition has unexpected sites: {}".format(sites.difference(all_sites)) 
    print('\nloci sites correct')


def test_genomes():
    aln = Nexus.Nexus()
    aln.read(alignment_file)
    all_sites = set(range(aln.nchar))
    
    x = pd.read_excel(charset_file, sheet_name= 'genomes' , engine='openpyxl')
    
    site_length = 0
    sites_range = []
    for i in range(len(x)):
        site_length = site_length + x.end[i] + 1 - x.start[i]
        sites_range.append(range(x.start[i] - 1, x.end[i]))
    sites = set((itertools.chain.from_iterable(sites_range)))
    
    assert site_length == len(all_sites), "The genomes charpartition has {} more/less site(s) than the number of sites in the alignment".format(abs(site_length - len(all_sites)))
    assert all_sites.difference(sites) == set(), "The genomes charpartition does not cover the following sites: {}".format(all_sites.difference(sites))     
    assert sites.difference(all_sites) == set(), "The genomes charpartition has unexpected sites: {}".format(sites.difference(all_sites)) 
    print('\ngenomes sites correct')
