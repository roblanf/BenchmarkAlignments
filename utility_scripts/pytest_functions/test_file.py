# python -m pytest test cmd
# python -m pytest -x, stop after one failure
import os
import yaml
import pytest
import requests
from Bio.Nexus import Nexus
import itertools
#from urllib.request import urlopen
 

folder = r"C:\Users\u7151703\Desktop\research\datasets\processing\nex\datasets" # prettier    
files = os.listdir(folder)
yaml_file = os.path.join(folder, "README.yaml")  
alignment_file = os.path.join(folder, "alignment.nex")


def test_existing():
    assert files.count("README.yaml") == 1, "couldn't find README.yaml file"
    assert files.count("alignment.nex") == 1, "couldn't find alignment.nex"
    
    
def test_extra_file():
    extras = set(files) - set(['alignment.nex', 'README.yaml', 'alignment.nex-seq-summary.txt', 'alignment.nex-summary.txt'])
    assert len(extras) == 0, "There are extra file(s)"


def test_yaml_titles():
    y = yaml.load(open(yaml_file, 'r'),Loader=yaml.FullLoader)

    assert set(y.keys()) == set(['study', 'dataset']),"Missing 'study' or 'dataset' section from your yaml file"
    assert set(y["study"].keys()) == set(['DOI', 'reference', 'year']),"The sections of your 'study' section should be 'reference', 'year', and 'DOI'"
    assert set(y["dataset"].keys()) == set(['DOI', 'license', 'used for tree inference', 'notes', 'study clade', 'timetree root age', 'study root age', 'alignment', 'genomes']),"The sections of your 'dataset' section should be 'DOI', 'license', 'used for tree inference', 'notes', 'study clade', 'timetree root age', 'study root age'"
    assert set(y["dataset"]["study clade"].keys()) == set(['english', 'latin', 'taxon ID']),"The sections of your 'study clade' section should be 'english', 'latin', 'taxon ID'"
    assert set(y["dataset"]["alignment"].keys()) == set(['ntax', 'nchar', 'datatype', 'partitions']),"The sections of your 'alignment' section should be 'ntax', 'nchar', 'datatype', and 'partitions'"
    assert set(y["dataset"]["genomes"].keys()) == set(['mitochondrial', 'nuclear', 'chloroplast', 'dsDNA', 'ssDNA', 'dsRNA', 'ssRNA', 'bacterial']),"The sections of your 'genomes' section should be 'mitochondrial', 'nuclear', 'chloroplast', 'dsDNA', 'ssDNA', 'dsRNA', 'ssRNA', and 'bacterial'"


def test_yaml_doi():
    y = yaml.load(open(yaml_file, 'r'),Loader=yaml.FullLoader)
    response_s = requests.get("".join(["http://", y['study']['DOI']]))
    response_d = requests.get("".join(["http://", y['dataset']['DOI']]))
    
    assert response_s.status_code == 403 or response_s.status_code == 200, "this URL didn't work: {}".format("".join(["http://", y['study']['DOI']]))
    assert response_d.status_code == 403 or response_d.status_code == 200, "this URL didn't work: {}".format("".join(["http://", y['dataset']['DOI']]))
   

def test_license():
    y = yaml.load(open(yaml_file, 'r'),Loader=yaml.FullLoader)
    
    assert y['dataset']['license'] in ["CC0", "CCBY"], "The license for the dataset must be CC0 or CCBY"
    
    
def test_aln_block():
    y = yaml.load(open(yaml_file, 'r'),Loader=yaml.FullLoader)
    aln = y['dataset']['alignment']
    
    assert isinstance(aln['datatype'], str), "The datatype must be a string"
    assert aln['datatype'] in ["nucleotide", "protein"], "The datatype must be a 'nucleotide' or 'protein'"
    assert isinstance(aln['ntax'], int),"ntax must be a number"
    assert isinstance(aln['nchar'], int), "nchar must be a number"
    assert isinstance(aln['partitions'], int), "partitions must be a number"
    

def test_genomes():
    y = yaml.load(open(yaml_file, 'r'),Loader=yaml.FullLoader)
    gen = y['dataset']['genomes']
    
    responses = set([gen['mitochondrial'],
                    gen['nuclear'],
                    gen['chloroplast'],
                    gen['dsDNA'],
                    gen['ssDNA'],
                    gen['dsRNA'],
                    gen['ssRNA'],
                    gen['bacterial']])
    
    assert responses.issubset(set([True, False])), "All entries in the 'genome' section must be either 'yes' or 'no'"
    
    
def test_tree():
    y = yaml.load(open(yaml_file, 'r'),Loader=yaml.FullLoader)
    text = y['dataset']['used for tree inference']
    
    
    assert text in [True, False], "The 'used for tree inference' section must be 'yes' or 'no'"
    

def test_timetree_age():
    y = yaml.load(open(yaml_file, 'r'),Loader=yaml.FullLoader)
    age = y['dataset']['timetree root age']
    
    if age == "NA":
        pytest.skip()
    
    assert len(age.split()) <= 2, "There's a problem with this age: {}. It should be 'x mya', where x is a number".format(age)
    
    try:
        t = float(age.split()[0])
    except:
        raise AssertionError("Check the timetree root age (%s). It looks like it's not a number" % age.split()[0])
    assert t < 3000 and t > 0, "Check the timetree root age. It's too big or too small"
    assert age.split()[1] == 'mya', "The number in the root age should be followed by 'mya' as units."
    
    
def test_study_age():
    y = yaml.load(open(yaml_file, 'r'),Loader=yaml.FullLoader)
    age = y['dataset']['study root age']
    
    if age == "NA":
        pytest.skip()
    
    assert len(age.split()) <= 2, "There's a problem with this age: {}. It should be 'x mya', where x is a number".format(age)
    
    try:
        t= float(age.split()[0])
    except:
        raise AssertionError("Check the study root age (%s). It looks like it's not a number" % age.split()[0])
    assert t < 3000 and t > 0, "Check the study root age. It's too big or too small"
    assert age.split()[1] == 'mya', "The number in the study root age should be followed by 'mya' as units."
    
def test_genbank_taxanomy():
    y = yaml.load(open(yaml_file, 'r'),Loader=yaml.FullLoader)
    clade = y['dataset']['study clade']

    assert isinstance(clade['latin'], str), "The latin clade must be a string"
    assert isinstance(clade['english'], str), "The latin clade must be a string"
    assert isinstance(clade['taxon ID'], int), "The taxon ID must be a number"

    response = requests.get("".join(['http://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=', str(clade['taxon ID'])]))
    assert response.status_code == 403 or response.status_code == 200,  "this taxon ID didn't work"


def test_read_aln():
    aln = Nexus.Nexus()
    try:
        aln.read(alignment_file)
    except:
        raise AssertionError("Couldn't read nexus file, please check and try again.")


def test_charpart_keys():
    aln = Nexus.Nexus()
    aln.read(alignment_file)
    assert list(aln.charpartitions.keys()) == ['loci', 'genomes'], "There should be exactly two CHARPARTITIONS: 'loci' and 'genomes'. Check and try again."
    assert list(aln.taxsets.keys()) == ['outgroups'], "There should be exactly one TAXSET: 'outgroups'. Check and try again."
    

def test_charpart_length():
    aln = Nexus.Nexus()
    aln.read(alignment_file)
    
    all_sites = set(range(aln.nchar))
    loci_sites = [x[1] for x in aln.charpartitions['loci'].items()]
    loci_sites = list(itertools.chain.from_iterable(loci_sites))

    assert len(loci_sites) <= len(all_sites), "The loci charpartition has {} more/less site(s) than the number of sites in the alignment".format(len(loci_sites) - len(all_sites))
    assert len(set(loci_sites)) >= len(all_sites), "The loci charpartition does not cover the following sites, please fix: {}".format(all_sites.difference(set(loci_sites)))

    geno_sites = [x[1] for x in aln.charpartitions['genomes'].items()]
    geno_sites = list(itertools.chain.from_iterable(geno_sites))
    
    assert len(geno_sites) <= len(all_sites), "The genomes charpartition has {} more/less site(s) than the number of sites in the alignment".format(len(loci_sites) - len(all_sites))
    assert len(set(geno_sites)) >= len(all_sites), "The genomes charpartition does not cover the following sites, please fix: {}".format(all_sites.difference(set(loci_sites)))
    
    
    
    
    
    
    
    
    
    
    
    
    