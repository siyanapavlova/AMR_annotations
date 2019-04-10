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

if __name__ == "__main__":
	grew.init()
	ud_graph = grew.graph("./data/dev_data/sentence0002.conll")
	print(group_by_relation([ud_graph], amr_rels))