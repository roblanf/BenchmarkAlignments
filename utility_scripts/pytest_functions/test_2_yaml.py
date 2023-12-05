# python -m pytest, test cmd
# python -m pytest -x, stop after one failure
# python -m pytest -s, see print messages
# python -m pytest > ..path\pytest_log.txt, record the output. Mine: C:\Users\u7151703\Desktop\research\datasets\processing\nex\datasets\pytest_log.txt
import os
import yaml
import pytest
import requests
 

folder = "processing\\nex\\datasets" # prettier 
yaml_file = os.path.join(folder, "README.yaml")  


def test_yaml_titles():
    y = yaml.load(open(yaml_file, 'r'),Loader=yaml.FullLoader)

    assert set(y.keys()) == set(['study', 'dataset']),"Missing 'study' or 'dataset' section from your yaml file"
    assert set(y["study"].keys()) == set(['DOI', 'reference', 'year']),"The sections of your 'study' section should be 'reference', 'year', and 'DOI'"
    assert set(y["dataset"].keys()) == set(['DOI', 'license', 'figshare', 'dataset curation', 'used for tree inference', 'timetree', 'study root age', 'study clade', 'outgroups', 'notes']),"The sections of your 'dataset' section should be 'DOI', 'license', 'figshare', 'dataset curation', 'used for tree inference', 'timetree', 'study root age', 'study clade', 'outgroups', 'notes'"
    assert set(y["dataset"]["dataset curation"].keys()) == set(['alignment file', 'partition information', 'justification', 'sequence edits']),"The sections of your 'dataset curation' section should be 'alignment file', 'partition information', 'justification', 'sequence edits'"
    assert set(y["dataset"]["used for tree inference"].keys()) == set(['concatenated', 'locus trees']),"The sections of your 'study clade' section should be 'concatenated', 'locus trees'"
    assert set(y["dataset"]["timetree"].keys()) == set(['timetree species 1', 'timetree species 2', 'date accessed', 'timetree root age', 'timetree lower CI', 'timetree upper CI', 'timetree N']),"The sections of your 'timetree' section should be 'timetree species 1', 'timetree species 2', 'date accessed', 'timetree root age', 'timetree lower CI', 'timetree upper CI', 'timetree N'"
    assert set(y["dataset"]["study clade"].keys()) == set(['english', 'latin', 'taxon ID']),"The sections of your 'study clade' section should be 'english', 'latin', 'taxon ID'"
    print('\n\tyaml file structure correct')


def test_yaml_doi():
    y = yaml.load(open(yaml_file, 'r'),Loader=yaml.FullLoader)
    response_s = requests.get("".join(["http://", y['study']['DOI']]))
    response_d = requests.get("".join(["http://", y['dataset']['DOI']]))
    
    assert response_s.status_code == 403 or response_s.status_code == 200, "this URL didn't work: {}".format("".join(["http://", y['study']['DOI']]))
    assert response_d.status_code == 403 or response_d.status_code == 200, "this URL didn't work: {}".format("".join(["http://", y['dataset']['DOI']]))
    print('\tdoi correct')
    

def test_license():
    y = yaml.load(open(yaml_file, 'r'),Loader=yaml.FullLoader)
    
    assert y['dataset']['license'] in ["CC0", "CCBY"], "The license for the dataset must be CC0 or CCBY"
    print('\tlicense correct')
        

def test_figshare():
    y = yaml.load(open(yaml_file, 'r'),Loader=yaml.FullLoader)
    response_f = requests.get("".join(["http://", y['dataset']['figshare']]))
    
    assert response_f.status_code == 403 or response_f.status_code == 200, "The figshare URL didn't work."
    print('\tfigshare link correct')


def test_data_curation():
    y = yaml.load(open(yaml_file, 'r'),Loader=yaml.FullLoader)
    aln_file = y['dataset']['dataset curation']['alignment file']
    par_file = y['dataset']['dataset curation']['partition information']
    justification = y['dataset']['dataset curation']['justification']
    edits = y['dataset']['dataset curation']['sequence edits']
    
    assert isinstance(aln_file, str) and len(aln_file.split()) == 1,"Alignment file must be a file name."
    assert isinstance(par_file, str) and len(par_file.split()) == 1,"Partition information must be a file name."
    assert isinstance(justification, str),"Justification must be a string."
    assert isinstance(edits, str),"Sequence edits must be a string."
    print('\tdataset curation imformation correct')
        
    
def test_tree():
    y = yaml.load(open(yaml_file, 'r'),Loader=yaml.FullLoader)
    text = y['dataset']['used for tree inference']
        
    assert text['concatenated'] in [True, False], "The 'used for tree inference' section must be 'yes' or 'no'"
    assert text['locus trees'] in [True, False], "The 'used for tree inference' section must be 'yes' or 'no'"
    print('\twhether used for tree inference correct')
    

def test_timetree():
    y = yaml.load(open(yaml_file, 'r'),Loader=yaml.FullLoader)
    timetree = y['dataset']['timetree']
    date = y['dataset']['timetree']['date accessed'].split('/')
    
    assert isinstance(timetree['timetree species 1'], str) and len(timetree['timetree species 1'].split()) == 1,"Timetree species name should be one word."
    assert isinstance(timetree['timetree species 2'], str) and len(timetree['timetree species 2'].split()) == 1,"Timetree species name should be one word."
    dd = int(date[0])
    assert isinstance(dd,int) and dd > 0 and dd < 32,"The timetree date is incorrect."
    mm = int(date[1])
    assert isinstance(mm,int) and mm > 0 and mm < 13,"The timetree month is incorrect."
    yy = int(date[2])
    assert isinstance(yy,int) and yy > 2022,"The timetree year is incorrect."
    print('\ttime tree correct')


def test_timetree_age():
    y = yaml.load(open(yaml_file, 'r'),Loader=yaml.FullLoader)
    age = y['dataset']['timetree']['timetree root age']
    lower = y['dataset']['timetree']['timetree lower CI']
    upper = y['dataset']['timetree']['timetree upper CI']
    tree_n = y['dataset']['timetree']['timetree N']
    
    if age == "NA":
        print('\ttimetree root age correct')
        pytest.skip()
        
    
    assert len(age.split()) <= 2, "There's a problem with this age: {}. It should be 'x mya', where x is a number".format(age)    
    try:
        t = float(age.split()[0])
    except:
        raise AssertionError("Check the timetree root age (%s). It looks like it's not a number" % age.split()[0])
    assert t < 3000 and t > 0, "Check the timetree root age. It's too big or too small"
    assert age.split()[1] == 'mya', "The number in the root age should be followed by 'mya' as units."
    
    assert len(lower.split()) <= 2, "There's a problem with this age: {}. It should be 'x mya', where x is a number".format(lower)
    try:
        l = float(lower.split()[0])
    except:
        raise AssertionError("Check the timetree lower CI (%s). It looks like it's not a number" % lower.split()[0])
    assert l < t and l > 0, "Check the timetree lower CI. It's too big or too small"
    assert lower.split()[1] == 'mya', "The number in the timetree lower CI should be followed by 'mya' as units."
    
    assert len(upper.split()) <= 2, "There's a problem with this age: {}. It should be 'x mya', where x is a number".format(upper)
    try:
        u = float(upper.split()[0])
    except:
        raise AssertionError("Check the timetree upper CI (%s). It looks like it's not a number" % upper.split()[0])
    assert u < 3000 and u > l, "Check the timetree upper CI. It's too big or too small"
    assert upper.split()[1] == 'mya', "The number in the timetree upper CI should be followed by 'mya' as units."
    
    try:
        int(tree_n)
    except:
        raise AssertionError("Check the timetree N. It looks like it's not an integer" % upper.split()[0])
    print('\ttimetree root age correct')
    
    
def test_study_age():
    y = yaml.load(open(yaml_file, 'r'),Loader=yaml.FullLoader)
    age = y['dataset']['study root age']
    
    if age == "NA":
        print('\tstudy root age correct')
        pytest.skip()
    
    assert len(age.split()) <= 2, "There's a problem with this age: {}. It should be 'x mya', where x is a number".format(age)
    
    try:
        t= float(age.split()[0])
    except:
        raise AssertionError("Check the study root age (%s). It looks like it's not a number" % age.split()[0])
    assert t < 3000 and t > 0, "Check the study root age. It's too big or too small"
    assert age.split()[1] == 'mya', "The number in the study root age should be followed by 'mya' as units."
    print('\tstudy root age correct')
    
    
def test_genbank_taxanomy():
    y = yaml.load(open(yaml_file, 'r'),Loader=yaml.FullLoader)
    clade = y['dataset']['study clade']

    assert isinstance(clade['latin'], str), "The latin clade must be a string"
    assert isinstance(clade['english'], str), "The latin clade must be a string"
    assert isinstance(clade['taxon ID'], int), "The taxon ID must be a number"

    response = requests.get("".join(['http://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=', str(clade['taxon ID'])]))
    assert response.status_code == 403 or response.status_code == 200,  "this taxon ID didn't work"
    print('\ttaxon ID correct')
    
    
def test_outgroups():
    y = yaml.load(open(yaml_file, 'r'),Loader=yaml.FullLoader)
    outgroups = y['dataset']['outgroups']
    
    assert len(outgroups.split()) == len(outgroups.split(',')), "Outgroups shoulb be seperated by comma"
    assert len(outgroups.split(' ')) > 0, "There should be at list one outgroup taxon"
    print('\toutgroups correct')


