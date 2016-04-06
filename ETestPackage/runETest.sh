for i in {1..60}
 do
    nohup python mac/calc_ETest.py $i > ETest_$i.txt &
    echo "launched ETest $i"
 done
