import grew 

def load_data(filename):
	"""Loads a UD graph from a specified location
	"""
	ud_graph = grew.graph(filename)
	return ud_graph 

def ud_graph_search(ud_graph, pattern): 
	"""Takes a ud_graph, as well as pattern, and searches for the latter in the former. 
	"""
	result = grew.corpus_search(pattern, ud_graph)
	return result 
	
def ud_to_amr(grs, ud_graph, strat):
	"""Takes a UD graph in CoNNL-U format and transforms
	it into an AMR graph by applying a set of rules
	Parameters: ud_graph - the UD graph to be transformed; grs_filename - str, the name of the file containing the GREW string representation of a grs

	Output: an AMR graph in GREW format
	"""
	grs = grew.grs(grs_filename)
	result = grew.run(grs, ud_graph, strat)
	return result 

def __test_is_dag__(amr_graph):
	"""
	Helper function for unit testing module. Takes a ud_graph, checks if it is a directed acyclic graph and if 
	there are 
	returns: integer 1 if yes, integer 0 if no

	"""
	
	
	pass

def __test_no_iso__(amr_graph):
	"""
	Helper function for unit testing module. Takes a ud_graph, checks that it does not have isolated components
	returns: integer 0 if yes, integer 1 if no
	"""
	pass


def __generate_nodetuples__(amr_graph):
	'''
	Helper function for __test_is_dag__ and __test_no_iso__ functions. Takes an amr_graph in dictionary form and 
	returns a list of all node-pairs in the graph. recall that amr graphs are directed, as 
	such the tuples are internally ordered (head, dep)
	'''
	nodetuples = []
	# iterate through every word (represented by its index number) in the amr_graph
	for word_idx in amr_graph:
		# in the GREW graph representation, the internal structure for each word 
		# is as follows: [{dictionary of features of the word}, 
		# [list of all dependents of the word[dependency relation, dependent word_idx]]]

		# get to list of all dependents of the word
		for dep in amr_graph[word_idx][1]: 
			# get to word_idx for each dependent
			nodetuples.append((word, dep[1]))

	return nodetuples

def __amr_graph_to_conllu__(amr_graph):
	'''
	Helper function. Takes an AMR in graph format, converts it into a format 
	for convenient writing to conllu file format with the save_data function. 
	'''

	pass 

def save_data(amr_graph):
	"""Takes an amr graph and saves it into a file

	Parameters: amr_graph - the AMR graph to be saved
	output | str - a string representing an AMR graph in conllu format.
	"""
	pass

if __name__== "__main__":
	grew.init()
	print("Grew initiated \n") 

	# load the UD graph 
	ud_graph = load_data("./data/dev_data/test_LP2half.conll")
	print("Grew graph loaded \n")

	# run a simple GRS 
	grs_filename = './grs/grs_amr_main.grs' 


	new_graph = ud_to_amr(grs_filename, ud_graph, strat="simple")
	print(new_graph)