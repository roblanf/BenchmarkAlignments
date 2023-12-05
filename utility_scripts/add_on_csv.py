import os
import yaml
import pandas as pd
import csv
from Bio.Nexus import Nexus
import argparse

def add_on_csv(inpath, outfile, dataset_name):
    # generate a df from the alignment.nex file and charset.xlsx file
    alignment_file = os.path.join(inpath, 'alignment.nex')
    aln = Nexus.Nexus(alignment_file)
    datatype = aln.datatype
    aln_length = aln.nchar
    ntaxa = aln.ntax
    
    charset_file = os.path.join(inpath, 'charset.csv')
    df_char = pd.read_csv(charset_file)
    partitions = len(df_char.partition_name)
    
    if 'bacterial' in list(df_char.genome):
        bacterial = 'TRUE'
    else:
        bacterial = 'FALSE'
    if 'chloroplast' in list(df_char.genome):
        chloroplast = 'TRUE'
    else:
        chloroplast = 'FALSE'
    if 'dsDNA' in list(df_char.genome):
        dsDNA = 'TRUE'
    else:
        dsDNA = 'FALSE'
    if 'dsRNA' in list(df_char.genome):
        dsRNA = 'TRUE'
    else:
        dsRNA = 'FALSE'
    if 'mitochondrial' in list(df_char.genome):
        mitochondrial = 'TRUE'
    else:
        mitochondrial = 'FALSE'
    if 'nuclear' in list(df_char.genome):
        nuclear = 'TRUE'
    else:
        nuclear = 'FALSE'
    if 'ssDNA' in list(df_char.genome):
        ssDNA = 'TRUE'
    else:
        ssDNA = 'FALSE'
    if 'ssRNA' in list(df_char.genome):
        ssRNA = 'TRUE'
    else:
        ssRNA = 'FALSE'
        
    concatenated_aln = pd.DataFrame({
        'datatype': [datatype],
        'aln_length': [aln_length],
        'ntaxa': [ntaxa],
        'partitions': [partitions],
        'bacterial': [bacterial],
        'chloroplast': [chloroplast],
        'dsDNA': [dsDNA],
        'dsRNA': [dsRNA],
        'mitochondrial': [mitochondrial],
        'nuclear': [nuclear],
        'ssDNA': [ssDNA],
        'ssRNA': [ssRNA],    
    })
    
    # generate a df from the YAML file
    yaml_file = os.path.join(inpath, 'README.yaml')
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)
    concatenated_yaml   = pd.json_normalize(data)
    
    coly = ['dataset.DOI',
            'dataset.license',
            'dataset.notes',
            'dataset.study clade.english',
            'dataset.study clade.latin',
            'dataset.study clade.taxon ID',
            'dataset.study root age',
            'dataset.timetree.timetree root age',
            'dataset.used for tree inference.concatenated',
            'study.DOI',
            'study.reference',
            'study.year']
    concatenated_yaml = concatenated_yaml[coly]
    
    # get summaries as df
    smy_file = os.path.join(inpath, 'alignment.nex-summary.txt')
    concatenated_smy = pd.read_table(smy_file , sep='\t')
    
    if datatype == 'nucleotide':
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
    elif datatype == 'protein':
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
    
    # merge
    summarydf = concatenated_smy.join(concatenated_aln).join(concatenated_yaml)
    summarydf.insert(0, 'name', dataset_name)
    
    # write
    with open(outfile, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        line_count = sum(1 for row in reader) - 1
    summarydf.insert(0, 'index', line_count)    
    
    summarydf.to_csv(outfile,  mode='a', header=False, index = False)



# running
parser = argparse.ArgumentParser(description='')
parser.add_argument('--inpath', '-i', help='', 
                    required= True)
parser.add_argument('--outfile', '-o', help='', 
                    required= True)
parser.add_argument('--dataset_name', '-n', help='', 
                    required= True)
args = parser.parse_args()

if __name__ == '__main__':
    try:
       add_on_csv(args.inpath, args.outfile, args.dataset_name)
    except Exception as e:
        print(e)  

