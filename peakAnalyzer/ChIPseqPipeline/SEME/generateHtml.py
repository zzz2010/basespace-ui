import os
import sys

outdir=sys.argv[1]
dirurl=outdir.replace("/home/sokemay/basespace/basespace-ui/basespace-ui","")
#print dirurl

def getScoreandFeature():
	scores=[]
	features=[]
	pwm=open(outdir+'SEME_clust.pwm','r')
	
	for line in pwm:
		if line.startswith("DE"):
			str_arr=line.split("\t")
			scores.append(str_arr[3])
			features.append(str_arr[4])
	
	return scores,features

def getKnownTf():
	known_tf=[]
	pwm_eval=open(outdir+'SEME_clust.pwm_eval.txt','r')
	lines=pwm_eval.readlines()
	for i in xrange(len(lines)):
		if lines[i].startswith('Similar Known Motifs'):
			break;
	for j in xrange((i+1),len(lines)):
		str_arr=lines[j].split("\t")
		known_tf.append("\n".join(str_arr[1:]))
	
	return known_tf

html_summary='<div style="padding-top:25px"><table class="table table-bordered">\
	<thead><tr><th>Summary</th></thead>\
	<tbody><tr>\
	<td style="text-align:center"><img  src="'+ dirurl +'SEME_clust.pwm_roc.png" class="img-polariod"></td></tr></tbody></table>'

score=[]
feature_detected=[]
known_tf=[]

(score,feature_detected) = getScoreandFeature()
known_tf=getKnownTf()

html_result='<table class="table table-bordered"><thead><tr><th>Motif Name</th><th>Logo</th><th>Known TF|PWM Divergence</th><th>Empirical Score</th><th>Feature Detected</th><th>Position Distribution</th><th>Sequence Rank Distribution</th></tr></thead><tbody>'
for i in xrange(1,6):
	title='Motif_clust'+str(i)
	logo=title+'.logo.png'
	pos_dist=title+'_posdist.png'
	rank_dist=title+'_rankdist.png'
	index=i-1
	row='<tr><td>'+ title +'</td><td><img width=300px height=200px src="'+dirurl+logo+'"></td><td width="20%">'+known_tf[index]+'</td><td>'+score[index]+'</td><td>'+feature_detected[index]+'</td><td><img width=300px height=200px src="'+dirurl+pos_dist+'"></td><td><img width=300px height=200px src="'+dirurl+rank_dist+'"></td></tr>'
	html_result+=row


html_output=html_summary+html_result+'</tbody></table></div>'
print html_output
