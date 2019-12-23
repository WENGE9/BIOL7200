#!/usr/bin/env python3

'''
Script for finding orthologs using reciprocal BLAST hits.

You may choose to import any of the other allowed modules.

You have to write an argparse for getting command line arguments. The usage for
this script is:
    ./find_orthologs.py -i1 <Input file 1> -i2 <Input file 2> -o <Output file name> –t <Sequence type – n/p>

where "n" specifies a nucleotide sequence and "p" specifies a protein sequence.
'''

import argparse
import os
def main():
    '''
    This is the main function.
    '''
    '''
    Insert argparse code that populates the following variables
     - file_one
     - file_two
     - output_file
     - input_sequence_type
    '''
    # Argparse code
    # blastn -db testSpeciesA.fasta -query testSpeciesB.fasta -out out.txt -outfmt 10
    parser = argparse.ArgumentParser()
    parser.add_argument('-i1', '--file_one', required = True, help='one of the input file')
    parser.add_argument('-i2', '--file_two', required = True, help='the other input file')
    parser.add_argument('-o', '--output_file', required = True,help='the output file name')
    parser.add_argument('-t', '--input_sequence_type', required = True, help='the type of sequence - n/p')
    args = parser.parse_args()
    # print(args.file_one,args.file_two,args.output_file,args.input_sequence_type)
    file_one = args.file_one
    file_two = args.file_two
    output_file = args.output_file
    input_sequence_type = args.input_sequence_type
    # first step: create one reference database and query
    os.system("makeblastdb -in ./input_files/"+file_one+" -dbtype 'nucl' -out file_one.db")
    os.system("blastn -db file_one.db -query ./input_files/%s -max_target_seqs 1 -out out1.txt -outfmt 6" % file_two)
    os.system("makeblastdb -in ./input_files/"+file_two+" -dbtype 'nucl' -out file_two.db")
    os.system("blastn -db file_two.db -query ./input_files/%s -max_target_seqs 1 -out out2.txt -outfmt 6" % file_one)
    # store and depulicate
    with open('out1.txt','r') as inputfile:
        origin_list = []
        result_list = []
        i = 0
        for line in inputfile:
            line = line.strip().split("\t")
            result1 = line[0]+"\t"+line[1]
            origin_list.append(result1)
        print("origin_list :",len(origin_list))
        for i in origin_list:
            if i not in result_list:
                result_list.append(i)
            else:
                continue
    print(len(result_list))
    with open('out2.txt','r') as inputfile:
        origin_list2 = []
        result_list2 = []
        i = 0
        for line in inputfile:
            line = line.strip().split("\t")
            result2 = line[1]+"\t"+line[0]
            origin_list2.append(result2)
        print("origin_list2 :",len(origin_list2))
        for i in origin_list2:
            if i not in result_list2:
                result_list2.append(i)
            else:
                continue
    print(len(result_list2))
    output_list = []
    for i in result_list:
        if i in result_list2:
            output_list.append(i)
        else:
            continue
    os.system("rm out1.txt out2.txt")
    os.system("rm file_*")
    '''
    output_list is a list of reciprocal BLAST hits. Each element is a tab
    separated pair of gene names. Eg:
    ["lcl|AM421808.1_cds_CAM09336.1_10	lcl|AE002098.2_cds_NMB0033_33", "lcl|AM421808.1_cds_CAM09337.1_11
    lcl|AE002098.2_cds_NMB0034_34", "lcl|AM421808.1_cds_CAM09338.1_12	lcl|AE002098.2_cds_NMB0035_35", "lcl|AM421808.1_cds_CAM09339.1_13
    lcl|AE002098.2_cds_NMB0036_36", ...]
    '''

    # output_list = get_reciprocal_hits(file_one, file_two, input_sequence_type)
    with open(output_file, 'w') as output_fh:
        for ortholog_pair in output_list:
            output_fh.write(ortholog_pair + '\n')
     
if __name__ == "__main__":
    main()
