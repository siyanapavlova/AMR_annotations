import grew 
from amr_graph_to_conllu 

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
	
def ud_to_amr(grs, ud_graph, strat):
	"""
	Takes a UD graph in CoNNL-U format and transforms it into an AMR graph by applying a set of rules
	
	input | ud_graph: dict - the UD graph to be transformed; grs: str - the filepath of the file containing 
	the GREW string representation of a grs
	output| list - containing one, or more (if there is more than 1 solution), AMR graph in GREW dictionary form. 
	"""
	grs = grew.grs(grs_filename)
	result = grew.run(grs, ud_graph, strat)
	return result 

def __test_amr_is_dag__(amr_graph):
	"""
	Helper function for unit testing module. Takes a ud_graph, checks if it is a directed acyclic graph. 
	Leverages the following properties: (i) directed nature of conllu format; (ii) single-root characteristic 
	UD and AMR frameworks; as a result, not generalisable to other graphs that don't have these two properties.  
	
	input | amr_graph: dict - an AMR graph in GREW dictionary form 
	output | int - 1 if yes, 0 if no

	"""
	
	
	pass

def __test_no_iso__(amr_graph):
	"""
	Helper function for unit testing module. Takes a ud_graph, checks that it does not have isolated components
	
	input | amr_graph: dict - an AMR graph in GREW dictionary form 	
	output | int - 1 if yes, 0 if no
	"""
	node_tuples = __generate_nodetuples__(amr_graph)
	simple_graphrep = __generate_simple_graphrep__(node_tuples)

	# get all the nodes in the amr_graph, except the "ROOT"
	nodes_all = set([i for i in simple_graphrep.keys() if i != "ROOT"])
	# start searching with dep node of "ROOT"
	node_root = simple_graphrep["ROOT"]
	nodes_to_visit = set(node_root)
	nodes_visited = set()
	
	# recursion to visit all nodes, stop when nodes_to_visit empty, or if visited nodes matches 
	# the list of all nodes in the amr_graph (i.e. all nodes are connected). 
	while len(nodes_to_visit) > 0:
		__visiting_node = nodes_to_visit.pop()
		for node1 in simple_graphrep[__visiting_node]:
			nodes_to_visit.add(node1)
		
		nodes_visited.add(__visiting_node)
		if nodes_visited == nodes_all:
			return 1
	return 0


def __generate_nodetuples__(amr_graph):
	'''
	Helper function for __test_is_dag__ and __test_no_iso__ functions. Takes an amr_graph in dictionary form and 
	returns a list of all node-pairs in the graph. recall that amr graphs are directed, as 
	such the tuples are internally ordered (head, dep)
	input | amr_graph: dict - an AMR graph in GREW dictionary form 	
	output | list - a list containing all the node pairs (i.e. connected by an edge) in amr_graph
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
			nodetuples.append((word_idx, dep[1]))

	return nodetuples

def __generate_simple_graphrep__(nodetuples):
	'''
	Helper function for __test_is_dag__ and __test_no_iso__ functions. Takes a list of node tuples and transforms 
	them into a simplified graph representation. Necessary for the __test_no_iso__ function as the GREW graph dictionary
	transformations does not delete words that are not present in the AMR (so as to allow the surface representation
	of the original sentence to be recovered easily.)
	'''
	simple_graphrep = {}

	for nodetuple in nodetuples:
		head = nodetuple[0]
		dep = nodetuple[1]
		try: 
			simple_graphrep[head].append(dep)
		except KeyError:
			simple_graphrep[head] = list(dep)

	return simple_graphrep

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
	ud_graph = load_data("./data/dev_data/test_LP2half.conll")
	print("Grew graph loaded \n")

	# run a simple GRS 
	grs_filename = './grs/grs_amr_main.grs' 

	# generate the graph(s) from the application of the grs in grs_filename
	new_graphs = ud_to_amr(grs_filename, ud_graph, strat="simple")
