#!python3.5
import os
import yaml
import pandas as pd

# generate a csv from the YAML files
all_files = glob.glob(os.path.abspath(os.path.join(os.getcwd(),'../datasets/**/*.yaml')), recursive=True)
df_from_each_file = (pd.io.json.json_normalize(yaml.load(open(f))) for f in all_files)
concatenated_df   = pd.concat(df_from_each_file, ignore_index=True)
