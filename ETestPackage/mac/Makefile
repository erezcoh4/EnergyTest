/Users/erezcohen/Desktop/EnergyTest/AnaFiles/ETestResults_1.root:
	python calc_ETest.py 1

/Users/erezcohen/Desktop/EnergyTest/AnaFiles/ETestResults_2.root:
	python calc_ETest.py 2

/Users/erezcohen/Desktop/EnergyTest/AnaFiles/ETestResults_3.root:
	python calc_ETest.py 3

/Users/erezcohen/Desktop/EnergyTest/AnaFiles/ETestResults_4.root:
	python calc_ETest.py 4




/Users/erezcohen/Desktop/EnergyTest/AnaFiles/ETestResults_nbins_50.root: \
                /Users/erezcohen/Desktop/EnergyTest/AnaFiles/ETestResults_1.root \
                /Users/erezcohen/Desktop/EnergyTest/AnaFiles/ETestResults_2.root \
                /Users/erezcohen/Desktop/EnergyTest/AnaFiles/ETestResults_3.root \
                /Users/erezcohen/Desktop/EnergyTest/AnaFiles/ETestResults_4.root
	hadd /Users/erezcohen/Desktop/EnergyTest/AnaFiles/ETestResults_nbins_50.root /Users/erezcohen/Desktop/EnergyTest/AnaFiles/ETestResults_*.root


clean:
	rm -fr /Users/erezcohen/Desktop/EnergyTest/AnaFiles/ETestResults_*.root

