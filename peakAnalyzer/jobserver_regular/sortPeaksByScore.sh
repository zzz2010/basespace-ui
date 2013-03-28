 outdir=$1
 
 for f in $outdir*summits.bed
 do
 	echo $f
 	sort -k 5 -nr $f 
done