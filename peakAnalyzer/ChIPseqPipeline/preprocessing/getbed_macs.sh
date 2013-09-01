macsxls=$1
FC=$2

awk -v FC=$FC '{OFS="\t"; if(NF>7&&FNR>20){if($8>FC&&$3==int($3)){print $1,$2+$5,$2+$5+1,$2,$3,$6,$7,$8,$9}}}' $macsxls|sort -k 8nr 
