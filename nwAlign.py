#!/usr/bin/env python3

# Write your code here

import sys
file_one = sys.argv[1]
file_two = sys.argv[2]
#print(file_one)
#print(file_two)

# read seq1 and seq2
with open(file_one,"r") as inputfile:
    for line in inputfile:
        seq1 = ''
        line = line.strip()
        if line[0] == ">":
            continue
        else:
            seq1 = seq1 + line.strip()
#print(seq1)

with open(file_two,"r") as inputfile:
    for line in inputfile:
        seq2 = ''
        line = line.strip()
        if line[0] == ">":
            continue
        else:
            seq2 = seq2 + line.strip()
#print(seq2)
# initialize the matrix, horizontal is seq2, vertical is seq1, set matrix to 0
mat = []
for i in range(0,len(seq1)+1):
    H = []
    mat.append(H)
    for j in range(0,len(seq2)+1):
        H.append(0)
for i in range(0,len(seq2)+1):
    mat[0][i] = i*(-1)
for j in range(0,len(seq1)+1):
    mat[j][0] = j*(-1)
#============================================================================
# generate sorce matrix
for i in range(1,len(seq1)+1): 
    for j in range(1,len(seq2)+1):
        s1 = seq1[i-1]
        s2 = seq2[j-1]
        # match situation
        if s1 == s2:
            D_change = mat[i-1][j-1] + 1
            H_change = mat[i][j-1] - 1
            V_change = mat[i-1][j] - 1
            mat[i][j] = max(D_change,H_change,V_change)
        # mismatch situation
        elif s1 != s2:
            D_change = mat[i-1][j-1] - 1
            H_change = mat[i][j-1] - 1
            V_change = mat[i-1][j] - 1
            mat[i][j] = max(D_change,H_change,V_change)
            
#for i in mat:print(i)

#=============================================================================
# trace back
# start from lower left corner
i = len(seq1)
j = len(seq2)
# start from mat[i][j]
# for first mat[i][j], if seq1[i] = seq2[j],
# status = match, arrow = D, trace back to upper left
# list1.append(seq1[i]), list2.append(seq2[j])
# if seq1[j] != seq2[j], status = mismatch, arrow = D/H/V, trace back to max of three ceils.
# for D: list1.append(seq1[i]), list2.append(seq2[j])
# for H: list1.append("_"), list2.append(seq2[j])
# for V: list1.append(seq1[i]), list2.append("_")
str1 = ""
str2 = ""
str3 = ""

while i >= 1 and j >= 1:
    if seq1[i-1] == seq2[j-1]:
        arrow = "D"
        str1 = str1 + seq1[i-1]
        str2 = str2 + "|"
        str3 = str3 + seq2[j-1]
        # flag = "match"
    elif seq1[i-1] != seq2[j-1]:
        # flag = "mismatch"
        if mat[i-1][j-1] >= mat[i-1][j] and mat[i-1][j-1] >= mat[i][j-1]:
            arrow = "D"
            str1 = str1 + seq1[i-1]
            str2 = str2 + "*"
            str3 = str3 + seq2[j-1]
        elif mat[i-1][j] > mat[i-1][j-1] and mat[i-1][j] >= mat[i][j-1]:
            arrow = "V"
            str1 = str1 + seq1[i-1]
            str2 = str2 + " "
            str3 = str3 + "_"
        elif mat[i][j-1] > mat[i-1][j-1] and mat[i][j-1] > mat[i-1][j]:
            arrow = "H"
            str1 = str1 + "_"
            str2 = str2 + " "
            str3 = str3 + seq2[j-1]
    # print(flag)
    # print(mat[i-1][j-1],"(D)",mat[i-1][j],"V",mat[i][j-1],"H")
    # print(arrow)
    if arrow == "D":
        i = i-1
        j = j-1
    if arrow == "V":
        i = i-1
        j = j
    if arrow == "H":
        i = i
        j = j-1
str1 = str1[::-1] 
str2 = str2[::-1]
str3 = str3[::-1]
score = str2.count("|") - str2.count(" ") - str2.count("*")
sys.stdout.write(str1+'\n')
sys.stdout.write(str2+'\n')
sys.stdout.write(str3+'\n')
sys.stdout.write("Alignment socre: "+str(score)+'\n')















