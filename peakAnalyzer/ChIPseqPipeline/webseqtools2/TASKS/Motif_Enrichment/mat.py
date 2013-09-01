import os
import sys



lines=open(sys.argv[1],'r').readlines()

tfname=""
for i in range(0,len(lines)):
	line=lines[i]
	if "Name" in line:
		i+=1
		tfname=lines[i].strip()
		print "DE\tI_"+tfname+"_bergman04"
		print "PO\tA\tC\tG\tT"
	if "Matrix" in line:
		i+=1
		A=lines[i].strip().split()
		i+=1
                C=lines[i].strip().split()
		i+=1
                G=lines[i].strip().split()
		i+=1
                T=lines[i].strip().split()
		for j in range(1,len(A)):
			print str(j)+"\t"+A[j]+"\t"+C[j]+"\t"+G[j]+"\t"+T[j]+"\tX"
		print "XX"
		
			
		
