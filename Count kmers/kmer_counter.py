#! /usr/bin/env python3


# Write your code here.  Print your output to standard out.
# import sys and get kmer and filename
import sys
kmer = int(sys.argv[1])
filename = str(sys.argv[2])
# print(kmer,type(kmer))
# print(filename,type(filename))
# put the sequence in the fasta file into one line string
seq = ''
with open(filename,'r') as inputfile:
    for line in inputfile:
        if line[0] == ">":
            continue
        else:
            seq = seq + line.replace('\n','').strip()
# put all the kmers into kmer_list
kmer_list = []
for i in range(0,len(seq)-kmer+1):
    kmer_list.append(seq[i:i+kmer])
# print(kmer_list)
# create a dict which keys are kmers and values are counts, then sort alphabetically
kmer_dict = {}
for j in kmer_list:
    if j not in kmer_dict.keys():
        kmer_dict[j] = 1
    else:
        kmer_dict[j] += 1
# sort the keys in dict
sorted_keys = []
for k in kmer_dict.keys():
    sorted_keys.append(k)
    sorted_keys.sort()
# output
for items in sorted_keys:
    sys.stdout.write("{}\t{}".format(items,kmer_dict[items]))
    sys.stdout.write('\n')
