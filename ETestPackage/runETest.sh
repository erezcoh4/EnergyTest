for i in {1..60}
 do
    nohup python mac/calc_ETest.py 40 50 $i > nohupout/ETest_40_$i.txt &
    echo "launched ETest with Nbins = 40 number $i"
 done
echo "done Nbins=40"

for i in {1..60}
 do
    nohup python mac/calc_ETest.py 50 40 $i > nohupout/ETest_50_$i.txt &
    echo "launched ETest with Nbins = 50 number $i"
 done
echo "done Nbins=50"
