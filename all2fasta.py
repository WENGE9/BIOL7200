#!/usr/bin/env python3

import re
import argparse
aa = 'ARNDCQEGHILKMFPSTWYV'
# Argparse code
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fold', help='line fold', default = 70)
parser.add_argument('-i', '--filename', required = True, help='path of inputfile')
args = parser.parse_args()
file_name = args.filename
fold_num = int(args.fold)
#print('file_name:',file_name,'fold_num:',fold_num)
#========================================================================
def formattype(line):
    # determine whether embl file
    embl = re.match('(ID)',line)
    if embl:
        return "embl"
    # determine whether fastq file
    fastq = re.match('(@)',line)
    if fastq:
        return "fastq"
    # determine whether mega file
    mega = re.match('(#MEGA)',line,re.I)
    if mega:
        return "mega"
    # determine whether gb file
    gb = re.match('(LOCUS)',line)
    if gb:
        return "gb"
# read the first line of each file
inputfile = open(file_name,'r')
firstline = inputfile.readline()
inputfile.close()
#=========================================================
# determine file type and return output file name
def output_type(seq):
    seq_length = len(seq)
    na_seq = re.match('[acgtn]+',seq,re.I)
    if len(na_seq.group()) == len(seq):
        outname = file_name.split('.')
        output = ''
        if len(outname) > 1 and outname[-1] != "fna":
            outname[-1] = "fna"
            output = ".".join(outname)
        if len(outname) == 1:
            outname.append("fna")
            output = ".".join(outname)
    else:
        seq = search_seq
        outname = file_name.split('.')
        output = ''
        if len(outname) > 1 and outname[-1] != "faa":
            outname[-1] = "faa"
            output = ".".join(outname)
        if len(outname) == 1:
            outname.append("faa")
            output = ".".join(outname)
    return output
#========================================================================================            
# write the output file with header and sequence with accordingly file name
def write_output(output,header,seq):
    seq = seq.strip()
    outputfile = open(output,'a')
    outputfile.write(header+'\n')
    if len(seq) % fold_num != 0:
        line_num = len(seq) // fold_num + 1
    else:
        line_num = len(seq) // fold_num
    for i in range(1,line_num+1):
        if i < line_num:
            outputfile.write(seq[fold_num*(i-1):fold_num*i]+'\n')
        else:
            outputfile.write(seq[fold_num*(i-1):]+'\n')
    outputfile.close()
#============================================================================
# operation of gb file
if formattype(firstline) == "gb":
    with open(file_name,'r') as infile:
        gb_list = []
        for line in infile:
            line = line.strip()
            gb_list.append(line)
        header = ''
        seq = ''
        for i in range(0,len(gb_list)):
            locus = re.match('LOCUS\s+(.+?)\s+',gb_list[i])
            if locus:
                header = locus.group(1)
            seq_start = re.match('ORIGIN',gb_list[i])
            seq_list = []
            if seq_start:
                seq_list = gb_list[i+1:-2]
                break
        origin_seq = "".join(seq_list)
        search_seq = re.sub('\d','',origin_seq)
        seq = search_seq.strip().replace(" ","")
        seq = seq.upper()
        write_output(output_type(seq),header,seq)
# determine the file format and do the according operation
if formattype(firstline) == "embl": 
    with open(file_name,'r') as infile:
        embl_list = []
        for line in infile:
            line = line.strip()
            embl_list.append(line)
        header_dict = {}
        seq = ''
        for i in range(0,len(embl_list)):
            search_ID = re.match('ID\s+(.+?);',embl_list[i])
            if search_ID:
                header_dict['ID'] = search_ID.group(1)
            # use re.search to find SV
            search_SV = re.search('SV\s+(.+?);',embl_list[i])
            if search_SV:
                header_dict['SV'] = search_SV.group(1)
            # use re.match to find DE 
            search_DE = re.match('DE\s+(.+)',embl_list[i])
            if search_DE:
                header_dict['DE'] = search_DE.group(1)
            # find "SQ" and append the lines after SQ to new list
            seq_start = re.match('SQ\s+',embl_list[i])
            seq_list = []
            if seq_start:
                seq_list = embl_list[i+1:len(embl_list)-1]
                break
        seq_origin = ''
        for i in seq_list:
            seq_origin += i
        search_seq = re.sub('\d','',seq_origin)
        seq = search_seq.strip().replace(" ","")
        seq = seq.upper()
        header = '>ENA'+'|'+header_dict['ID']+'|'+header_dict['ID']+'.'+header_dict['SV']+' '+header_dict['DE']                 
        write_output(output_type(seq),header,seq)
# operation of mega file
if formattype(firstline) == "mega": 
    with open(file_name,'r') as infile:
        header_dict = {}
        seq = ''
        mega_list = []
        mega_dict = {}
        for line in infile:
            line = line.strip()
            mega_list.append(line)
        mega_list = mega_list[2:]
        for i in range(0,len(mega_list)):
            name = re.match('#((?!MEGA).+)',mega_list[i],re.I)
            if name:
                head = name.group(1)
                mega_dict[head] = ''
                continue
            if mega_list[i] != '':
                mega_dict[head] += mega_list[i]
            else:
                continue
        for j in mega_dict:
            write_output(output_type(mega_dict[head]),">"+j,mega_dict[j])
# operation of fastq file
if formattype(firstline) == "fastq":
    with open(file_name,'r') as infile:
        header_dict = {}
        seq = ''
        fq_list = []
        fq_dict = {}
        for line in infile:
            line = line.strip()
            fq_list.append(line)
        for i in range(0,len(fq_list)):
            if i % 4 == 0:
                fq_dict[fq_list[i][1:]] = fq_list[i+1]
                sample_seq = fq_list[i+1]
                continue
            else:
                continue
        for j in fq_dict:
            write_output(output_type(sample_seq),">"+j,fq_dict[j])

         



