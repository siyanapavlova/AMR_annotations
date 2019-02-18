import re
def get_amr_sents(amrs_list): 
	'''a function to extract the sentence and the list of lines for the AMRs contained in a readlines pull from a 
	.txt file of AMR data
	input | a list containing a .readlines() pull from a .txt file of AMR data
	output | sentence: str - an unparsed sentence extracted from the AMR data; __amr_lines_prev: list - a list 
	containing the AMR representation in text. the elements of the list correspond to individual lines in this textual 
	AMR representation. 
	'''
	
	amr_lines_prev = []
	sentence = ''
	while len(amrs_list) != 0: 
		__ = amrs_list.pop(0)
		if not re.match(r"^[0-9]+",  __):
			amr_lines_prev.append(__)
		else:
			sentence = __
			break
	return sentence, amr_lines_prev

def preprocess(amrs_list, amrs_filepath_structure, sents_filepath_structure):

	'''
	takes a list of lines for the AMRs contained in a readlines pull from a .txt file of AMR data, extracts each 
	sentence and each AMR (in textual representation) and writes the sentence to a .txt file, and the same for the 
	textual AMR in another .txt file. It recursively calls the get_amr_sents function. 
	input | a list containing a .readlines() pull from a .txt file of AMR data; amrs_filepath_structure; str - the 
	structure of the file path for storing the .txt files for textual AMRs; sents_filepath_structure; str - the 
	structure of the file path for storing the .txt files for sentences. 
	output | .txt files for each sentence and textual AMR 
	in the dataset
	'''

	sent_written_count = 0 
	while len(amrs_list) !=0:
		__sentence, __amr_lines_prev = get_amr_sents(amrs_list)

		try: 
			sent_num = re.Match.group(re.match(r"^[0-9]+", __sentence))
			sentence_only = __sentence.lstrip(sent_num+". ")
			sent_num4file = sent_num if len(sent_num) == 4 else "0" * (4-len(sent_num))+sent_num

		# exception to catch the case when dealing with the last text AMR obtained (which would not have
		# a subsequent sentence number in order to establish its file name. )
		except TypeError:
			sent_num = sent_written_count+1


		with open (sent_filepath_structure.format(sent_num4file), 'w') as file:
			file.write(sentence_only)
			file.close()

		# write the amr_lines into a file with its corresponding sentence number. recall that as we loop through 
		# the amrs_list, __amr_lines_prev collects lines that are for the preceding sentence. 
		sent_num_prev = str(int(sent_num)-1)
		sent_num4file_prev = sent_num_prev if len(sent_num_prev) == 4 else "0" * (4-len(sent_num_prev))+sent_num_prev

		with open (amrs_filepath_structure.format(sent_num4file_prev), 'w') as file:
			for line in __amr_lines_prev:
				file.write(line)
			file.close()
		sent_written_count+=1


if __name__== "__main__":
	data = open("./data/amr_bank_data/amr_bank/amr-bank-v1.4.txt")
	amrs = data.readlines()
	amrs_filepath_structure = './data/amr_bank_data/amrs/amr{}.txt'
	sents_filepath_structure = './data/amr_bank_data/sentences/sentence{}.txt'
	preprocess(amrs, amrs_filepath_structure, sent_filepath_structure)
