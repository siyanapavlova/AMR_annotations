import grew
import pprint

pp = pprint.PrettyPrinter(indent = 4)

#TODO: add more relations to this list
amr_rels = ['ARG0', 'ARG1', 'ARG2', 'ARG3', 'ARG4', 'ARG5', 'ARG6', 'ARG7', 'ARG8', 'ARG9',
			'accompanier', 'age', 'beneficiary', 'concession', 'condition', 'consist-of',
			'degree', 'destination', 'direction', 'domain', 'duration', 'example', 'extent',
			'frequency', 'instrument', 'li', 'location', 'manner', 'medium', 'mod', 'mode',
			'name', 'ord', 'part', 'path', 'polarity', 'polite', 'poss', 'purpose', 'quant',
			'range', 'scale', 'source', 'subevent', 'time', 'topic', 'unit', 'value', 'wiki',
			':calendar', ':century', ':day', ':dayperiod', ':decade', ':era', ':month',
			':quarter', ':season', ':timezone', ':weekday', ':year', ':year2',
			'op1', 'op2', 'op3', 'op4']

def amr_text_to_grew(amr_text):
	'''
	Given an AMR graph in text, produce the corresponding GREW graph
	Input:
	amr_text - the text representation of the AMR graph
	Output: a GREW graph
	'''
	pass

def group_by_relation(graphs, relations):
	'''
	Give a list of GREW graphs and a list of relations, for each relation
	return a the list of the indeces of the graphs containing that relation
	Inputs:
	sentences - a list of GREW graphs
	relations  - a list of relations
	Output: a dictionary where the keys are the relations and the values are
			lists of graphs containing the corresponding relation
	'''
	graphs_by_relation = {key: [] for key in relations}
	#For each graph
	for ind, g in enumerate(graphs):
		#Make a set of all the relations contained in that graph
		graph_rels = set()
		for node in g:
			for rel in g[node][1]:
				graph_rels.add(rel[0])
		#For each of the relations contained in the graph,
		#append the graph index to the list of graphs associated with that relation
		for rel in graph_rels:
			if rel in graphs_by_relation:
				graphs_by_relation[rel].append(ind)

	return graphs_by_relation

def split_by_relations(sentences, relations1, relations2):
	'''
	Given a list of GREW graph and two lists of relations,
	split the first list into 4 categories:
	1. graphs not containing any of the relations from any of the lists
	2. graphs containing only relations from the first list
	3. graphs containing only relations from the second list
	4. graphs conitaning relations from both lists
	'''
	pass

def map_lemma_amr_ud(amrgraph, udgraph, amr_relation):
    '''
    given an AMR graph and its associated UD graph, searches for all nodes in the AMR GREW graph that has the 
    amr_relation that is passed into the function. The resulting list of token_num-lemma pairs are searched for
    in the UD GREW graph. The resulting token_num-lemma pairs are for nodes in the UD graph whose token_num and lemmas
    match match those of the amrgraph
    '''
    # list comprehension. checks every node in the amrgraph to identify those that has the amr_relation. obtains 
    # a set of token_num-lemma pairs for the node (the parent) with the amr_relation. 
    amr_lemmaset = [(i, amrgraph[i][0]["lemma"]) for i in amrgraph for i2 in amrgraph[i][1] if i2[0] == amr_relation]
    # The set of pairs are checked for in the (corresponding) UD GREW is searched for the 
    ud_lemmaset = [pair for pair in amr_lemmaset for i in udgraph if pair[1]==udgraph[i][0]["lemma"]]
    
    return ud_lemmaset

def get_childrencount(graph):   
    '''
    takes a UD GREW graph. iterates through all its tokens and for each, counts the number of dependents it has and 
    writes it as a new attribute within the UD graph. 
    '''
    for token_num in graph:
        graph[token_num][0]["num_child"] = len(graph[token_num][1])

if __name__ == "__main__":
	grew.init()
	ud_graph = grew.graph("./data/dev_data/sentence0002.conll")
	print(group_by_relation([ud_graph], amr_rels))