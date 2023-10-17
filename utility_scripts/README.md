How to add a dataset
====================

Preparation
-------------

1. Download AMAS.py from: https://github.com/marekborowiec/AMAS. Then, put it in your working folder.

2. A partitioned or unpartitioned original alignment downloaded from published paper.

3. Python 3. (@HuaiyanRen in using Python 3.9.13 on his laptop)


Basic workflow of adding a dataset
-------------

#1. Convert file(s) of alignment to nexus format.

```
python convert_to_nexus.py -i path -o folder -r rootpath
```
`-i`: the path of file(s) of alignment.
`-o`: the name of a created folder that including the nexus files. Default: `nex`.

#2. Concatenate nexus files into `dataset\alignment.nex`

```
python concatenate_loci.py -i path
```
`-i`: the path of nexus file(s).

#3. Generate a csv file to record partition, locus and genome information and remove [charset] information in `alignment.nex`.

##3.1 If the `alignment.nex` is created by lots of partitioned nexus file:
```
python generate_charset_csv.py -i path -st seq_type
```
`-i`: the path of `alignment.nex`.
`-st`: 'DNA' or 'AA'.
The [charset] information in `alignment.nex` will be automatically removed.
  
##3.2 If the downloaded dataset has already had a RAxML style partition file:
```
python raxml_to_charcsv.py -i path -st seq_type
```
`-i`: the path of `alignment.nex`.
`-st`: 'DNA' or 'AA'.
Then, manually remove [charset] information in `alignment.nex`.
  
Once 3.1 or 3.2 has done, manually add genome information into `charset.csv`. The names of genome should in the list: `['bacterial', 'chloroplast', 'dsDNA', 'dsRNA', 'mitochondrial', 'nuclear', 'ssDNA', 'ssRNA']`.

#4. Fill the yaml file.

  This should be done manually. There is a `README.txt` file in `new_dataset_files` folder guides how to do it.
  
#5. Generate AMAS summaries for the alignment.

```
python generate_summaries.py -i path -c core
```
`-i`: the path of `alignment.nex`.
`-c`: the number of CPU cores to use.

#6. Test all required files are existing and containing correct information by `pytest`.

```
python -m pytest -s > ..path\pytest_log.txt
```
`>`: the path of `alignment.nex`. The `pytest_log.txt` should be put here, without any failure in it.

#7. Add the dataset information to `summary.csv`.

```
python add_on_csv.py -i aln_path -o csv_path -n dataset_name
```
`-i`: the path of `alignment.nex`.
`-o`: the path of `summary.csv`.
`-n`: name of the dataset, which should be `family name of first the author` + `_` + `year of publish`.

#8. Rename and compress the `dataset` file, and upload to FigShare.


Other useful python scripts.
-------------








