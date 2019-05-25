import ud_to_amr, amr_graph_to_text, smatcher, parser
import grew
from random import seed, sample
import pprint
import operator

pp = pprint.PrettyPrinter(indent=4)

def run_pipeline(load_path, save_path, filename, gold_amr): 	
	# load the UD graph 
	ud_graph = ud_to_amr.load_data(load_path)
	
	#print("Grew graph loaded \n")

	# run a simple GRS 
	grs_filename = './grs/grs_amr_main.grs' 

	# generate the graph(s) from the application of the grs in grs_filename
	try: 
		new_graphs = ud_to_amr.ud_to_amr(grs_filename, ud_graph, strat="test_new_lex")
	except grew.utils.GrewError:
		return None
	score_dict = {}
	# print(len(new_graphs))
	for new_graph_num in range(len(new_graphs)):
		new_graph = new_graphs[new_graph_num]
		text_amr = amr_graph_to_text.amr_grew_to_text(new_graph)
		# pp.pprint(new_graph)
		# print(text_amr)
		parser.save_data(text_amr, save_path, filename.format("_"+str(new_graph_num)))  # add a numerical extension  to 
																			# to distinguish between alternative results
		_score = smatcher.get_smatch_score(save_path+filename.format("_"+str(new_graph_num)), gold_amr) #gold goes second
		score_dict[filename.format("_"+str(new_graph_num))] = float(_score[-5:-1])

	# get max scoring rewrite result 
	best_rewrite = max(score_dict.items(), key=(lambda key: score_dict[key[0]]))
	best_textgraph = best_rewrite[0]
	score = smatcher.get_smatch_score(save_path+best_textgraph, gold_amr) 
	# print("="*10)
	# print(score)
	# print(save_path+filename, gold_amr)
	return score


if __name__=="__main__":
	# sentence_nums = choose_sentences_from_lp(20, 1, 1562)
	grew.init()
	print("Grew initiated \n")

	seed(1)
	# sentence_nums = sorted(sample(range(1,1562,1),20))
	# sentence_nums = [59, 276, 430, 523, 778, 799, 887, 1166, 1245, 1426]
	# sentence_nums = [347]

	# sentence_nums = list(range(1,121))
	# sentence_nums = list(range(1,15))
	# sentence_nums = [59]
	sentence_nums = [17]

	# sentence_nums = list(range(1,1563))
	# sentence_nums.remove(347)
	# sentence_nums.remove(406)
	# sentence_nums.remove(662)
	# sentence_nums.remove(697)
	# sentence_nums.remove(818)
	# sentence_nums.remove(1272)
	# sentence_nums.remove(1344)
	scores = []
	print(sentence_nums)

	for num in sentence_nums:
		result = run_pipeline('./data/amr_bank_data/ud/sentence'+'{:04d}'.format(num)+'.conll',
							'./data/evaluation/',
							'sentence'+'{:04d}{}'.format(num, '{}')+'.txt',
							'./data/amr_bank_data/amrs/amr'+'{:04d}'.format(num)+'.txt')
		if result != None:
			scores.append(('{:04d}'.format(num), result))
	# pp.pprint(scores)
	# scores_split = [scores.split(i) for score in scores for i in [b"Precision: ", b"Recall: ", "F-score: "] ]
	precision = [float(score[1].split(b"Precision: ")[1].split(b"\n")[0]) for score in scores]
	recall = [float(score[1].split(b"Recall: ")[1].split(b"\n")[0]) for score in scores]
	f1 = [float(score[1].split(b"F-score: ")[1].split(b"\n")[0]) for score in scores]
	for score_val in [precision, recall, f1]:
		if score_val:
			print("======================")
			print ("Min score:", min(score_val))
			print ("Max score:", max(score_val))
			print ("Avg score:", sum(score_val)/len(score_val))
			print("======================")
			index, value = max(enumerate(score_val), key=operator.itemgetter(1))
			print(index, value)
			print(score_val)
	print(len(precision))