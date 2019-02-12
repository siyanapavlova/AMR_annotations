import unittest

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

	def is_directed_graph(self):
		'''UD_to_AMR should produce a directed graph'''
		pass

	def is_acyclic_graph(self):
		'''UD_to_AMR should produce an acyclic graph'''
		pass

	def has_only_AMR_tags(self):
		'''UD_to_AMR should produce a graph which has only AMR tags'''
		pass

	def every_edge_has_label(self):
		'''UD_to_AMR should produce a graph in which every edge has a label'''
		pass


if __name__== "__main__":
	pass