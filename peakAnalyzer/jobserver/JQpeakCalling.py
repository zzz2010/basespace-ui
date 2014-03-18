import os
import sys
import glob
import commands

#Usage Line
print "Welcome.\n Usage: python <.cfg> <bowtie2_path> <bowtie2_index> <genome_length_file> <output_dir> [jobOption]\n" 
sys.stdout.flush()    

#parameters for tweak/tune
num_proc=" 16 "

# #these are based on user-input
bowtie2_dir=sys.argv[2]
bowtie2_index_dir=sys.argv[3]
genome_length_path=sys.argv[4]
output_dir=sys.argv[5]+"/"
mapOnly=False
if len(sys.argv)>6 and 'map' in sys.argv[6]:
    mapOnly=True

#tracking vars
isControl=0
targetArray=[]
controlArray=[]
targetfileName_List=list()
targetfileExtension_List=list()
controlfileName_List=list()
controlfileExtension_List=list()
targetMappings_List=list()
controlMappings_List=list()

targetPair=list()
controlPair=list()

#This procedure determines if a "suffix" file is already mapped
#Return 1 for mapping file; 0 for raw read file.
def isMapped(suffix):
    if suffix=='.fa' or suffix=='.fasta' or suffix=='.fq' or suffix=='.fastq' or suffix=='.fastq.gz':
        return 0
    return 1

#This procedure return the type of the file (determine by the extension suffix)
#Input "Filename", Return 
#0 for sam, 1 for bam, 2 for bed, 3 for fa/fasta, 4 for fq/fastq
def FileType(fileName): 
    prefix, suffix = os.path.splitext(fileName)
    #print prefix +"-test1"
    #print suffix +"-test2"
    if suffix=='.sam':
        return 0
    elif suffix=='.bam':
        return 1
    elif suffix=='.bed':
        return 2
    elif suffix=='.fa' or suffix=='.fasta':
        return 3
    elif suffix=='.fq' or suffix=='.fastq':
        return 4

def unzipFile(filename):
    if filename.endswith(".gz"):
        outfile="/tmp/"+os.path.basename(filename).replace(".gz","")
        cmd="gunzip -c "+filename+" > "+outfile
        print cmd
        os.system(cmd)
        return outfile
    else:
        return filename
#This procedure defines which are Target/Control files
#A file is read with each line specifying a Target/Control file
#Delimiter "===" is used to seperate the Target from the Control files
#We assume target files appear BEFORE "==="; otherwise, the specified is a control file.
def setReadFiles():
    try:
        if len(sys.argv) < 2:
            raise Exception('Config file is missing!')
        
        with open(sys.argv[1], "r" ) as configFile:
            #configContents = configFile.readlines().strip();
            global targetArray
            global controlArray
            
            global isControl
            global isPair
            
            global targetPair
            global controlPair
            global targetMappings_List
            global controlMappings_List
            
            global num_proc
            
            for line in configFile:
                line=line.strip()
                #print len(line.split())
                
                if line == '===':
                    isControl=1
                elif line == '': pass 
                else:
                    if len(line.split())==1:
                        if isControl==0:
                            targetArray.append( unzipFile(line) )
                        else:
                            controlArray.append( unzipFile(line) )
                    else:
                        line = line.split()
                        #bowtie2 [options]* -x <bt2-idx> {-1 <m1> -2 <m2> | -U <r>} [-S <sam>]
                        name, ext = os.path.splitext(line[0])
                        if isControl==0:
                            targetPair.append(" "+bowtie2_dir + " -p " +num_proc+ " --very-fast -x " + bowtie2_index_dir + " -1 " + line[0] + " -2 " + line[1] + " -S " + name+".sam >"+output_dir+os.path.basename(line[0])+".maplog.txt")
                            targetArray.append(name+".sam")                            
                        else:
                            controlPair.append(" "+bowtie2_dir + " -p " +num_proc+ " --very-fast -x " + bowtie2_index_dir + " -1 " + line[0] + " -2 " + line[1] + " -S " + name+".sam >"+output_dir+os.path.basename(line[1])+".maplog.txt")
                            controlArray.append(name+".sam")
                        #print " "+bowtie2_dir + " -p 2 -x " + bowtie2_index_dir + " -1 " + line[0] + " -2 " + line[1] + " -S " + name+".sam "
                #print line
            
    except IOError as e:
        print '1.Config file name is problematic.'

#This procedure will map any files found in the config-file and name each output with a suffix .sam to them
def MapFiles():
    global targetfileName_List
    global targetfileExtension_List
    global controlfileName_List
    global controlfileExtension_List
    global targetMappings_List
    global controlMappings_List
    
    global num_proc
    
    for fileName in targetArray:
        targetfileName, targetfileExtension = os.path.splitext(fileName)
        targetfileName_List.append(targetfileName)
        targetfileExtension_List.append(targetfileExtension)
        #print targetfileName_List[0] +  " lala"
        
    for fileName in controlArray:
        controlfileName, controlfileExtension = os.path.splitext(fileName)
        controlfileName_List.append(controlfileName)
        controlfileExtension_List.append(controlfileExtension)
        #print controlfileName_List[0] +  " lala"
        
    cnt=0
    for extension in targetfileExtension_List:        
        if isMapped(extension) == 0:
            #print extension
            cmd=" "+bowtie2_dir + " -p " +num_proc+ " --very-fast -x " + bowtie2_index_dir + " -U " + targetfileName_List[cnt]+extension + " -S " + targetfileName_List[cnt]+".sam 2>"+targetfileName_List[cnt]+".maplog.txt"
            #cmd=batmis_dir+'batman -g '+batmis_index_dir+' -q '+ targetfileName_List[cnt]+extension + ' -o ' + targetfileName_List[cnt]+'.bin ' + ' -n 2 -U;'
            #cmd+=batmis_dir+'batdecode -g '+batmis_index_dir+' -i '+ targetfileName_List[cnt]+'.bin -o ' + targetfileName_List[cnt]+'.sam '
            print 'CMD: '+ cmd 
            print '1.Mapping _target_ sequences...: '+targetfileName_List[cnt]+extension
            os.system(cmd)
            os.system("mv " + targetfileName_List[cnt]+".maplog.txt" + " " + output_dir)
            #cmd = 'rm ' + targetfileName_List[cnt]+'.bin '
            #os.system(cmd)
            print '1.Mapping '+ targetfileName_List[cnt]+' Done.'
            targetMappings_List.append(targetfileName_List[cnt]+'.sam')
        else:
            targetMappings_List.append(targetfileName_List[cnt]+extension)
        cnt+=1
        
    cnt=0
    for extension in controlfileExtension_List:
        if isControl==0:
            break
        if isMapped(extension) == 0:
          ##  cmd=" "+bowtie2_dir + " -p " +num_proc+ " --very-fast -x " + bowtie2_index_dir + " -U " + controlfileName_List[cnt]+extension + " -S " + controlfileName_List[cnt]+".sam "
            cmd=" "+bowtie2_dir + " -p " +num_proc+ " --very-fast -x "+ bowtie2_index_dir + " -U " + controlfileName_List[cnt]+extension + " -S " + controlfileName_List[cnt]+".sam 2>"+controlfileName_List[cnt]+".maplog.txt"
            #cmd=batmis_dir+'batman -g '+batmis_index_dir+' -q '+ controlfileName_List[cnt]+extension + ' -o ' + controlfileName_List[cnt]+'.bin ' + ' -n 2 -U;'
            #cmd+=batmis_dir+'batdecode -g '+batmis_index_dir+' -i '+ controlfileName_List[cnt]+'.bin -o ' + controlfileName_List[cnt]+'.sam '
            print 'CMD: '+ cmd
            print '1.Mapping _control_ sequences...: '+controlfileName_List[cnt]+extension
            os.system(cmd)
            os.system("mv " + controlfileName_List[cnt]+".maplog.txt" + " " + output_dir)
            #cmd = 'rm ' + controlfileName_List[cnt]+'.bin '
            #os.system(cmd)
            print '1.Mapping '+ controlfileName_List[cnt]+' Done.'
            controlMappings_List.append(controlfileName_List[cnt]+'.sam')
        else:
            controlMappings_List.append(controlfileName_List[cnt]+extension)
        cnt+=1
        
    global targetPair
    global controlPair
    for bt2PairMap in (targetPair+controlPair):
        #print bt2PairMap 
        print '1.Mapping sequences... CMD: '+bt2PairMap
        os.system(bt2PairMap)

#This procedure takes in a sorted-rmdup file_path and create a .tags.unique file in the output_dir
def PrintTagsUnique(path):
    global output_dir
    
    fileName, fileExtension = os.path.splitext(os.path.basename(path))
    fileName=output_dir+fileName+'.tags.unique'
    
    os.system( ' bamToBed -i ' + path + " | " + " awk '{printf(\"%s\\t%d\\t%s\\n\", $1, ($2+$3)/2, $6)}' > " + fileName)

#This procedure takes all the mappings from our mapper and perform:
# bamConversion, sorting the aln wrt genomic location removing duplicates from each independent mapping file
# finally: merge all the rmdup-ed files into one single file for peak-caller
def ConvertToBam():
    delayDelete=list()
    toMergeTargets=''
    toMergeControls=''
    global targetfileName_List
    global controlfileName_List
    global targetMappings_List
    global controlMappings_List
    
    for tmpName in targetMappings_List:
        print tmpName
        print genome_length_path
        if FileType(tmpName)==0:    #sam
            os.system('samtools view -bS -q 10 ' + tmpName + ' > '+ tmpName+'.bam')
            os.system('rm '+tmpName)
        elif FileType(tmpName)==1:    #bam
            os.system('samtools view -b -q 10 ' + tmpName + ' > '+ tmpName+'.bam')
        elif FileType(tmpName)==2:    #bed
            os.system('bedToBam -i ' + tmpName + ' -g ' + genome_length_path + ' > ' + tmpName +'.bam')

        #print tmpName+"-bamTMP"
        os.system('samtools sort -m 10000000000 ' + tmpName+'.bam ' + tmpName+'_sorted')
        os.system('samtools rmdup -s ' + tmpName+'_sorted.bam ' + tmpName+'_rmdup.bam')
        toMergeTargets+=(tmpName+'_rmdup.bam ')
        
        #call function to create .tags.unique for zz
        PrintTagsUnique(tmpName+'_rmdup.bam')
        
        # cleanup
        os.system('rm '+ tmpName+'.bam; rm '+tmpName+'_sorted.bam;')
        delayDelete.append(tmpName+'_rmdup.bam ')
        
    for tmpName in controlMappings_List:
        if FileType(tmpName)==0: #sam
            os.system('samtools view -bS -q 10 ' + tmpName + ' > '+ tmpName+'.bam')
            os.system('rm '+tmpName)
        elif FileType(tmpName)==1: #bam
            os.system('samtools view -b -q 10 ' + tmpName + ' > '+ tmpName+'.bam')
        elif FileType(tmpName)==2:    #bed
            os.system('bedToBam -i ' + tmpName + ' -g ' + genome_length_path + ' > ' + tmpName +'.bam')
            
        os.system('samtools sort -m 10000000000 ' + tmpName+'.bam ' + tmpName+'_sorted')
        os.system('samtools rmdup -s ' + tmpName+'_sorted.bam ' + tmpName+'_rmdup.bam')        
        toMergeControls+=(tmpName+'_rmdup.bam ')
        
        #call function to create .tags.unique for zz
        PrintTagsUnique(tmpName+'_rmdup.bam')
        
        # cleanup
        os.system('rm '+ tmpName+'.bam; rm '+tmpName+'_sorted.bam;')
        delayDelete.append(tmpName+'_rmdup.bam ')
    
    #this line will merge the files!
    #Apparently samtools cannot merge 1 file, in our case... troublesome! (and we cannot create a dummy .bam fast)
    if len(toMergeTargets.split()) > 1: #assume we have at least 1 input target file
        cmd = 'samtools merge ' + targetfileName_List[0]+'_COMBINED.bam ' + toMergeTargets
    else :
        cmd = ' mv ' + toMergeTargets.split()[0] + ' ' + targetfileName_List[0]+'_COMBINED.bam '
    
    print 'CMD: ' + cmd
    os.system(cmd)
    os.system('mv ' + targetfileName_List[0] + '_COMBINED.bam ' + output_dir)
    
    if isControl != 0: 
        cnt=len(toMergeControls.split())
        if cnt > 1: #assume we have at least 1 input target file
            cmd = 'samtools merge ' + controlfileName_List[0]+'_COMBINED.bam ' + toMergeControls
        elif  cnt==1:
            cmd = ' mv ' + toMergeControls.split()[0] + ' ' + controlfileName_List[0]+'_COMBINED.bam '
        else:
            cmd = ' '
        
        print 'CMD: ' + cmd
        os.system(cmd)
        os.system('mv ' + controlfileName_List[0]+ '_COMBINED.bam ' + output_dir)
    
    #after merge then we delete the intermediate files!
    for removeTmp in delayDelete:
        os.system('rm '+removeTmp)

def PeakCall():

    global targetfileName_List
    global controlfileName_List
    global isControl

    targetfileName, targetfileExtension = os.path.splitext(os.path.basename(targetfileName_List[0]))
    
    macsCMD='macs14 -t '+ output_dir+targetfileName +'_COMBINED.bam -f auto -n ' +  output_dir+targetfileName
    if isControl!=0:
        controlfileName, controlfileExtension = os.path.splitext(os.path.basename(controlfileName_List[0]))
        macsCMD+=' -c '+ output_dir+controlfileName +'_COMBINED.bam '
    
    print "CMD: " + macsCMD
    os.system(macsCMD)        
        
def main():
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    print "0.Open Config File: "+sys.argv[1]
    setReadFiles()
    MapFiles()
    print "2.samtools sort/rmdup/merge on all aln files"
    ConvertToBam()
    if not mapOnly:
        print "3.Peak-Calling with MACS-1.4.2"
        PeakCall()
        print "4.MACS is done."
    
    os.system('rm batman.log; rm decode.log;')

main()