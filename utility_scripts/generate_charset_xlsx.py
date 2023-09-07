import os
import pandas as pd
import argparse

def charset_csv(inpath,seq_type):
    
    partitions_content = [['charset', 'start', 'end']]
    loci_content = [['charset', 'start', 'end']]
    
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
    
    # add partitions sheet
    xlsx_file = os.path.join(inpath, 'charset.xlsx')
    df_partitions = pd.DataFrame(partitions_content)
    df_partitions.to_excel(xlsx_file, sheet_name='partitions', index=False, header=False)
    
    # add loci sheet
    df_loci = pd.DataFrame(loci_content)
    with pd.ExcelWriter(xlsx_file, engine='openpyxl', mode='a') as xf:
        df_loci.to_excel(xf, sheet_name='loci', index=False, header=False)
        
    # add genome sheet
    df = pd.DataFrame(pd.DataFrame([['charset', 'start', 'end']]))
    with pd.ExcelWriter(xlsx_file, engine='openpyxl', mode='a') as xf:
        df.to_excel(xf, sheet_name='genomes', index=False, header=False)
        
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