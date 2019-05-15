import pprint

pp = pprint.PrettyPrinter(indent=4)

def _load_conllu(filename):
    pass

def get_text_format(graph, current_node, visited, text_format, tabs):
	"""Takes a graph in GREW format and produces its textual representation

	Parameters: graph - a preprocessed graph in GREW format (needs to have abbreviations
	and a list of incoming relations for each node)
				current_node - the current node for the recursion
				visited - a list of already visited nodes
				text_format - the text format so far
				tabs - the number of tabs to be put at the beginning of each new line

	Output: the visited nodes and text format of the graph so far
	"""
	# pp.pprint(graph)
	if current_node not in visited:
		text_format += '(' + graph[current_node][0]['abbreviation'] +' / ' + graph[current_node][0]['concept'].lower()

		# print(text_format)
		# print(graph[0][current_node][1])
		# print("="*10)
		if graph[current_node][1] == []:
			text_format += ')'
			visited.append(current_node)
		else:
			for child_node in graph[current_node][1]:
				text_format = text_format + '\n' + tabs*'\t' + ':' + child_node[0] + ' '
				visited, text_format = get_text_format(graph, child_node[1], visited, text_format, tabs + 1)
			text_format += ')'
			visited.append(current_node)
	else:
		text_format += '(' + graph[current_node][0]['abbreviation'] + ')'
	return visited, text_format


    

def amr_grew_to_text(graph):
	"""Takes a graph in GREW format and produces its textual representation
	The graph is prepossed so that an abbreviation and a list of incoming
	relations is added to each node. The recursive get_text_format function
	is then called

	Parameters: graph - a graph in GREW format

	Output: the graph in text format
	"""

	#For each node add a list of incoming relations by reversing the outgoing ones

	abbreviations = []

	#Create abbreviations for each node
	for node in graph:
		abbr = graph[node][0]['concept'][0].lower()
		#if first letter is not in the abbreviations, the first letter becomes the abbreviation
		if abbr not in abbreviations:
			graph[node][0]['abbreviation'] = abbr
			abbreviations.append(abbr)
		else:
			previous = [x for x in abbreviations if x.startswith(abbr)]
			graph[node][0]['abbreviation'] = abbr + str(len(previous)+1)
			abbreviations.append(abbr)

	
	# for node in graph[0]:
	# 	abbr = (graph[0][node][0]['concept'][0].lower(),node)
	# 	print(abbr)
	# 	# print(node)
	# 	#if first letter is not in the abbreviations, the first letter becomes the abbreviation
	# 	if abbr not in abbreviations:
	# 		graph[0][node][0]['abbreviation'] = abbr[0]
	# 		abbreviations.append(abbr)
	# 	else:
	# 		previous = [x for x in abbreviations if x.startswith(abbr[0])]
	# 		graph[0][node][0]['abbreviation'] = abbr[0] + str(len(previous)+1)
	# 		abbreviations.append(abbr)
	

	#Make a list in each node where the incoming relations will be kept
	for node in graph:
		graph[node].append([])

	#Fill the incoming relations list
	for node in graph:
		for relation in graph[node][1]:
			graph[relation[1]][2] = [relation[0],node]

	#Find the starting node (root)
	for node in graph:
		if graph[node][2] == []:
			starting_node = node
			break

	#Get the text format of the preprocessed graph with a starting node
	visited, text_format = get_text_format(graph, starting_node, [], '', 1)
	return text_format

def conllu_for_smatcher(graphs):
	"""Takes a list of AMR graphs in GREW format
	and saves them all into a file which follows the
	format accepted by SMATCH

	Parameters: graphs - a list of AMR graphs in GREW format

	Output: True/False? Or the location of the file?
	"""

	# Would need graph ID for each graph as well
	for graph in graphs:
		text_format = amr_grew_to_text(graph)

if __name__== "__main__":
	new_graph = {'2': [{'xpos': 'VBD', 'upos': 'VERB', 'lemma': 'see', 'form': 'saw', 'concept': 'see-01', 'Mood': 'Ind', 'VerbForm': 'Fin', 'Tense': 'Past'}, [['lex.doer', '1'], ['lex.patient', '5']]], '5': [{'xpos': 'NN', 'upos': 'NOUN', '_MISC_SpaceAfter': 'No', 'lemma': 'picture', 'form': 'picture', 'concept': 'picture', 'Number': 'Sing'}, [['ARG0-of', '4']]], '4': [{'concept': 'magnificent', 'lemma': 'magnificent', 'form': 'magnificent', 'Degree': 'Pos', 'xpos': 'JJ', 'upos': 'ADJ'}, []], '1': [{'xpos': 'PRP', 'Person': '1', 'lemma': 'I', 'form': 'I', 'PronType': 'Prs', 'Case': 'Nom', 'Number': 'Sing', 'upos': 'PRON', 'concept': 'I'}, []]}
	print(amr_grew_to_text(new_graph))
