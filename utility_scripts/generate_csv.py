#!python3.5
import os
import yaml
import pandas as pd
import glob
import AMAS

# generate a csv from the YAML files
all_files = glob.glob(os.path.abspath(os.path.join(os.getcwd(),'../datasets/**/*.yaml')), recursive=True)
df_from_each_yaml = (pd.io.json.json_normalize(yaml.load(open(f))) for f in all_files)
concatenated_yaml   = pd.concat(df_from_each_yaml, ignore_index=True)

# get summaries as df
all_smys_f = glob.glob(os.path.abspath(os.path.join(os.getcwd(),'../datasets/**/alignment.nex-summary.txt')), recursive=True)
all_smys = (pd.read_table(open(f)) for f in all_smys_f)
concatenated_smy = pd.concat(all_smys, ignore_index=True, axis=0)

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

# get data types



# dataset names
datasets = glob.glob(os.path.abspath(os.path.join(os.getcwd(),'../datasets/*')))
datasets = [os.path.basename(f) for f in datasets]
concatenated_smy.insert(0, 'name', datasets)
concatenated_yaml.insert(0, 'name', datasets)

# merge
summarydf = pd.merge(concatenated_smy, concatenated_yaml,  how='left', left_on=['name'], right_on = ['name'])

# write
summarydf.to_csv(os.path.abspath(os.path.join(os.getcwd(),'../summary.csv')))

