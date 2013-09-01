ccatpeak=$1
FC=$2


awk -v FC=$FC '{OFS="\t";if($7>FC){print $1,$2,$2+1,$3,$4,$5,$6,$7,$8}}'  $ccatpeak
