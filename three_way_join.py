#! /usr/bin/env python3


# Write your code here.  Print your output to standard out.

import sys
knownGene = str(sys.argv[1])
kgXref = str(sys.argv[2])
genesets = str(sys.argv[3])

# get information for kgXref.txt and remove duplicate 
with open(kgXref,'r') as inputfile:
    kgXref = {}
    for line in inputfile:
        line = line.strip().split("\t")
        kgXref[line[0]] = line[4]
gene_name = []
gene_id = []
kgxref_modified = {}
for i in kgXref:
    if kgXref[i] not in gene_name:
        gene_name.append(kgXref[i])
        gene_id.append(i)
        kgxref_modified[i] = kgXref[i]
    else:
        continue

# get information for knownGene.txt
with open(knownGene,'r') as inputfile:
    join_dict = {}
    for line in inputfile:
        knownGene_list = []
        try:
            line = line.split("\t")
            knownGene_list.append(line[1]) # chromosome = line[1]
            knownGene_list.append(line[3]) # position_start = line[4]
            knownGene_list.append(line[4]) # position_end = line[5]
            join_dict[line[0]] = knownGene_list
        except:
            continue
        
# change gene id to gene name
join_modified = {}
for i in gene_id:
    try:
        join_modified[kgxref_modified[i]] = join_dict[i]
    except:
        continue
# print(join_modified)

# load Geneset
geneset_list = []
with open(genesets,'r') as inputfile:
    for line in inputfile:
        line = line.strip()
        geneset_list.append(line)
sys.stdout.write("Gene\tChr\tStart\tStop")
sys.stdout.write('\n')
for i in geneset_list:
    if i in join_modified.keys():
        sys.stdout.write("{}\t{}\t{}\t{}".format(i,join_modified[i][0],join_modified[i][1],join_modified[i][2]))
        sys.stdout.write('\n')
    else:
        continue
