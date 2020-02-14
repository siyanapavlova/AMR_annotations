import ud_to_amr, amr_graph_to_text, smatcher, parser
import grew
import pprint
import operator
import csv
import os

pp = pprint.PrettyPrinter(indent=4)

def run_pipeline(load_path, save_path, filename, gold_amr): 
	'''Process a UD graph in CoNNL-U format to produce the
	corresponding AMRs and find the maximum similarity score
	between a produced AMR and the gold standard AMR.
	Parameters: load_path - location of the UD CoNNL-U file
				save_path - where to save the AMRs
				filename - beginning of the name under which to save the AMRs
				gold_amr - location of the gold AMR file
	Output: best SMATCH similarity score for the sentence
	'''	
	# load the UD graph 
	ud_graph = ud_to_amr.load_data(load_path)
	
	#print("Grew graph loaded \n")

	# run a simple GRS 
	# grs_filename = './grs/grs_amr_main.grs'
	# grs_filename = './grs/grs_amr_main_interim.grs'
	grs_filename = './grs/grs_amr_main_base.grs'

	#printing out the grew format as text; for testing and analysis purposes
	# new_graphs = ud_to_amr.ud_to_amr(grs_filename, ud_graph, strat="add_conc")
	# print(amr_graph_to_text.amr_grew_to_text(new_graphs[0]))

	# generate the graph(s) from the application of the grs in grs_filename
	print("Currently at " + filename)
	try: 
		new_graphs = ud_to_amr.ud_to_amr(grs_filename, ud_graph, strat="test_new_lex")
	except grew.utils.GrewError as er:
		print(filename)
		print(er)
		return None

	# new_graphs = ud_to_amr.ud_to_amr(grs_filename, ud_graph, strat="test_new_lex")


	score_dict = {}
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
	return score

def calculate_scores(sentence_nums):
	'''Given a list of sentence numbers pointing to CoNLL-u parsed files,
	call the processing pipeline and calculate scores
	Parameters: sentence_nums: a list of numbers pointing to sentence numbers
	Output: 3 lists: precision for each sentence, recall for each sentences,
			and f1 for each sentence
	'''
	scores = []
	for num in sentence_nums:
		result = run_pipeline('./data/amr_bank_data/ud/sentence'+'{:04d}'.format(num)+'.conll',
							'./data/evaluation/',
							'sentence'+'{:04d}{}'.format(num, '{}')+'.txt',
							'./data/amr_bank_data/amrs/amr'+'{:04d}'.format(num)+'.txt')
		if result != None:
			scores.append(('{:04d}'.format(num), result))
		else:
			scores.append(('{:04d}'.format(num), b'Precision: -1.00\nRecall: -1.00\nF-score: -1.00\n'))
	# pp.pprint(scores)
	# scores_split = [scores.split(i) for score in scores for i in [b"Precision: ", b"Recall: ", "F-score: "] ]
	precision = [float(score[1].split(b"Precision: ")[1].split(b"\n")[0]) for score in scores]
	recall = [float(score[1].split(b"Recall: ")[1].split(b"\n")[0]) for score in scores]
	f1 = [float(score[1].split(b"F-score: ")[1].split(b"\n")[0]) for score in scores]

	for score_val in [precision, recall, f1]:
		if score_val:
			score_val = [i for i in score_val if i >=0]
			print("======================")
			print ("Min score:", min(score_val))
			print ("Max score:", max(score_val))
			print ("Avg score:", sum(score_val)/len(score_val))
			print("======================")
			index, value = max(enumerate(score_val), key=operator.itemgetter(1))
			print(index, value)
			print(score_val)
	print(len(precision))
	return precision, recall, f1

def collect_scores(sentence_nums, n, folder):
	'''Calls calculare_scores to find the scores for a set of sentences,
	collects the scores and stores them in a folder
	Parameters: sentence_nums - a list of sentence numbers to be tested
				n - the number of times that the test should be run
				folder - path to the folder where results should be saved
	Output: creates four files in the desired folder: 'precision.csv',
			'recall.csv', 'f1.csv' and 'all_metrics.csv'
	'''
	if not os.path.exists(folder):
		os.makedirs(folder)

	data = {'precision': [], 'recall': [], 'f1': []}
	with open(folder+'/all_metrics.csv', 'a') as csvfile:
		writefile = csv.writer(csvfile, delimiter='\t')
		writefile.writerow(['Measure', 'Min', 'Max', 'Average'])
		for i in range(n):
			precision, recall, f1 = calculate_scores(sentence_nums)
			for score_val in [('precision', precision), ('recall', recall), ('f1',f1)]:
				data[score_val[0]].append(score_val[1])

				score_val_clean = [i for i in score_val[1] if i >=0]
				min_score = min(score_val_clean)
				max_score = max(score_val_clean)
				avg_score = sum(score_val_clean)/len(score_val_clean)
				writefile.writerow([score_val[0], min_score, max_score, avg_score])
			writefile.writerow(['','','',''])
	for file, measure in [(folder+'/precision.csv', 'precision'),
							(folder+'/recall.csv', 'recall'),
							(folder+'/f1.csv', 'f1')]:
		with open(file, 'a') as f:
			data_file = csv.writer(f, delimiter='\t')
			for run in data[measure]:
				data_file.writerow(run)


if __name__=="__main__":
	#initialise Grew
	grew.init()
	print("Grew initiated \n")

	#generate the numbers of the sentences to be processed
	sentence_nums = list(range(1,101))

	#process the sentences and collect scores
	collect_scores(sentence_nums, 1, './results/final_100')
