import os
import pandas as pd
import argparse

def charset_csv(inpath):
    
    csv_content = [['charset', 'start', 'end']]
    
    file = os.path.join(inpath, 'alignment.nex')
    with open(file, 'r') as file_open:
        lines = file_open.readlines()
    
    for line in lines:
        if 'charset ' in line:
            csv_content.append([line.split()[1], float(line.split()[-1].split(';')[0].split('-')[0]), float(line.split()[-1].split(';')[0].split('-')[1])])
    
    # add loci sheet
    df = pd.DataFrame(csv_content)
    csv_file = os.path.join(inpath, 'charset.xlsx')
    df.to_excel(csv_file, sheet_name='loci', index=False, header=False)
    
    # add genome sheet
    df = pd.DataFrame(pd.DataFrame([['charset', 'start', 'end']]))
    with pd.ExcelWriter(csv_file, engine='openpyxl', mode='a') as writer:
        df.to_excel(writer, sheet_name='genome', index=False, header=False)
        
    # remove sets information in nex file
    new_lines = []
    for line in lines:
        new_lines.append(line)
        if 'begin sets;' in line:
            new_lines.pop()
            break

    with open(file, 'w') as file_open:
        file_open.writelines(new_lines)


# running
parser = argparse.ArgumentParser(description='')
parser.add_argument('--inpath', '-i', help='', 
                    default = r"C:\Users\u7151703\Desktop\research\datasets\processing\nex\datasets")
args = parser.parse_args()

if __name__ == '__main__':
    try:
       charset_csv(args.inpath)
    except Exception as e:
        print(e)