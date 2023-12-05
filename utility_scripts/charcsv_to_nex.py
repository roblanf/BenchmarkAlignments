import os
import pandas as pd
import argparse

def csv_to_nex(inpath,seq_type):
    if seq_type == 'DNA':
        model = 'GTR+I+G'
    elif seq_type == 'AA':
        model = 'LG+I+G'
           
    csv_file = os.path.join(inpath, 'charset.csv')
    df = pd.read_csv(csv_file)
       
    par_list = ['#NEXUS', 'begin sets;','','[partitions]']
    charpar_str = 'charpartition partitions ='
    for i in range(len(df)):
        par_list.append('charset ' + df.partition_name[i] + ' = ' + str(int(df.partition_start[i])) + '-' + str(int(df.partition_end[i])) + '\\' + str(int(df.partition_skip[i])) + ';')
        charpar_str = charpar_str + ' ' + model + ': ' + df.partition_name[i] + ','
    charpar_str = charpar_str[:-1] + ';'
    par_list = par_list + ['', charpar_str, '', 'end;']
    par_file = os.path.join(inpath,'partitions.nex')
    with open(par_file, 'w') as file_open:
        for line in par_list:
            file_open.write(line +'\n')

    loci_list = ['#NEXUS', 'begin sets;','','[loci]']
    charpar_str = 'charpartition loci ='
    loci_name = []
    start_dict = {}
    end_dict = {}
    for i in range(len(df)):
        if df.locus_name[i] not in loci_name:
            loci_name.append(df.locus_name[i])
            start_dict[df.locus_name[i]] = df.partition_start[i]
            end_dict[df.locus_name[i]] = df.partition_end[i]
        else:
            if df.partition_start[i] < start_dict[df.locus_name[i]]:
                start_dict[df.locus_name[i]] = df.partition_start[i]
            if df.partition_end[i] > end_dict[df.locus_name[i]]:
                end_dict[df.locus_name[i]] = df.partition_end[i]
    for i in range(len(loci_name)):
        loci_list.append('charset ' + loci_name[i] + ' = ' + str(int(start_dict[loci_name[i]])) + '-' + str(int(end_dict[loci_name[i]])) + ';')
        charpar_str = charpar_str + ' ' + model + ': ' + loci_name[i] + ','
    charpar_str = charpar_str[:-1] + ';'
    loci_list = loci_list + ['', charpar_str, '', 'end;']
    loci_file = os.path.join(inpath,'loci.nex')
    with open(loci_file, 'w') as file_open:
        for line in loci_list:
            file_open.write(line +'\n')
    
     
    
# running
parser = argparse.ArgumentParser(description='')
parser.add_argument('--inpath', '-i', help='', 
                    required= True)
parser.add_argument('--seq_type', '-st', help='', 
                    required= True)
args = parser.parse_args()

if __name__ == '__main__':
    try:
       csv_to_nex(args.inpath, args.seq_type)
    except Exception as e:
        print(e)    