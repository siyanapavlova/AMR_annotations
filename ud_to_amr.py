import grew 
import amr_graph_to_conllu 

ud_tags = ['nsubj', 'obj', 'iobj', 'obl', 'vocative', 'expl', 'dislocated', 'nmod',
			'appos', 'nummod', 'csubj', 'ccomp', 'xcomp', 'advcl', 'advmod*', 'discourse',
			'aux', 'cop', 'mark', 'acl', 'amod', 'det', 'clf', 'case', 'conj', 'cc', 'fixed',
			'flat', 'compound', 'list', 'parataxis', 'orphan', 'goeswith', 'reparandum',
			'punct', 'root', 'dep']

def load_data(filename):
	"""
	Loads a UD graph from a specified location.
	
	input | filename: str - the filepath for the file containing the AMR graph (either in conllu or GREW dictionary 
	format)
	output | dict - a single AMR graph in GREW dictionary format
	"""
	ud_graph = grew.graph(filename)
	return ud_graph 

def ud_graph_search(ud_graph, pattern): 
	"""
	Takes a ud_graph, as well as a pattern, and searches for the latter in the former. 

	input | 
	output | 
	"""
	result = grew.corpus_search(pattern, ud_graph)
	return result 
	
def ud_to_amr(grs_filename, ud_graph, strat): 
	"""
	Takes a UD graph in CoNNL-U format and transforms it into an AMR graph by applying a set of rules
	
	input | ud_graph: dict - the UD graph to be transformed; grs_filename: str - the filepath of the file containing 
	the GREW string representation of a grs
	output| list - containing one, or more (if there is more than 1 solution), AMR graph in GREW dictionary form. 
	"""
	grs = grew.grs(grs_filename)
	result = grew.run(grs, ud_graph, strat)
	return result 

def save_data(amr_graph, filepath):
	"""
	Takes an amr graph and saves it into a file
	input | amr_graph: dict - the AMR graph to be saved, in GREW dictionary form
	output | a .conllu file containing the AMR graph in conllu format.
	"""
	amr_conllu = amr_graph_to_conllu.__amr_graph_to_conllu__(amr_graph)
	with open(filepath, 'w') as file:
		file.write(amr_conllu)
		file.close()

if __name__== "__main__":
	grew.init()
	print("Grew initiated \n") 

	# load the UD graph 
	ud_graph = load_data("./data/amr_bank_data/ud/sentence0347.conll")
	print("Grew graph loaded \n")
	print(ud_graph)

	# run a simple GRS 
	grs_filename = './grs/grs_amr_main.grs' 

	# generate the graph(s) from the application of the grs in grs_filename
	new_graphs = ud_to_amr(grs_filename, ud_graph, strat="test_new_lex")
	print(new_graphs[0])
