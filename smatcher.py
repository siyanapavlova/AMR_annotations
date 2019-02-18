import smatch
import subprocess



if __name__== "__main__":
	file1 = "./data/amr_bank_data/amrs/amr0001.txt"
	file2 = "./data/amr_bank_data/amrs/amr0001.txt"
	result1 = subprocess.check_output('ls', shell=True)
	print(result1)
	result2 = subprocess.check_output('python ./data/smatch-master/smatch.py -f {} {}'.format(file1, file2), shell=True)
	print(result2)
	pass