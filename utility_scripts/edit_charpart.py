import os
import argparse


def edit_text(inpath):
    
    file = os.path.join(inpath, 'alignment.nex')
    with open(file, 'r') as file_open:
        lines = file_open.readlines()
    
    for l in range(len(lines)):
        if 'begin data' in lines[l]:
            lines[l] = lines[l].replace('data','DATA')
        elif 'begin sets' in lines[l]:
            line = lines[l].replace('sets','SETS')
            lines[l] = line + '\n\t[loci]\n'
        elif 'dimensions ' in lines[l] or 'format ' in lines[l] or 'matrix' in lines[l]:
            lines[l] = '\t' + lines[l]
        elif 'charset ' in lines[l]:
            lines[l] = lines[l].replace('charset','\tCHARSET')
        elif 'charpartition combined' in lines[l]:
            lines[l] = lines[l].replace('charpartition combined','\n\tCHARPARTITION loci')
            lines[l] = lines[l] +'\n\n\t[genomes]\n\n\tCHARPARTITION genomes =\n\n\t[outgroups]\n\tTAXSET outgroups =\n\n'
        elif '#NEXUS' in lines[l] or ';' in lines[l]:
            continue
        else:
            lines[l] = '\t' + lines[l]
    
    with open(file, 'w') as file_open:
        for line in lines:
            file_open.write(line)

# running
parser = argparse.ArgumentParser(description='')
parser.add_argument('--inpath', '-i', help='', 
                    default = r"C:\Users\u7151703\Desktop\research\datasets\processing\nex\datasets")
args = parser.parse_args()

if __name__ == '__main__':
    try:
       edit_text(args.inpath)
    except Exception as e:
        print(e)