# to split a big file
f="/Users/roblanfear/Documents/github/BenchmarkAlignments/possible_datasets/Wu_2018/alignment.nex"

split -b 50m $f $f'.'

# to join files back into a single alignment
d="/Users/roblanfear/Documents/github/BenchmarkAlignments/possible_datasets/Wu_2018/"
cat $d"alignment.nex."* > $d"alignment.nex"