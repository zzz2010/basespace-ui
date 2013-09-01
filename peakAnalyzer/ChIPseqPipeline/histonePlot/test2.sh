rm -r test/output
mkdir test/output

cd test/vcap
sh getPEO.sh
cd ..
cd ..

#
python plotHistoneDist.py test/vcap/CHV029.peak.cutoff.bed.class.bed.e vcap2h test/vcap/  test/output &

python plotHistoneDist.py test/vcap/CHV029.peak.cutoff.bed.class.bed.p vcap2h test/vcap/  test/output &

python plotHistoneDist.py test/vcap/CHV029.peak.cutoff.bed.class.bed.o vcap2h test/vcap/  test/output &


python plotHistoneDist.py test/vcap/CHV031.peak.cutoff.bed.class.bed.e vcap2h test/vcap/  test/output &

python plotHistoneDist.py test/vcap/CHV031.peak.cutoff.bed.class.bed.p vcap2h test/vcap/  test/output

python plotHistoneDist.py test/vcap/CHV031.peak.cutoff.bed.class.bed.o vcap2h test/vcap/  test/output
#
#
#python plotHistoneDist.py test/gene.bed BroadHistoneHelas3 ../broad_histone/hg19/  test/output
~
