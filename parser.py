from ufal.udpipe import Model, OutputFormat, Sentence, ProcessingError
import re
import os

def load_data(file):
	"""Loads a sentence and its ID from a text file.
	A file is expected to contain one sentence and its ID after the sentence
	enclosed in brackets. (e.g. "Today is a beutiful day. (001)")

	Parameters: file - the path to the file to be loaded

	Output: the sentence ID and the sentence itself
	"""
	#Load the data from a file
	with open(file) as f:
		sentence = f.read()

	#Find the sentence_id
	pattern = re.compile(r'\(.*\)$')
	sentence_id = pattern.search(sentence)
	#return the sentence_id and the sentence itself
	return (sentence_id.group()[1:-1], sentence.replace(sentence_id.group(), ''))
	

def parse(text, sentence_id):
	"""Takes a sentence in raw text and produces
	its CoNLL-U annotation by invoking udpipe

	Paratemeters: text - the sentence to be parsed
				  sentence_id - the ID of the sentence

	Output: a UD graph
	"""
	model = Model.load('./models/udpipe/english-ewt-ud-2.3-181115.udpipe')

	tokenizer = model.newTokenizer(model.DEFAULT)

	conlluOutput = OutputFormat.newOutputFormat("conllu")

	sentence = Sentence()

	error = ProcessingError()

	tokenizer.setText(text)

	tokenizer.nextSentence(sentence, error)

	model.tag(sentence, model.DEFAULT)

	model.parse(sentence, model.DEFAULT)

	return conlluOutput.writeSentence(sentence).replace('# sent_id = 1', '# sent_id = '+sentence_id)

	# This loop would allow us to pass whole text and not just a sentence
	# to udpipe. However, since at this stage we are working with sentences,
	# it is not necessary. We already have the data split into sentences.
	# The way it is split will depend on the model too? Or does udpipe use an
	# external tokenizer?

	# conllu_list = []
	# while tokenizer.nextSentence(sentence, error):
	# 	model.tag(sentence, model.DEFAULT)
	# 	model.parse(sentence, model.DEFAULT)
	# 	conllu_list.append(conlluOutput.writeSentence(sentence))
	# return conllu_list

def save_data(graph, directory, filename):
	"""Takes a string and saves it in a directory under a given name
	Intended to be used with UD graphs in CoNNL-U format

	Parameters: graph - the UD graph to be saved
				directory - the directory where the file should be saved
				filename - the name under which the file should be saved

	Output: True or False (maybe?) or no output at all (?) or the location of the file (?)
	"""

	#check if the directory exists and create it if it does not
	if not os.path.exists(directory):
		os.makedirs(directory)
	#write the graph in a file in the provided directory
	with open(directory+filename, 'w') as f:
		f.write(graph)
	return True

def parse_files_in_folder(read_folder, write_folder):
	"""Takes a folder containing .txt files with sentences,
	parses them and saves them into another folder

	Paramenters: read_folder - the folder where the original .txt files are located
				 write_folder - the folder where the parsed sentences should be saved

	Output: none
	"""
	for filename in os.listdir(read_folder):
		if filename.endswith('.txt'):
			print(filename)
			sentence_id, sentence = load_data('./data/amr_bank_data/sentences/'+filename)
			parsed_data = parse(sentence, sentence_id)
			save_data(parsed_data, write_folder, filename[:-3]+'conll')

if __name__== "__main__":
	#Parse the sentences from the amr bank (The Little Prince)
	parse_files_in_folder('./data/amr_bank_data/sentences/', './data/amr_bank_data/ud/')