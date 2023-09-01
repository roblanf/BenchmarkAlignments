#!python3.5
#import os
import yaml
import pandas as pd
import csv
#import glob
#import AMAS

# generate a df from the YAML file
with open(r"C:\Users\u7151703\Desktop\research\datasets\processing\nex\datasets\README.yaml", 'r') as f:
    data = yaml.safe_load(f)
concatenated_yaml   = pd.json_normalize(data)

coly = ['dataset.DOI',
        'dataset.alignment.datatype',
        'dataset.alignment.nchar',
        'dataset.alignment.ntax',
        'dataset.alignment.partitions',
        'dataset.genomes.bacterial',
        'dataset.genomes.chloroplast',
        'dataset.genomes.dsDNA',
        'dataset.genomes.dsRNA',
        'dataset.genomes.mitochondrial',
        'dataset.genomes.nuclear',
        'dataset.genomes.ssDNA',
        'dataset.genomes.ssRNA',
        'dataset.license',
        'dataset.notes',
        'dataset.study clade.english',
        'dataset.study clade.latin',
        'dataset.study clade.taxon ID',
        'dataset.study root age',
        'dataset.timetree root age',
        'dataset.used for tree inference',
        'study.DOI',
        'study.reference',
        'study.year']
concatenated_yaml = concatenated_yaml[coly]

# get summaries as df
concatenated_smy = pd.read_table(r"C:\Users\u7151703\Desktop\research\datasets\processing\nex\datasets\alignment.nex-summary.txt",sep='\t')

if concatenated_yaml['dataset.alignment.datatype'][0] == 'nucleotide':
    cols = ['Total_matrix_cells',
    		'Undetermined_characters',
    		'Missing_percent',
           	'No_variable_sites',
    		'Proportion_variable_sites',		
    		'Parsimony_informative_sites',		
    		'Proportion_parsimony_informative',
    		'AT_content', 
           	'GC_content']
    concatenated_smy = concatenated_smy[cols]
elif concatenated_yaml['dataset.alignment.datatype'][0] == 'protein':
    cols = ['Total_matrix_cells',
    		'Undetermined_characters',
    		'Missing_percent',
           	'No_variable_sites',
    		'Proportion_variable_sites',		
    		'Parsimony_informative_sites',		
    		'Proportion_parsimony_informative']
    concatenated_smy = concatenated_smy[cols]
    concatenated_smy['AT_content'] = ''
    concatenated_smy['GC_content'] = ''


# dataset names
datasets ='Sanchez-Baracaldo_2017'
concatenated_smy.insert(0, 'name', datasets)
concatenated_yaml.insert(0, 'name', datasets)

# merge
summarydf = pd.merge(concatenated_smy, concatenated_yaml,  how='left', left_on=['name'], right_on = ['name'])

# write
with open(r"C:\Users\u7151703\Desktop\research\code\BenchmarkAlignments\summary.csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    line_count = sum(1 for row in reader) - 1
summarydf.insert(0, '', line_count)    

summarydf.to_csv(r"C:\Users\u7151703\Desktop\research\code\BenchmarkAlignments\summary.csv",  mode='a', header=False, index = False)


