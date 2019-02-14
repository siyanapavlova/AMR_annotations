import grew 

def load_data(filename):
	"""Loads a UD graph from a specified location
	"""
	grew.init()
	ud_graph = grew.corpus(filename)
	return ud_graph 

def ud_graph_search(ud_graph, pattern): 
	"""Takes a ud_graph, as well as pattern, and searches for the latter in the former. 
	"""
	result = grew.corpus_search(pattern, ud_graph)
	return result 
	
def ud_to_amr(ud_graph):
	"""Takes a UD graph in CoNNL-U format and transforms
	it into an AMR graph by applying a set of rules
	Parameters: ud_graph - the UD graph to be transformed; grs_filename - str, the name of the file containing the GREW string representation of a grs

	Output: an AMR graph in GREW format
	"""
	grs = grew.grs(grs_filename)
	result = grew.run(grs, ud_graph, strat)
	return result 


	pass

def save_data(amr_graph):
	"""Takes an amr graph and saves it into a file

	Parameters: amr_graph - the AMR graph to be saved
	"""
	pass

if __name__== "__main__":
	# load the UD graph 
	ud_graph = load_data("./test_LP2half.conll")
	# run a simple GRS 
	grs_filename = './grs/core_roles.grs' 
	grs = grew.grs(grs_filename)
	print("GRS file loaded:", grs)
	new_graph = ud_to_amr(grs_filename, ud_graph, strat="coord_gov_share")
	# new_graph = ud_to_amr(grs_filename, ud_graph, strat="noun_amod")
	# new_graph = ud_to_amr(grs_filename, ud_graph, strat="remove_det")
	pass