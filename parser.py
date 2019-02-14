from ufal.udpipe import Model, OutputFormat, Sentence, ProcessingError

def load_data():
	pass

def parse(text):
	"""Takes a sentence in raw text and produces
	its CoNLL-U annotation by invoking udpipe

	Paratemeters: text - the sentence to be parsed

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

	return conlluOutput.writeSentence(sentence)

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

def save_data(graph):
	"""Takes a UD graph in CoNNL-U format and saves it into a file

	Parameters: graph - the UD graph to be saved

	Output: True or False (maybe?) or no output at all (?) or the location of the file (?)
	"""
	pass

if __name__== "__main__":
	print(parse("I saw a magnificent picture."))
	print(parse("Hi there."))
	print(parse("Hi there. How are you?"))