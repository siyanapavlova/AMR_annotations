import ud_to_amr, amr_graph_to_text, smatcher, parser
import grew
from random import seed, sample
import pprint

pp = pprint.PrettyPrinter(indent=4)

def run_pipeline(load_path, save_path, filename, gold_amr): 	
	# load the UD graph 
	ud_graph = ud_to_amr.load_data(load_path)
	
	#print("Grew graph loaded \n")

	# run a simple GRS 
	grs_filename = './grs/grs_amr_main.grs' 

	# generate the graph(s) from the application of the grs in grs_filename
	new_graphs = ud_to_amr.ud_to_amr(grs_filename, ud_graph, strat="simple")
	text_amr = amr_graph_to_text.amr_grew_to_text(new_graphs)
	parser.save_data(text_amr, save_path, filename)

	print(text_amr)
	print("="*10)

	score = smatcher.get_smatch_score(save_path+filename, gold_amr) #gold goes second - we are not sure why though
	# print(save_path+filename, gold_amr)
	return score


if __name__=="__main__":
	# sentence_nums = choose_sentences_from_lp(20, 1, 1562)
	grew.init()
	print("Grew initiated \n")

	seed(1)
	sentence_nums = sorted(sample(range(1,1562,1),20))
	# sentence_nums = [59, 276, 430, 523, 778, 799, 887, 1166, 1245, 1426]
	# sentence_nums = [4]
	# sentence_nums = [130]
	scores = []
	print(sentence_nums)
	for num in sentence_nums:
		scores.append(('{:04d}'.format(num), run_pipeline('./data/amr_bank_data/ud/sentence'+'{:04d}'.format(num)+'.conll',
							'./data/evaluation/',
							'sentence'+'{:04d}'.format(num)+'.txt',
							'./data/amr_bank_data/amrs/amr'+'{:04d}'.format(num)+'.txt')))
	pp.pprint(scores)