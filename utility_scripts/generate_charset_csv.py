import os
import pandas as pd
import argparse

def charset_csv(inpath,seq_type):
    
    partitions_content = [['partitions', 'par_start', 'par_end']]
    loci_content = [['loci', 'loci_start', 'loci_end']]
    
    file = os.path.join(inpath, 'alignment.nex')
    with open(file, 'r') as file_open:
        lines = file_open.readlines()
    
    if seq_type == 'DNA':
        gene_dict = {}
        for line in lines:
            if 'charset ' in line or 'CHARSET ' in line:
                partitions_content.append([line.split()[1], float(line.split()[-1].split(';')[0].split('-')[0]), float(line.split()[-1].split(';')[0].split('-')[1].split('\\')[0])])
                
                gene_id = '_'.join(line.split()[1].split('_')[:-1])
                if gene_id not in gene_dict:
                    gene_dict[gene_id] = []
                    loci_content.append([gene_id ,float(line.split()[-1].split(';')[0].split('-')[0]), float(line.split()[-1].split(';')[0].split('-')[1].split('\\')[0])])
                    
    elif seq_type == 'AA':
        for line in lines:
            if 'charset ' in line or 'CHARSET ' in line:
                partitions_content.append([line.split()[1], float(line.split()[-1].split(';')[0].split('-')[0]), float(line.split()[-1].split(';')[0].split('-')[1])])
                loci_content.append([line.split()[1], float(line.split()[-1].split(';')[0].split('-')[0]), float(line.split()[-1].split(';')[0].split('-')[1])])
    
    # combine dataframe
    df_partitions = pd.DataFrame(partitions_content)
    df_loci = pd.DataFrame(loci_content)
    df_genomes = pd.DataFrame(pd.DataFrame([['genomes', 'gen_start', 'gen_end']]))
    df = pd.concat([df_partitions, df_loci, df_genomes], axis=1)

    # add to csv
    csv_file = os.path.join(inpath, 'charset.csv')
    df.to_csv(csv_file, mode= 'w', index=False, header=False)
    
    # remove sets information in nex file
    new_lines = []
    for line in lines:
        new_lines.append(line)
        if 'begin sets;' in line or 'begin SETS;' in line:
            new_lines.pop()
            break

    with open(file, 'w') as file_open:
        file_open.writelines(new_lines)

    # running
parser = argparse.ArgumentParser(description='')
parser.add_argument('--inpath', '-i', help='', 
                    default = r"C:\Users\u7151703\Desktop\research\datasets\processing\nex\datasets")
parser.add_argument('--seq_type', '-st', help='', 
                    required= True)
args = parser.parse_args()

if __name__ == '__main__':
    try:
       charset_csv(args.inpath, args.seq_type)
    except Exception as e:
        print(e)