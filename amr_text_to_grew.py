import pprint
import grew

def load_file(file):
	with open(file) as f:
		text = [i for i in f.readlines()]
	return text

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
	'''
	1. flattens the text 
		Case 1: no children: closing brackets on 1 line  - no children and no splitter 
			add a lemma attribute as well as a concept attribute 
			return the text, as the 
			use try accept to add nodes 

		Case 2: has children, closing missing and : appearing before 
	2. 
	3. no need to restore token order because we are extracting the subgraph(s) from the node of interest

	input: dictionary is an empty global dictionary 


	'''
	lines = load_file('./data/amr_bank_data/amrs/amr0002.txt')
	lines = [i.strip('\n') for i in lines if i !='\n'] # remove the newlines-only lines 
	lines = [line.lstrip(re.match(r"^[\s]+", line).group()) if re.match(r"^[\s]+", line) != None else line for line in lines ]
	# strip preceding whitespaces 
	
	graph = dict()

	bracket_counter = 0
	while bracket_counter > -1:  
		line = lines.pop(0) # pop the first line 
		bracket_counter += len(re.findall("\(",line)) # check and track the number of starting brackets
		
		# process the line 
		# the first line will always be the root. there will always be the concept node and its variable


		# 1. find roles: 
		roles = re.findall(":[a-zA-Z]+", line)
		# 2. find variables:
		variables = re.findall("\([a-z][1-9]* /", line)
		# 3. find concepts: 
		concepts = []
		while len(roles) >0 or len(variables) >0:
			if len(roles) > 0: _role = roles.pop(0)
			if len(variables) > 0: _variable = variables.pop(0)
				# splits with a string results in a list 
				line = [i for i in line.split(_role) if i !='']
				line = [i for i in line.split(_variable) if i !='']
				_concept = re.match(r'\s*[a-z]+\-*[0-9]*', line")
				line = line.split(_concept)[1]

				# to do: check that concept not already in the dict
				# if not, then add concept to the dict
		 		graph[str(len(graph)+1)] = [{"concept": _concept, 
				 							"variable": _variable},
											 [(_role:)]]
		bracket_counter -= len(re.findall("\)",line)) 


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