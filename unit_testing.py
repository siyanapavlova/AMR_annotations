import unittest
from ud_to_amr import ud_to_amr, __test_no_iso__, load_data, __test_amr_is_dag__, __test_only_AMR_tags__
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
			test_graphs.append(ud_to_amr(grs_filename, ud_graph, strat="simple"))
	print(test_graphs)

	def test_is_dag(self):
		'''UD_to_AMR should produce a directed acyclic graph'''
		for amr_graph in self.test_graphs:
			result = __test_amr_is_dag__(amr_graph)
			print(result)
			self.assertEqual(1, result)

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

if __name__== "__main__":
	unittest.main()
