import os
import pandas as pd
import argparse

def charset_csv(inpath, name, seq_type):
    
    partitions_content = [['alignment_name','partition_name', 'partition_start', 'partition_end', 'partition_skip', 'locus_name', 'codon_position', 'genome', 'data_type']]
    
    file = os.path.join(inpath, 'alignment.nex')
    with open(file, 'r') as file_open:
        lines = file_open.readlines()
    
    if seq_type == 'DNA':
        for line in lines:
            if 'charset ' in line or 'CHARSET ' in line:
                csv_row = [name, line.split()[1]]
                if '\\' in line:
                    csv_row = csv_row + [float(line.split()[-1].split(';')[0].split('-')[0]), float(line.split()[-1].split(';')[0].split('-')[1].split('\\')[0]), float(line.split()[-1].split(';')[0].split('-')[1].split('\\')[1])]
                    if 'Pos' in line.split()[1]:
                        csv_row = csv_row + [line.split()[1].split('Pos')[0], float(line.split()[1].split('Pos')[1])]
                else:
                    csv_row = csv_row + [float(line.split()[-1].split(';')[0].split('-')[0]), float(line.split()[-1].split(';')[0].split('-')[1]), 1, line.split()[1], 'NA']
                csv_row = csv_row + ['', seq_type]
                partitions_content.append(csv_row)
                                
    elif seq_type == 'AA':
        for line in lines:
            if 'charset ' in line or 'CHARSET ' in line:
                csv_row = [name, line.split()[1]]
                csv_row = csv_row + [float(line.split()[-1].split(';')[0].split('-')[0]), float(line.split()[-1].split(';')[0].split('-')[1]), 1, line.split()[1], 'NA']
                csv_row = csv_row + ['', seq_type]
                partitions_content.append(csv_row)
                
    # add to csv
    df = pd.DataFrame(partitions_content)
    csv_file = os.path.join(inpath, 'charset.csv')
    df.to_csv(csv_file, mode= 'w', index=False, header=False)
    
# running
parser = argparse.ArgumentParser(description='')
parser.add_argument('--inpath', '-i', help='', 
                    required = True)
parser.add_argument('--name', '-n', help='', 
                    required = True)
parser.add_argument('--seq_type', '-st', help='', 
                    required = True)
args = parser.parse_args()

if __name__ == '__main__':
    try:
       charset_csv(args.inpath, args.name, args.seq_type)
    except Exception as e:
        print(e)