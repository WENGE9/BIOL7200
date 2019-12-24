#!/usr/bin/env python3
import sys
import argparse

# create argparse and help statement
parser = argparse.ArgumentParser()
parser.add_argument('-i1', '--filename1', required = True, help = 'path of inputfile1')
parser.add_argument('-i2', '--filename2', required = True, help = 'path of inputfile2')
parser.add_argument('-m', '--minimaloverlap', required = True, help = 'minimal overlap should be a integer range in 0 - 100')
parser.add_argument('-o', '--outputfile', required = True, help = 'name of outputfile')
parser.add_argument('-j', '--join', help = 'join the two entries', action = 'store_true')
args = parser.parse_args()
file1 = args.filename1
file2 = args.filename2
per = int(args.minimaloverlap)
output = args.outputfile
j = args.join

#store the lines of file1 in list1 and chromosome name in chr_name
chr_name = []
TE_dict = {}
with open(file1,'r') as inputfile1:
    for line1 in inputfile1:
        line1 = line1.strip().split('\t')
        if line1[0] not in chr_name:
            chr_name.append(line1[0])
        if line1[0] not in TE_dict:
            TE_dict[line1[0]] = []
        TE_dict[line1[0]].append(line1)
        
# store the lines of file2 in list2 
Intro_dict = {}
with open(file2,'r') as inputfile2:
    for line2 in inputfile2:
        line2 = line2.strip().split('\t')
        if line2[0] not in Intro_dict:
            Intro_dict[line2[0]] = []
        Intro_dict[line2[0]].append(line2)
        
# iteration for each chromosome
for chr in chr_name:
    next_index = 0
    # iterate corresponding intervals in each chromosome
    for TE in range(len(TE_dict[chr])):
        TE_start = int(TE_dict[chr][TE][1])
        TE_end = int(TE_dict[chr][TE][2])
        TE_length = int(TE_end) - int(TE_start)
        # record the index of first overlap interval for each interval in TE
        # next interval in TE will iterate the interval in Intro begin with next_interval
        index_record = False
        index = next_index
        # make sure iteration operate in the chromosome
        while TE <= len(TE_dict[chr]):
            if index >= len(Intro_dict[chr]):
                break
            intro_start = int(Intro_dict[chr][index][1])
            intro_end = int(Intro_dict[chr][index][2])
            # no overlap situation => next loop
            if intro_end < TE_start:
                index += 1
                continue
            # first overlap situation => sotre index as next_index
            elif intro_end >= TE_start:
                if intro_start < TE_end:
                    if not index_record:
                        next_index = index
                        index_record = True
                    overlap = int(min(intro_end,TE_end)) - int(max(intro_start,TE_start))
                    # able to output:
                    if overlap/TE_length*100 >= per:
                        with open(output,'a+') as out:
                            if j:
                                # join output has duplicate lines
                                out.write(chr+'\t'+str(TE_start)+'\t'+str(TE_end)+'\t'+chr+'\t'+str(intro_start)+'\t'+str(intro_end)+'\n')
                                index += 1
                                continue
                            else:
                                # output without joint has no duplicate lines thus break loop after each output
                                out.write(chr+'\t'+str(TE_start)+'\t'+str(TE_end)+'\n')
                                break
                    else:
                        index += 1
                        continue 
                else:
                    break
            if intro_start > TE_end:
                break
