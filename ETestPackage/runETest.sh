# operate using
# > ./runETest <Nbins> <cutoff parameter = 0.6617>
Nsamples=30
echo "Nbins = $1, cutoff parameter = $2, Nsamples=$Nsamples"
for i in {1..60}
do
nohup python mac/calc_ETest.py $1 $Nsamples $i $2 > nohupout/ETest_$1_$2_$i.txt &
echo "launched ETest with Nbins = $1 cutoff parameter $2 number $i"
done
echo "done Nbins=$1 cutoff=$2"
