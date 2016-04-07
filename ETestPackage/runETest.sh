Nsamples=30
echo "Nbins = $1, Nsamples=$Nsamples"
for i in {1..60}
 do
    nohup python mac/calc_ETest.py $1 $Nsamples $i > nohupout/ETest_$1_$i.txt &
    echo "launched ETest with Nbins = $1 number $i"
 done
echo "done Nbins=$1"
