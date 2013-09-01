import os
import sys
from collections import defaultdict

greatOut=sys.argv[1]
outdir=sys.argv[2]

def getTermUrl(ontology, term_id):
	url=''
	if 'GO' in ontology:
		url='http://amigo.geneontology.org/cgi-bin/amigo/term_details?term='+term_id
	elif 'Mouse Phenotype' in ontology:
		url='http://www.informatics.jax.org/searches/Phat.cgi?id='+term_id
	elif 'Human Phenotype' in ontology:
		url='http://www.human-phenotype-ontology.org/hpoweb/showterm?id=' + term_id
	elif 'Disease Ontology' in ontology:
		extractedid=term_id.split(':')[1]
		url='http://bioportal.bioontology.org/ontologies/49838?p=terms&conceptid=DOID%3A' + extractedid
	elif 'MSigDB' in ontology:
		url='http://www.broadinstitute.org/gsea/msigdb/cards/'+term_id
	elif 'Placenta Disorders' in ontology:
		url='#'
	elif 'PANTHER' in ontology:
		url='http://www.pantherdb.org/pathway/pathwayDiagram.jsp?catAccession='+term_id
	elif 'Pathway Commons' in ontology:
		url='http://www.pathwaycommons.org/pc/record2.do?id='+term_id
	elif 'BioCyc' in ontology:
		url='http://biocyc.org/META/new-image?object='+term_id
	elif 'MGI Expression' in ontology:
		url='http://www.informatics.jax.org/searches/anatdict.cgi?id=' + term_id
	elif ('Transcription Factor Targets' or 'miRNA Targets') in ontology:
		url='http://acgt.cs.tau.ac.il/amadeus/suppl/metazoan_compendium.htm'
	elif 'InterPro' in ontology:
		url='http://www.ebi.ac.uk/interpro/DisplayIproEntry?ac='+term_id
	elif 'TreeFam' in ontology:
		url='http://www.treefam.org/cgi-bin/TFinfo.pl?ac='+term_id
	elif 'HGNC' in ontology:
		extractedid=term_id.split(',')[0]
		url='http://www.genenames.org/genefamily/'+extractedid+'.php'
		
	return url


#input:line in great out file split by tabs and column indices to select cols
def generateHtmlRow(arr,colindex, ontology):
	#selected index to display exclu term info
	
	binomfdr=float(arr[6])
	hyperfdr=float(arr[15])

	str_tmp=''
	if binomfdr <= 0.05 or hyperfdr <=0.05:
		#write peak-gene pairs to tmp file
		pkgenefile=open(outdir+'/peakGenePairs.tmp','a')
		pkgenepair=arr[22] +'\t'+arr[23]
		pkgenefile.write(pkgenepair)
		#create rows for tables
		term_id=arr[1]
		term_url=getTermUrl(ontology, term_id)
		str_tmp='<td><a target="_blank" href='+term_url+'>' + arr[2] + '</a></td>\n'
		for i in colindex:
			if i==11 or i==20:  #term and set coverage cols
				val=float(arr[i]) *100
				val='%.3g'%(val)
				value=str(val)+'%'
			else:
				value='%.5g'%(float(arr[i]))

			str_tmp=str_tmp+'<td>'+value+'</td>\n'
		str_out='<tr>'+str_tmp+'</tr>'
	else:
		str_out=''
	
	return str_out

def generateHtmlHead(header):
	html_head="<thead><tr>"
	for n in header:
		col="<th>"+n+"</th>"
		html_head= html_head+col+"\n"
	html_head=html_head+"</tr></thead>"
	return html_head

out=open(greatOut, "r")
lines=out.readlines()

colnames=['Term Name','Binom Rank','Binom Raw P-Val','Binom FDR Q-Val','Binom Fold Enrichment','Binom Observed Region Hits','Binom Region Set Coverage','Hyper Rank','Hyper Raw P-Val','Hyper FDR Q-Val','Hyper Fold Enrichment','Hyper Observed Gene Hits','Hyper Total Genes','Hyper Gene Set Coverage']
colindex=[3,4,6,7,9,11,12,13,15,16,18,19,20]
html_head=generateHtmlHead(colnames)

#table
result=lines[5:]

i=0
curr=result[0]
html_tables={}
ontology=''
while not curr.strip().startswith("#") and i<len(result):
	arr=curr.split("\t")
	ontology=arr[0]
	#create rows for current table
	html_row= generateHtmlRow(arr, colindex, ontology)
	
	#if str not empty
	#if ontology not already added in dict
	if ontology in html_tables.keys():	
		html_tables[ontology].append(html_row)
	else:
		html_tables[ontology]=[html_row]
		
	i=i+1
	curr=result[i]
#	print curr

html_out='<div class="accordion" id="accordion2">'
keylist=html_tables.keys()
keylist.sort()
for k in keylist:
	k_nospace=k.replace(" ","")
	k_nospace=k_nospace.replace(":","-")
	html_out = html_out +'<div class="accordion-group"><div class="accordion-heading"><a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapse_' +k_nospace+'">'+k+'</a></div><div id="collapse_'+k_nospace+'" class="accordion-body collapse in"><div class="accordion-inner"><table style=font-size:90% cellpadding="0" cellspacing="0" border="0" class="table table-striped table-bordered table-condensed" id="table_'+k_nospace+'">' + html_head + "".join(html_tables[k]) + '</table></div></div></div>' 
	
html_out=html_out+"</div>"
print html_out



