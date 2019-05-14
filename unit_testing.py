import unittest
from ud_to_amr import ud_to_amr
import grew
import pprint
import os

pp = pprint.PrettyPrinter(indent = 4)

amr_roles = [':ARG0', ':ARG1', ':ARG2', ':ARG3', ':ARG4', ':ARG5',
			':accompanier', ':age', ':beneficiary',
			':concession', ':condition', ':consist-of',
			':degree', ':destination', ':direction', ':domain', ':duration',
			':example', ':extent', ':frequency', ':instrument', ':li', ':location',
			':manner', ':medium', ':mod', ':mode', ':name', ':ord',
			':part', ':path', ':polarity', ':polite', ':poss', ':purpose',
			':quant', ':range', ':scale', ':source', ':subevent',
			':time', ':topic', ':unit', ':value', ':wiki',
			':calendar', ':century', ':day', ':dayperiod', ':decade',
			':era', ':month', ':quarter', ':season', ':timezone', ':weekday', ':year', ':year2']
#need regex-es for :op1, :op2, ... :opN,:prep-* and :conj-*

grew.init()
# g = grew.graph( '''graph {
# 	W1 [ phon ="the", cat =DET ];
# 	W2 [ phon ="child", cat =N];
# 	W3 [ phon ="plays", cat =V];
# 	W4 [ phon ="the", cat =DET ];
# 	W5 [ phon ="fool", cat =N];
# 	W2 -[det ]->W1;
# 	W3 -[suj ]->W2;
# 	W3 -[obj ]->W5;
# 	W5 -[det ]->W4;
# }''')

class ParserTest(unittest.TestCase):

	def has_pos(self):
		'''every word should have a POS tag'''
		pass

	def has_lemma(self):
		'''every word should have a lemma'''
		pass

	def has_incoming_deprel(self):
		'''every word should have an incoming dependency relation'''
		pass

	def has_features(self):
		'''every word should have features'''
		pass

class UDtoAMRtest(unittest.TestCase):

	test_graphs = []
	grs_filename = './grs/grs_amr_main.grs'

	for filename in os.listdir("./data/dev_data/ud_graphs/"):
		if filename.endswith('.conll'):
			ud_graph = load_data("./data/dev_data/ud_graphs/"+filename)
			test_graphs.extend(ud_to_amr(grs_filename, ud_graph, strat="simple"))
	print(test_graphs)

	def test_has_no_iso(self):
		'''UD_to_AMR should produce graphs whithout isolated components'''
		for amr_graph in self.test_graphs:
			result = __test_no_iso__(amr_graph)
			self.assertEqual(1, result)

	def test_has_only_AMR_tags(self):
		'''UD_to_AMR should produce a graph which has only AMR tags'''
		for amr_graph in self.test_graphs:
			# pp.pprint(amr_graph)
			result = __test_only_AMR_tags__(amr_graph)
			self.assertEqual(1, result)

	# def test_every_edge_has_label(self):
	# 	'''UD_to_AMR should produce a graph in which every edge has a label'''
	# 	for amr_graph in self.test_graphs:
	# 		result = __every_edge_has_label__(amr_graph)
	# 		self.assertEqual(1, result)


def __test_no_iso__(amr_graph):
	"""
	Helper function for unit testing module. Takes a ud_graph, checks that it does not have isolated components
	
	input | amr_graph: dict - an AMR graph in GREW dictionary form 	
	output | int - 1 if yes, 0 if no
	"""
	node_tuples = __generate_nodetuples__(amr_graph)
	simple_graphrep = __generate_simple_graphrep__(node_tuples)

	# get all the nodes in the amr_graph with at least 1 connection
	nodes_all = set([i[0] for i in node_tuples] + [i[1] for i in node_tuples])

	# get all the head nodes present in the amr_graph (i.e. leaving out all the leaf nodes). 
	nodes_heads = set([i for i in simple_graphrep.keys()])
	
	assert len(simple_graphrep["ROOT"]) == 1, "It appears this graph may have more than 1 root, \
	AMRs can only have a single root. Please check."
		# AMRs should only have 1 root node, so simple_graphrep["ROOT"] should return a list of one 
		# element, which contains a str that is the index number for the root word. 
	
	# start searching with "ROOT". 
	nodes_to_visit = set(["ROOT"])
	nodes_visited = set()
	
	# recursion to visit all nodes accessible from "ROOT", stop when nodes_to_visit empty, or 
	# if visited nodes matches the list of all nodes in the amr_graph (i.e. all nodes are connected). 
	while len(nodes_to_visit) > 0:
		# .pop on a set removes a random element. but this does not matter, we only want to 
		# be sure to have visited all head nodes once, so the order of visit does not matter. 
		__visiting_node = nodes_to_visit.pop()
	
		for node1 in simple_graphrep[__visiting_node]:
			# check that node1 is not a leaf node before adding to nodes_to_visit. 
			nodes_visited.add(node1)
			if node1 in nodes_heads: 
				nodes_to_visit.add(node1)
		
		nodes_visited.add(__visiting_node)
		if nodes_visited == nodes_all:
			return 1
	return 0 # returns zero if we can't match nodes_visited with nodes_all

def __test_only_AMR_tags__(amr_graph):
	"""
	Helper function for unit testing. Takes an amr_graph, checks that none of the tags are UD tags

	input | amr_graph - an AMR graph in GREW dictionary format
	output | 1 if no UD tags, 0 if there are UD tags
	"""
	for node in amr_graph[0]:
		for relation in amr_graph[0][node][1]:
			if relation[0] in ud_tags:
				# print('UD TAAAAAGS ', relation[0])
				return 0
	return 1

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


if __name__== "__main__":
	unittest.main()
