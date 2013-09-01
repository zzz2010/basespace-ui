import sys,os

if len(sys.argv)<2:
    print 'Usage: python genTssJSON.py inData'
    exit(1)

def filter(data,n):
    td=data[:]
    for i in range(0,len(data)):
    	a=i-n/2
    	b=i+n/2+1
	if n%2==0:
	    a+=1
	a=max(a,0)
	b=min(b,len(data)-1)
	data[i]=sum(td[a:b])/(b-a+1)
    return data

def getStr(x, data):
    ret='['
    for i in range(0,len(x)):
	if i>0:
	    ret+=','
    	ret+='['+str(x[i])+','+str(data[i])+']'
    ret+=']'
    return ret

fi=open(sys.argv[1],'r')
fo=open(sys.argv[1]+'_1.json','w')
fo.write('{\n\"chart\":{\"renderTo\":\"container'+str(1)+'\",\"type\":\"spline\"},\n\"title\":{\"text\":\"Peak Distribution Around TSS (transcript direction)\"},\n\"xAxis\":{\"title\":{\"text\":\"Position\"}},\n\"yAxis\":{\"title\":{\"text\":\"Density\"}},\n\"series\":[')
i=0
for line in fi:
    line=line.strip()
    if len(line)<1:
    	continue
    temp=line.split('\t')
    if i==0:
    	x=map(int,temp)
    else:
	data=map(float,temp[1:len(temp)])
#	print [i/sum(data) for i in data]
	data=filter([i/sum(data) for i in data],5)
#	print data
	if i>1:
	    fo.write(',\n')
	fo.write('{\"name\":\"'+temp[0]+'\",\"data\":'+getStr(x,data)+'}')
    i+=1
fo.write(']\n}')
fo.close()

