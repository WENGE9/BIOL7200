#!/usr/bin/env python3

# Write your code here
import sys
file_one = sys.argv[1]
file_two = sys.argv[2]

# read seq1 and seq2
with open(file_one,"r") as inputfile:
    for line in inputfile:
        seq1 = ''
        line = line.strip()
        if line[0] == ">":
            continue
        else:
            seq1 = seq1 + line.strip()


with open(file_two,"r") as inputfile:
    for line in inputfile:
        seq2 = ''
        line = line.strip()
        if line[0] == ">":
            continue
        else:
            seq2 = seq2 + line.strip()

#print(seq1)
#print(seq2)
# initialize the matrix, horizontal is seq2, vertical is seq1, set matrix to 0
mat = []
for i in range(0,len(seq1)+1):
    H = []
    mat.append(H)
    for j in range(0,len(seq2)+1):
        H.append(0)
    
# generate sorce matrix
maximum_mat = 0
for i in range(1,len(seq1)+1): 
    for j in range(1,len(seq2)+1):
        s1 = seq1[i-1]
        s2 = seq2[j-1]
        # match situation
        if s1 == s2:
            D_change = mat[i-1][j-1] + 1
            if D_change < 0:
                D_change = 0
            else:
                D_change = D_change
            H_change = mat[i][j-1] - 1
            if H_change < 0:
                H_change = 0
            else:
                H_change = H_change
            V_change = mat[i-1][j] - 1
            if V_change < 0:
                V_change = 0
            else:
                V_change = V_change
            mat[i][j] = max(D_change,H_change,V_change)
        # mismatch situation
        elif s1 != s2:
            D_change = mat[i-1][j-1] - 1
            if D_change < 0:
                D_change = 0
            else:
                D_change = D_change
            H_change = mat[i][j-1] - 1
            if H_change < 0:
                H_change = 0
            else:
                H_change = H_change
            V_change = mat[i-1][j] - 1
            if V_change < 0:
                V_change = 0
            else:
                V_change = V_change
            mat[i][j] = max(D_change,H_change,V_change)
        if mat[i][j] > maximum_mat:
            maximum_mat = mat[i][j]
            maximum_i = i
            maximum_j = j
        else:
            continue
#for i in mat:print(i)
#print(maximum_mat,maximum_i,maximum_j)
#===================================================================
# trace back start from maximum_mat
# use 3 string to store alignment results
str1 = ""
str2 = ""
str3 = ""

i0 = maximum_i
j0 = maximum_j

while mat[i0][j0] != 0:
    if seq1[i0-1] == seq2[j0-1]:
        arrow = "D"
        str1 = str1 + seq1[i0-1]
        str2 = str2 + "|"
        str3 = str3 + seq2[j0-1]
        # flag = "match"
    elif seq1[i0-1] != seq2[j0-1]:
        # flag = "mismatch"
        if mat[i0-1][j0-1] >= mat[i0-1][j0] and mat[i0-1][j0-1] >= mat[i0][j0-1]:
            arrow = "D"
            str1 = str1 + seq1[i0-1]
            str2 = str2 + "*"
            str3 = str3 + seq2[j0-1]
        elif mat[i0-1][j0] > mat[i0-1][j0-1] and mat[i0-1][j0] >= mat[i0][j0-1]:
            arrow = "V"
            str1 = str1 + seq1[i0-1]
            str2 = str2 + " "
            str3 = str3 + "_"
        elif mat[i0][j0-1] > mat[i0-1][j0-1] and mat[i0][j0-1] > mat[i0-1][j]:
            arrow = "H"
            str1 = str1 + "_"
            str2 = str2 + " "
            str3 = str3 + seq2[j0-1]
    # print(flag)
    # print(mat[i-1][j-1],"(D)",mat[i-1][j],"V",mat[i][j-1],"H")
    # print(arrow)
    if arrow == "D":
        i0 = i0-1
        j0 = j0-1
    if arrow == "V":
        i0 = i0-1
        j0 = j0
    if arrow == "H":
        i0 = i0
        j0 = j0-1
str1 = str1[::-1] 
str2 = str2[::-1]
str3 = str3[::-1]
score = str2.count("|") - str2.count(" ") - str2.count("*")
sys.stdout.write(str1+'\n')
sys.stdout.write(str2+'\n')
sys.stdout.write(str3+'\n')
sys.stdout.write("Alignment socre: "+str(score)+'\n')








