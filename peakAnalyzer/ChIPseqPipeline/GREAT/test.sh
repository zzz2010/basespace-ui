rm -r test/
mkdir test/

awk '{print $1"\t"$2"\t"$3"\t"$1":"$2"-"$3}' treated2.bed > treated.bed
python great.py treated2.bed hg19  /home/sokemay/ChIPseqPipeline/GREAT/test/


for f in /home/sokemay/ChIPseqPipeline/GREAT/test/*.great.xls;
do python generateHtmlTable.py $f > $f.html;
done;
