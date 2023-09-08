import yaml
import pandas as pd
import csv
from Bio.Nexus import Nexus

# generate a df from the alignment.nex file and charset.xlsx file
alignment_file = r"C:\Users\u7151703\Desktop\research\datasets\processing\nex\datasets\alignment.nex"
aln = Nexus.Nexus(alignment_file)
datatype = aln.datatype
aln_length = aln.nchar
ntaxa = aln.ntax

charset_file = r"C:\Users\u7151703\Desktop\research\datasets\processing\nex\datasets\charset.xlsx"
df_loci = pd.read_excel(charset_file, sheet_name= 'loci' , engine='openpyxl')
partitions = len(df_loci)

df_genomes = pd.read_excel(charset_file, sheet_name= 'genomes' , engine='openpyxl')
if 'bacterial' in list(df_genomes.charset):
    bacterial = 'TRUE'
else:
    bacterial = 'FALSE'
if 'chloroplast' in list(df_genomes.charset):
    chloroplast = 'TRUE'
else:
    chloroplast = 'FALSE'
if 'dsDNA' in list(df_genomes.charset):
    dsDNA = 'TRUE'
else:
    dsDNA = 'FALSE'
if 'dsRNA' in list(df_genomes.charset):
    dsRNA = 'TRUE'
else:
    dsRNA = 'FALSE'
if 'mitochondrial' in list(df_genomes.charset):
    mitochondrial = 'TRUE'
else:
    mitochondrial = 'FALSE'
if 'nuclear' in list(df_genomes.charset):
    nuclear = 'TRUE'
else:
    nuclear = 'FALSE'
if 'ssDNA' in list(df_genomes.charset):
    ssDNA = 'TRUE'
else:
    ssDNA = 'FALSE'
if 'ssRNA' in list(df_genomes.charset):
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
with open(r"C:\Users\u7151703\Desktop\research\datasets\processing\nex\datasets\README.yaml", 'r') as f:
    data = yaml.safe_load(f)
concatenated_yaml   = pd.json_normalize(data)

coly = ['dataset.DOI',
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
datasets ='Sanchez-Baracaldo_2017'
summarydf.insert(0, 'name', datasets)

# write
with open(r"C:\Users\u7151703\Desktop\research\code\BenchmarkAlignments\summary.csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    line_count = sum(1 for row in reader) - 1
summarydf.insert(0, 'index', line_count)    

summarydf.to_csv(r"C:\Users\u7151703\Desktop\research\code\BenchmarkAlignments\summary.csv",  mode='a', header=True, index = False)

