# python -m pytest, test cmd
# python -m pytest -x, stop after one failure
# python -m pytest -s, see print messages
# python -m pytest > ..path\pytest_log.txt, record the output. Mine: C:\Users\u7151703\Desktop\research\datasets\processing\nex\datasets\pytest_log.txt
import os
import yaml
import pytest
import requests
 

folder = r"C:\Users\u7151703\Desktop\research\datasets\processing\nex\datasets" # prettier    
yaml_file = os.path.join(folder, "README.yaml")  


def test_yaml_titles():
    y = yaml.load(open(yaml_file, 'r'),Loader=yaml.FullLoader)

    assert set(y.keys()) == set(['study', 'dataset']),"Missing 'study' or 'dataset' section from your yaml file"
    assert set(y["study"].keys()) == set(['DOI', 'reference', 'year']),"The sections of your 'study' section should be 'reference', 'year', and 'DOI'"
    assert set(y["dataset"].keys()) == set(['DOI', 'license', 'figshare', 'dataset curation', 'used for tree inference', 'timetree', 'study root age', 'study clade', 'outgroups', 'notes']),"The sections of your 'dataset' section should be 'DOI', 'license', 'figshare', 'dataset curation', 'used for tree inference', 'timetree', 'study root age', 'study clade', 'outgroups', 'notes'"
    assert set(y["dataset"]["dataset curation"].keys()) == set(['alignment file', 'partition information', 'justification', 'sequence edits']),"The sections of your 'dataset curation' section should be 'alignment file', 'partition information', 'justification', 'sequence edits'"
    assert set(y["dataset"]["used for tree inference"].keys()) == set(['concatenated', 'locus_trees']),"The sections of your 'study clade' section should be 'concatenated', 'locus_trees'"
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
        
    
def test_tree():
    y = yaml.load(open(yaml_file, 'r'),Loader=yaml.FullLoader)
    text = y['dataset']['used for tree inference']
        
    assert text in [True, False], "The 'used for tree inference' section must be 'yes' or 'no'"
    print('\twhether used for tree inference correct')
    

def test_timetree_age():
    y = yaml.load(open(yaml_file, 'r'),Loader=yaml.FullLoader)
    age = y['dataset']['timetree root age']
    
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
    
    assert ',' not in outgroups, "Outgroups shoulb be seperated by blank space"
    assert len(outgroups.split(' ')) > 0, "There should be at list one outgroup taxon"
    print('\toutgroups correct')


