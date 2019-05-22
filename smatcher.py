import smatch
import subprocess

def get_smatch_score(text_amr_file1, text_amr_file2):
	'''
	takes two files, each containing one (if the .txt file contain more than one, only the first will be analysed) 
	textual representation, computing their similarity score by calling smatch.py and returning it. guide for usage 
	of smatch.py here: https://amr.isi.edu/eval/smatch/smatch-guide.pdf
	input | text_amr_file1: str - the filepath or file handle for the .txt file, text_amr_file2: str - the filepath 
	or file handle for the .txt file
	output: float - a semantic similarity score computed by smatch.py
	'''

	smatchpy_loc = 'python ./data/smatch-master/smatch.py -f {} {} --pr'
	subprocess_cmd = smatchpy_loc.format(text_amr_file1, text_amr_file2)
	try:
		response = subprocess.check_output(subprocess_cmd, shell=True)
	except subprocess.CalledProcessError:
		response = "The filenames provided could not be found or opened. Please check and retry."

	return response


if __name__== "__main__":
	file1 = "./data/dev_data/eatApplesTom.txt"
	file2 = "./data/dev_data/eatTomApples.txt"
	print(get_smatch_score(file1,file2))
	
	pass