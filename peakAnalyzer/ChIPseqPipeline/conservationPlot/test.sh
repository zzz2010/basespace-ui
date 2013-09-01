rm -rf test/output
mkdir test/output
#sh plotCons.sh test/treated.bed /home/chipseq/public_html/phastCons/hg19/ test/output


sh test/getPromoter.sh test/genelist > test/output/gene.bed
sh phastcon_bed.sh test/motitfsite2.bed /data5/zhizhuo/ChIPseqPipeline/phastCons/hg19/ test/output


~
