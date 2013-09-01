import os
import sys
def format(s,locals):
	return s.format(**dict(globals().items()+locals.items()))

def getargs(args=None):
	i=1
	if not isinstance(args,dict):
		args=dict()

	while i<len(sys.argv):
		if len(sys.argv[i])>0:
			if sys.argv[i][0]=='-':
				try:
					float(sys.argv[i])
					args[k].append(sys.argv[i])
					i+=1
				except:
					k=sys.argv[i][1:]
					i+=1
					args[k]=[]
			else:
				args[k].append(sys.argv[i])
				i+=1
		else:
			args[k].append(sys.argv[i])
			i+=1
	return args

def getfilename(f):
	return f.split('/')[-1]

basename=getfilename

def ossystem(s):
	s=s.replace("python ","python2.7 ")
	sys.stdout.flush()
	print s
	sys.stdout.flush()
	return os.system(s)

def readconfig(f,args=None):
	if not isinstance(args,dict):
		args=dict()
	for line in open(f):
		line=line.strip().split('\t')
		if line[0] not in args:
			args[line[0]]=line[1:]
	return args

def argstoargslist(args):
	argslist=[]
	for k,v in args.items():
		argslist.append('-'+k)
		for vv in v:
			argslist.append(vv)
	return argslist

def writeconfig(f,args,mode='w'):
	g=open(f,mode)
	for key in args:
		print>>g,'\t'.join(map(str,[key]+args[key]))
	g.close()

def checkbedformat(f,w=10000,err=dict()):
	beginning=1
	try:
		for i,line in enumerate(open(f)):
			if not line.startswith('chr'):
				if beginning:
					continue
				else:
					raise Exception
			if line.startswith('chr\t'):
				continue
			#line=line.split('\t')
			line=line.split()
			if not 0<=int(line[2])-int(line[1])<=w:
				return 0
			beginning=0
	except: 
		try:
			err['error']=('error at line',i,line)
		except:
			err['error']=('error opening file',)
		return 0
	
	if beginning==0:
		err['error']=('no error',)
		return 1
	else:
		err['error']=('no valid line',)
		return 0

def checkpeakformat(f,err=dict()):
	beginning=1
	try:
		for i,line in enumerate(open(f)):
			if not line.startswith('chr'):
				if beginning:
					continue
				else:
					raise Exception
			if line.startswith('chr\t'):
				continue
			#line=line.split('\t')
			line=line.split()
			if not int(line[1]):
				raise Exception
				return 0
			beginning=0
	except: 
		try:
			err['error']=('error at line',i,line)
		except:
			err['error']=('error opening file',)
		return 0
	if beginning==0:
		err['error']=('no error',)
		return 1
	else:
		err['error']=('no valid line',)
		return 0

def checkformat(f,w=10000,err=dict()):
	format=2
	try:
		if checkbedformat(f,w,err):
			return 2
	except:
		pass
	try:
		if checkpeakformat(f,err):
			return 1
	except:
		pass
	return 0


def readbed1(f):
	format=checkformat(f)
	#tolerant against invalid lines at the beginning
	if format==2:
		for i,line in enumerate(open(f)):
			if not line.startswith('chr'):
				continue
			if line.startswith('chr\t'):
				continue
			#comps=line.split('\t')
			comps=line.split()
			comps[-1]=comps[-1].strip()
			yield [comps[0],int(comps[1]),int(comps[2])]+map(str,comps[3:])
	elif format==1:
		for i,line in enumerate(open(f)):
			if not line.startswith('chr'):
				continue
			if line.startswith('chr\t'):
				continue
			#comps=line.split('\t')
			comps=line.split()
			comps[-1]=comps[-1].strip()
			yield [comps[0],int(comps[1]),int(comps[1])+1]+map(str,comps[2:])
	else:
		raise Exception('Invalid File Format')


def readpeak1(f):
	format=checkformat(f)
	if format==2:
		for i,line in enumerate(open(f)):
			if not line.startswith('chr'):
				continue
			if line.startswith('chr\t'):
				continue
			#comps=line.split('\t')
			comps=line.split()
			comps[-1]=comps[-1].strip()
			yield [comps[0],(int(comps[1])+int(comps[2]))/2]+map(str,comps[3:])
	elif format==1:
		for line in open(f):
			if not line.startswith('chr'):
				continue
			if line.startswith('chr\t'):
				continue
			#comps=line.split('\t')
			comps=line.split()
			comps[-1]=comps[-1].strip()
			yield [comps[0],int(comps[1])]+map(str,comps[2:])
	else:
		raise Exception('Invalid File Format')


