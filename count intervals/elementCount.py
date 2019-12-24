#!/usr/bin/env python3
import sys
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--filename', required = True, help='path of inputfile')
args = parser.parse_args()
file_name = args.filename

chr_name = []
position = []
# read file and store chrname and store all the line in the position
with open(file_name,'r') as inputfile:
    for line in inputfile:
        line = line.strip().split('\t')
        position.append(line)
        if line[0] not in chr_name:
            chr_name.append(line[0])
# iterate chr_name and position and store the each site as whether it is header(H) or tail(T) in the list
# eg:10 15
#    12 15
#    13 20
# {chr1:[[10,"H"],[15,"T"],[12,"H"],[13,"H"],[15,"T"],[20,"T"]],chr10:[[],[]]}
# Then sort by the first element in the list
chr_position = {}
for i in chr_name:
    position_info = []
    for j in position:
        head_info = []
        tail_info = []
        if j[0] == i:
            head_info.append(j[1])
            head_info.append("H")
            tail_info.append(j[2])
            tail_info.append("T")
        else:
            continue
        position_info.append(head_info)
        position_info.append(tail_info)
    position_info.sort(key=lambda x:int(x[0]))
    chr_position[i] = position_info              
# count the frequence of each site.
# origin count = 0
# if site is H, count += 1
# if site is T, count -= 1
#     count
#   10  1
#   12  2
#   13  3
#   15  2
#   15  1
#   20  0
for i in chr_position:
    count = 0
    count_dict = {}
    for j in chr_position[i]:
        if j[1] == "H":
            count += 1
            count_dict[j[0]] = count
        else:
            count -= 1
            count_dict[j[0]] = count
    count_list = []
    for o in count_dict:
        tmp_list = []
        tmp_list.append(o)
        tmp_list.append(count_dict[o])
        count_list.append(tmp_list)
    '''for k in range(len(count_list)-2,-1,-1):
        if count_list[k][1] == count_list[k+1][1]:
            count_list.remove(count_list[k+1])'''   
    # for each element in the count_dict, if value != 0, output this key and continuously key and according value of key.
    # if value = 0, do next loop
    for k in range(0,len(count_list)-1):
        if count_list[k][1] != 0:
            sys.stdout.write(i+'\t'+str(count_list[k][0])+'\t'+str(count_list[k+1][0])+'\t'+str(count_list[k][1])+'\n')
        else:
            continue
