

# Basic procedure when adding a dataset

```
# check files (Python 2.7.x)
python check_files.py

# make summaries (Python 3.x)
source activate snakes
python generate_summaries.py

# update csv
python generate_csv.py

# zip up the datasets
source deactivate
python gzip_datasets.py


```