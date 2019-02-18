import smatch
import subprocess

def get_smatch_score(text_amr_file1, text_amr_file2):
	smatchpy_loc = 'python ./data/smatch-master/smatch.py -f {} {}'
	subprocess_cmd = smatchpy_loc.format(text_amr_file1, text_amr_file2)
	try:
		response = subprocess.check_output(subprocess_cmd, shell=True)
	except subprocess.CalledProcessError:
		response = "The filenames provided could not be found or opened. Please check and retry."

	return response


if __name__== "__main__":
	file1 = "./data/amr_bank_data/amrs/amr0001.txt"
	file2 = "./data/amr_bank_data/amrs/amr0001.txt"
	print(get_smatch_score(file1,file2))
	pass