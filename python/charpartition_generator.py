# a little script to generate charpartitions from files of charsets


filename = "/Users/robertlanfear/Desktop/sets.txt"

charsets = open(filename, 'r').readlines()

names = [s.split("=")[0].split("CHARSET")[1].strip() for s in charsets]

parts = []
for i, n in enumerate(names):
    print i, n
    part = ''.join([str(i+1), ":", n, ","])
    parts.append(part)

charpartition = ' '.join(parts)
charpartition = charpartition.rstrip(",")

charpartition = ''.join([charpartition, ";"])

print charpartition
