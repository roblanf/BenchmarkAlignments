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
    
    df = df.dropna(subset=['partitions'])    
    par_list = ['#NEXUS', 'begin sets;','','[partitions]']
    charpar_str = 'charpartition partitions ='
    for i in range(len(df)):
        par_list.append('charset ' + df.partitions[i] + ' = ' + str(df.par_start[i]) + '-' + str(df.par_end[i]) + ';')
        charpar_str = charpar_str + ' ' + model + ': ' + df.partitions[i] + ','
    charpar_str = charpar_str[:-1] + ';'
    par_list = par_list + ['', charpar_str, '', 'end;']
    par_file = os.path.join(inpath,'partitions.nex')
    with open(par_file, 'w') as file_open:
        for line in par_list:
            file_open.write(line +'\n')

    df = df.dropna(subset=['loci']) 
    loci_list = ['#NEXUS', 'begin sets;','','[loci]']
    charpar_str = 'charpartition loci ='
    for i in range(len(df)):
        loci_list.append('charset ' + df.loci[i] + ' = ' + str(df.loci_start[i]) + '-' + str(df.loci_end[i]) + ';')
        charpar_str = charpar_str + ' ' + model + ': ' + df.loci[i] + ','
    charpar_str = charpar_str[:-1] + ';'
    loci_list = loci_list + ['', charpar_str, '', 'end;']
    loci_file = os.path.join(inpath,'loci.nex')
    with open(loci_file, 'w') as file_open:
        for line in loci_list:
            file_open.write(line +'\n')
    
    df = df.dropna(subset=['genomes'])         
    gen_list = ['#NEXUS', 'begin sets;','','[genomes]']
    charpar_str = 'charpartition genomes ='
    for i in range(len(df)):
        gen_list.append('charset ' + df.genomes[i] + ' = ' + str(int(df.gen_start[i])) + '-' + str(int(df.gen_end[i])) + ';')
        charpar_str = charpar_str + ' ' + model + ': ' + df.genomes[i] + ','
    charpar_str = charpar_str[:-1] + ';'
    gen_list = gen_list + ['', charpar_str, '', 'end;']
    gen_file = os.path.join(inpath,'genomes.nex')
    with open(gen_file, 'w') as file_open:
        for line in gen_list:
            file_open.write(line +'\n')        
                
    
    
# running
parser = argparse.ArgumentParser(description='')
parser.add_argument('--inpath', '-i', help='', 
                    default = r"C:\Users\u7151703\Desktop\research\datasets\processing\nex\datasets")
parser.add_argument('--seq_type', '-st', help='', 
                    required= True)
args = parser.parse_args()

if __name__ == '__main__':
    try:
       csv_to_nex(args.inpath, args.seq_type)
    except Exception as e:
        print(e)    