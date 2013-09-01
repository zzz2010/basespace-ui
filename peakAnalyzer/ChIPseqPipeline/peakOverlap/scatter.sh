
col=$3
distance=$4


r1=/tmp/$RANDOM
r2=/tmp/$RANDOM
r3=/tmp/$RANDOM
cut -f 1-3,$col $1 > $r1
cut -f 1-3,$col $2 > $r2


closestBed -a $r1 -b $r2 -d |awk -v ds=$distance '{OFS="\t"; if($9<ds&&$8!="."){print $4,$8}  }' > $r3

r4=/tmp/$RANDOM
r5=/tmp/$RANDOM

windowBed -w $distance -v -a $r1 -b $r2 |awk '{OFS="\t"; print $4,0}' >> $r3
windowBed -w $distance -v -b $r1 -a $r2 |awk '{OFS="\t"; print 0,$4}' >> $r3

cat $r3

rm $r1 $r2 $r3
