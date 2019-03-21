import ud_to_amr, amr_graph_to_text, smatcher
import grew
from random import seed, sample
import pprint

pp = pprint.PrettyPrinter(indent=4)

def run_pipeline(load_path, save_path): 
	print(load_path)
	# load the UD graph 
	ud_graph = ud_to_amr.load_data(load_path)
	pp.pprint(ud_graph)
	print("Grew graph loaded \n")
	# print(ud_graph)

	# run a simple GRS 
	grs_filename = './grs/grs_amr_main.grs' 

	# generate the graph(s) from the application of the grs in grs_filename
	new_graphs = ud_to_amr.ud_to_amr(grs_filename, ud_graph, strat="simple")
	# print(new_graphs[0])
	# print(len(new_graphs))
	# ud_to_amr.save_data(new_graphs[0],save_path)
	pp.pprint(new_graphs[0])
	print(amr_graph_to_text.amr_grew_to_text(new_graphs))

if __name__=="__main__":
	# sentence_nums = choose_sentences_from_lp(20, 1, 1562)
	grew.init()
	print("Grew initiated \n")

	seed(1)
	# sentence_nums = sample(range(1,1562,1),20)
	sentence_nums = [276]
	sentence_nums = [4,5,6]
	print(sentence_nums)
	for num in sentence_nums:
		run_pipeline('./data/amr_bank_data/ud/sentence'+"{:04d}".format(num)+'.conll', './data/evaluation/sentence'+"{:04d}".format(num)+'.conll')