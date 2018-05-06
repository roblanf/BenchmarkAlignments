

# Basic procedure when adding a dataset

```
# check files (Python 2.7.x)
python check_files.py

# make summaries (Python 3.x)
# note that currently, if the alignment gets zipped you'll need to unzip it first before doing this step
source activate snakes
python generate_summaries.py

# update csv
python generate_csv.py
```