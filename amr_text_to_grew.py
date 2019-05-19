import pprint

def load_file(file):
	with open(file) as f:
		text = f.readlines()
	return ''.join(text)

pp = pprint.PrettyPrinter(indent=4)


'''
(s / see-01
      :ARG0 (i / i)
      :ARG1 (p / picture
            :mod (m / magnificent)
            :location (b2 / book :wiki -
                  :name (n / name :op1 "True" :op2 "Stories" :op3 "from" :op4 "Nature")
                  :topic (f / forest
                        :mod (p2 / primeval))))
      :mod (o / once)
      :time (a / age-01
            :ARG1 i
            :ARG2 (t / temporal-quantity :quant 6
                  :unit (y / year))))
'''

'''
[s / see-01
      :ARG0 [i / i]
      :ARG1 [p / picture
            :mod [m / magnificent]
            :location [b2 / book :wiki -
                  :name [n / name :op1 "True" :op2 "Stories" :op3 "from" :op4 "Nature"]
                  :topic [f / forest
                        :mod [p2 / primeval]]]]
      :mod [o / once]
      :time [a / age-01
            :ARG1 i
            :ARG2 [t / temporal-quantity :quant 6
                  :unit [y / year]]]]
'''

'''
[s / see-01 :ARG0 [i / i]  :ARG1 [p / picture :mod [m / magnificent]  :location [b2 / book :wiki - :name [n / name :op1 "True" :op2 "Stories" :op3 "from" :op4 "Nature"]  :topic [f / forest :mod [p2 / primeval] ] ] ]  :mod [o / once]  :time [a / age-01 :ARG1 i :ARG2 [t / temporal-quantity :quant 6 :unit [y / year] ] ] ] 

'''


def built_dict(text, dictionary):
	print(text)
	if '(' not in text and '/' not in text and ':' not in text:
		return [], text, {} #text here is the node ID
	if '(' in text and '/' in text and ':' not in text:
		# if the text is of the shape "(o / once)", we return an empty list, the id of the node ("o")
		# and the dictionary for that node ( {'lemma': 'once', rels: []} )
		dictionary[text.split('/')[0].strip()] = {'lemma': text.split('/')[1].strip(), 'rels':[]}
		return text.split('/')[0].strip(), dictionary
		# return [], text.split('/')[0].strip(), {'lemma': text.split('/')[1].strip(), 'rels':[]}
	node_id = text.split('/')[0]
	lemma = text.split('/')[1].strip().split('')

	print('='*15)

def build_adj_matrix(graph, start, step, size):
	'''Given a UD graph, a starting node, a step size and a matrix size,
	return an adjacency matrix for that graph, but only starting from the start node
	and spanning step number of steps
	Parameters: graph - a graph in UD format
				start - string? starting node in the graph
				step - integer, the number of steps to span from that node
				size - integer, the height and width of the required matrix
	Outputs: an adjacency matrix
	'''
	pass

if __name__ == "__main__":
	# text = load_file('./data/amr_bank_data/amrs/amr0005.txt')
	text = load_file('./data/amr_bank_data/amrs/amr0002.txt')
	print(text)
	print(' '.join(text.split()))
	# built_dict(text)

'''
[   {   '1': [   {   'Case': 'Nom',
                     'Number': 'Sing',
                     'Person': '1',
                     'PronType': 'Prs',
                     'concept': 'I',
                     'form': 'I',
                     'lemma': 'I',
                     'upos': 'PRON',
                     'xpos': 'PRP'},
                 []],
        '2': [   {   'Mood': 'Ind',
                     'Tense': 'Past',
                     'VerbForm': 'Fin',
                     'concept': 'see-01',
                     'form': 'saw',
                     'lemma': 'see',
                     'upos': 'VERB',
                     'xpos': 'VBD'},
                 [['lex.doer', '1'], ['lex.patient', '5']]],
        '4': [   {   'Degree': 'Pos',
                     'concept': 'magnificent',
                     'form': 'magnificent',
                     'lemma': 'magnificent',
                     'upos': 'ADJ',
                     'xpos': 'JJ'},
                 []],
        '5': [   {   'Number': 'Sing',
                     '_MISC_SpaceAfter': 'No',
                     'concept': 'picture',
                     'form': 'picture',
                     'lemma': 'picture',
                     'upos': 'NOUN',
                     'xpos': 'NN'},
                 [['ARG0-of', '4']]]}]
'''