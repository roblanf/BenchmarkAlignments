import os
import pandas as pd
import argparse

def xlsx_to_nex(inpath):
    
    xlsx_file = os.path.join(inpath, 'charset.xlsx')
    
    for set_sheet in ['loci','genomes']:
        df = pd.read_excel(xlsx_file, sheet_name= set_sheet , engine='openpyxl')
        
        
        nex_list = ['#NEXUS', 'begin set;','','['+set_sheet+']']
        charpar_str = 'charpartition ' + set_sheet + ' ='
        for i in range(len(df)):
            nex_list.append('charset ' + df.charset[i] + ' = ' + str(df.start[i]) + '-' + str(df.end[i]) + ';')
            charpar_str = charpar_str + ' ' + df.charset[i] + ': ' + str(df.start[i]) + '-' + str(df.end[i]) + ','
        charpar_str = charpar_str[:-1] + ';'
        nex_list = nex_list + ['', charpar_str, '', 'end;']

        
        nex_file = os.path.join(inpath, set_sheet + '.nex')
        with open(nex_file, 'w') as file_open:
            for line in nex_list:
                file_open.write(line +'\n')
    
    
    
# running
parser = argparse.ArgumentParser(description='')
parser.add_argument('--inpath', '-i', help='', 
                    default = r"C:\Users\u7151703\Desktop\research\datasets\processing\nex\datasets")
args = parser.parse_args()

if __name__ == '__main__':
    try:
       xlsx_to_nex(args.inpath)
    except Exception as e:
        print(e)    