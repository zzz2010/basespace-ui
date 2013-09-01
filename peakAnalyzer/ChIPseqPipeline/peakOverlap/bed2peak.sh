awk 'BEGIN{OFS="\t";$2=($2+$3)/2}{print $1,$2,$5}'  $1 
