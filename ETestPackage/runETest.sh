# operate using
# > ./runETest <Nbins> <cutoff parameter = 0.6617>
Nsamples=30
cutoff=0.6617
Nbins=$1
Contamination=$2
echo "Nbins = $1, cutoff parameter = $cutoff , contamination = $2, Nsamples = $Nsamples"
for i in {1..60}
do
nohup python mac/calc_ETest.py $Nbins $Nsamples $i $cutoff $Contamination > nohupout/ETest_$1_contamination_$2_$i.txt &
echo "launched ETest with Nbins = $1 Contamination $2 number $i"
done
echo "done Nbins=$1 Contamination=$2"
