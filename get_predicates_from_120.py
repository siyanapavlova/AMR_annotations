import grew
from create_lexicon import sort_file
import pprint

pp = pprint.PrettyPrinter(indent=4)

def construct_predicate_list(graph_file, predicates):
	to_write = []
	graph = grew.graph(graph_file)
	for node in graph:
		for predicate in predicates:
			if len(graph[node]) and graph[node][0].get('lemma') and graph[node][0]['lemma'] == predicate[0]:
				to_write.append(predicate[1])
	return to_write

if __name__ == "__main__":
	grew.init()
	print("Grew initiated \n")

	with open('./grs/lexicons/original_amr_lexicons/propbank-amr-frames-arg-descr.txt') as f:
		predicate_lines = f.readlines()

	predicates = [(line.split('-0')[0].split('-1')[0].strip() ,line) for line in predicate_lines]

	sentence_nums = list(range(1,120))

	to_write = []

	for num in sentence_nums:
		to_write += construct_predicate_list('./data/amr_bank_data/ud/sentence'+'{:04d}'.format(num)+'.conll', predicates)

	to_write = set(to_write)

	with open('./grs/lexicons/original_amr_lexicons/pred_for_120.txt', 'w') as file:
		for line in to_write:
			file.write(line)

	sort_file('./grs/lexicons/original_amr_lexicons/pred_for_120.txt')

	