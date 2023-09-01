import os
import argparse


def remove_taxon(inpath, taxa_list):
    
    file_list = [x for x in os.walk(inpath)][0][2]
    
    for f in file_list:
        # read the file lines
        file = os.path.join(inpath, f)
        with open(file, 'r') as file_open:
            lines = file_open.readlines()

        # count how many lines are removed        
        moves = 0
        for line in lines:
            if check_taxa(line, taxa_list):
                moves += 1

        # edit first line in phylip file
        first_line_list = lines[0].split()
        first_line_list_change = str(int(first_line_list[0])-moves)
        lines[0] = first_line_list_change + ' ' + first_line_list[1] + '\n'

        # rewrite lines that don't contain any suspicious taxa
        with open(file, 'w') as file_open:
            for line in lines:
                if not check_taxa(line, taxa_list):
                    file_open.write(line)

def check_taxa(line, taxa_list):
    for taxon in taxa_list:
        if taxon in line:
            return True
    return False

# running
parser = argparse.ArgumentParser(description='')
parser.add_argument('--inpath', '-i', help='', 
                    default = r"C:\Users\u7151703\Desktop\research\datasets\processing")
parser.add_argument('--taxa_list', '-t', help='', nargs='+',
                    required=True)
args = parser.parse_args()

if __name__ == '__main__':
    try:
       remove_taxon(args.inpath, args.taxa_list)
    except Exception as e:
        print(e)