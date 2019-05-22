import grew
import pprint, ud_to_amr, glob
import numpy as np
from itertools import combinations 
import networkx as nx
from sklearn.cluster import SpectralClustering, AgglomerativeClustering
from sklearn.metrics import silhouette_score, calinski_harabaz_score, davies_bouldin_score

pp = pprint.PrettyPrinter(indent = 4)

########## Environment Variables ########## 
AMR_RELS = ['ARG0', 'ARG1', 'ARG2', 'ARG3', 'ARG4', 'ARG5', 'ARG6', 'ARG7', 'ARG8', 'ARG9',
			'accompanier', 'age', 'beneficiary', 'concession', 'condition', 'consist-of',
			'degree', 'destination', 'direction', 'domain', 'duration', 'example', 'extent',
			'frequency', 'instrument', 'li', 'location', 'manner', 'medium', 'mod', 'mode',
			'name', 'ord', 'part', 'path', 'polarity', 'polite', 'poss', 'purpose', 'quant',
			'range', 'scale', 'source', 'subevent', 'time', 'topic', 'unit', 'value', 'wiki',
			':calendar', ':century', ':day', ':dayperiod', ':decade', ':era', ':month',
			':quarter', ':season', ':timezone', ':weekday', ':year', ':year2',
			'op1', 'op2', 'op3', 'op4']

UD_POS = ["ADJ",	"ADP", "ADV", "AUX", "INTJ", "CCONJ", "NOUN", "DET", "PROPN", "NUM", "VERB", "PART", "PRON", 
"SCONJ","PUNCT", "SYM", "X"]
UD_DEPRELS = ["nsubj", "obj", "iobj", "csubj", "ccomp", "xcomp", "obl", "vocative", "expl", "dislocated", "advcl", 
"advmod", "discourse", "aux", "cop", "mark", "nmod", "appos", "nummod", "acl", "amod", "det", "clf",
"case", "conj", "cc", "fixed", "flat", "compound", "list", "parataxis", "orphan", "goeswith", "reparandum", 
"punct", "root", "dep"]


#TODO: think about how best to implement filtering. deleting these at get_nxsubgraphs_largeststep or 
# later could cause disconnected nodes in the SG
UD_FILTER_POS = ["PUNCT", "X" ] # remove tokens that are punctuation or the undefined X, which don't help in 
								# discriminating between sentences 
UD_FILTER_DEPREL = ["punct", "dep"] # remove child tokens with relations that are punctuation or the undefined dep, 
									# which don't help in discriminating between sentences  

class Sentence:
	def __init__(self, sentence_num):
		self.sentence_num = sentence_num 	# this is the Little Prince sentence ID
		self.amr_grewgraph = None			# this is the gold AMR for the sentence (in GREW)
		self.ud_grewgraph = None			# this is our UD parse of the sentence (in GREW)
		self.ud_nxgraph = None 				# this is the complete nxgraph of the UD parse


########## Preparatory functions - at global sentence level ##########

def loadmake_allgraphs(ud_filepath="./data/amr_bank_data/ud/", 
						amr_filepath="./data/amr_bank_data/amrs_gold/"):
	'''
	Given the filepaths where CONLL-U files for sentences are stored, return a dictionary of all
	the sentences (e.g. of a corpus) containing GREW and Networkx objects. 
	UD and AMR relate to different annotations or representations of the same sentence. 
	'''
	allsentences_graphs = dict()
	goldamrfilenames = glob.glob(amr_filepath)
	sentence_nums = [file.split("\\")[-1].lstrip("sentence").rstrip(".conll") for file in goldamrfilenames]
	allsentences_graphs = {sentence_num: Sentence(sentence_num) for sentence_num in sentence_nums}
	for sentence_num in sentence_nums:
		allsentences_graphs[sentence_num].amr_grewgraph = grew.graph(amr_filepath)	# load amr, add it to dict
		allsentences_graphs[sentence_num].ud_grewgraph = grew.graph(ud_filepath) 	# load ud, add it to dict
		allsentences_graphs[sentence_num].ud_nxgraph = _make_nxgraph(allsentences_graphs[sentence_num]["ud_grewgraph"])
		# create nxgraph, add it to dict
	
	return allsentences_graphs

def _sentences_by_amr_relations(amr_grewgraphs, amr_relations):
	'''
	Give a list of GREW graphs and a list of amr_relations, for each amr relation
	return the list of the indices of the graphs containing that amr relation
	Inputs:
	amr_grewgraphs - a list of GREW AMR graphs
	amr_relations  - a list of AMR relations
	Output: a dictionary where the keys are the relations and the values are
			lists of graphs containing the corresponding relation
	'''
	sentences_by_amrrelations = {key: [] for key in amr_relations}
	#For each graph
	for ind, g in enumerate(amr_grewgraphs):
		#Make a set of all the relations contained in that graph
		graph_rels = set()
		for node in g:
			for rel in g[node][1]:
				graph_rels.add(rel[0])
		#For each of the relations contained in the graph,
		#append the graph index to the list of graphs associated with that relation
		for rel in graph_rels:
			if rel in sentences_by_amrrelations:
				sentences_by_amrrelations[rel].append(ind)

	return sentences_by_amrrelations


########## Preparatory functions - at AMR relation level ##########

def _make_ud_nxgraph(ud_grewgraph):
	'''
	takes a UD graph in GREW format. extracts node, node attribute, edge, edge attribute relation. 
	used in loadmake_allgraphs
	'''
	ud_nxgraph = nx.DiGraph() # directed graph 
	for node_num in ud_grewgraph:
		try:
			ud_nxgraph.add_node(node_num, upos = ud_grewgraph[node_num][0]['upos']) # add "upos" attribute as node attribute
		except: 
			ud_nxgraph.add_node(node_num, weight = "root") # for root node
		if len(ud_grewgraph[node_num][1]) >= 1: # only add edges for nodes that have children 
			for edge in ud_grewgraph[node_num][1]: 
				ud_nxgraph.add_edge(node_num, edge[1], UDrel=edge[0]) # add "UDrel" attribute as edge attribute

	return ud_nxgraph

def _map_lemma_udgrew_amrgrew(ud_grewgraph, amr_grewgraph, amr_relation):
	'''
	given a ud_grewgraph and its associated amr_grewgraph, searches for all nodes in the amr_grewgraph 
	that has the amr_relation that is passed into the function. This list of token_num-lemma pairs 
	is searched for in the ud_grewgraph. The resulting token_num-lemma pairs are for nodes in the ud_grewgraph 
	graph where both token_num and lemmas match those of the amr_grewgraph. 
	'''
	# list comprehension. checks every node in the amr_grewgraph to identify those that has the relation. obtains 
	# a set of token_num-lemma pairs for the node (the parent) with the relation. 
	amr_lemmalist = [amr_grewgraph[node][0]["lemma"] for node in amr_grewgraph for i2 in amr_grewgraph[node][1] if i2[0] == amr_relation]

	# some AMR relations may have more than 1 instance in the sentence. for these: 2 cases will be present: 
		# a. each lemma is different
		# b. same lemmas may be present 
	
	# we care about 1-to-1 matching of the lemmas, so let's remove duplicate lemmas in the set
	amr_lemmalist = set(amr_lemmalist)

	# we track 2 lists, the first is the set of tokens in the UD graph that have a 1-to-1 correspondence with the AMR graph 
	# the other is the set of lemmas in the AMR graph where we cannot find the 1-to-1 correspondence. 
	ud_grewgraph.pop("ROOT") # remove the 'ROOT' node here, since it won't have a lemma attribute
	ud_present_tokenlist = [node_num for lemma in amr_lemmalist for node_num in ud_grewgraph if lemma == ud_grewgraph[node_num][0]["lemma"]]
	ud_notpresent_lemmalist = [lemma for lemma in amr_lemmalist for node_num in ud_grewgraph if lemma != ud_grewgraph[node_num][0]["lemma"]]
    
	return amr_lemmalist, ud_present_tokenlist, ud_notpresent_lemmalist 

def _get_nxsubgraphs_largeststepsize(allsentences_graphs, sentences_by_amr_relations, amr_relation, stepsizerange):
	'''
	takes the entire set of Sentence objects for the corpus, for a single amr relation, get the subgraphs that correspond
	to this amr_relation. each subgraph returned is the one for the largest stepsize 
	'''
	sentence_nums = sentences_by_amr_relations[amr_relation]
	nxsubgraphs = [] 	#init an empty list to store the SGs

	largest_stepsize = max(stepsizerange)

	for sentence_num in sentence_nums: #iterate through the keys of the nx_graphs
		sent_nxgraph = allsentences_graphs[sentence_num].ud_nxgraph # saving it to the ud_nxgraph attribute of the Sentence() obj
		ud_present_tokenlist = map_lemma_udgrew_amrgrew(allsentences_graphs[sentence_num].amr_grewgraph],
											 allsentences_graphs[sentence_num].ud_grewgraph, amr_relation)[0]
		for token_num in ud_present_tokenlist: 
			subgraph_nodes = []
			__children_nodes = sent_nxgraph.successors(token_num) #get its children
			subgraph_nodes.extend(__children_nodes)
			while largest_stepsize > 0:
				__ = [sent_nxgraph.successors(node) for node in __children_nodes]
				__children_nodes = [item for item in sublist for sublist in __] # flatten the list and update __children_nodes
				subgraph_nodes.extend(__children_nodes)
				largest_stepsize -= 1 # decrement the counter

			subgraph_nodes.append(token_num) # include the "root" parent

			# get the subgraph with the final subgraph_nodes, and add to nxsubgraphs
			nxsubgraphs.append(sent_nxgraph.subgraph(subgraph_nodes)) 
    
	return nxsubgraphs


def _trim_nxsubgraph_leaves(nxsubgraphs):
	'''
	takes an iterable of nxsubgraphs, and for each nxsubgraph, do the following:
	1. find all nodes that have out degree of less than 1 (i.e. 0). These are the leaf nodes
	2. remove these leaf nodes 
	'''
	trimmed_nxsubgraphs = []
	for nxsubgraph in nxsubgraphs:
		leaf_nodes = [nodedata[0] for nodedata in subgraph.out_degree if nodedata[1]<1]
		__trimmedgraph = nxsubgraph.remove_nodes_from(leaf_nodes)	
		trimmed_nxsubgraphs.append(__trimmedgraph)

	return trimmed_nxsubgraphs

########## Preparatory functions - at AMR relation, subgraph level ##########

def _compute_affinity(nxsubgraphs_list, node_match, edge_match):
	'''
	given a list of subgraphs generated with the same stepsize, return an affinity matrix computed with 
	nx's graph edit distance, pairwise between each node.  
	'''
    
	# create a zeros np matrix for storing the GED scores 
	affinity_matrix = np.zeros(len[nxsubgraphs_list], len(nxsubgraphs_list))
    
	# generate unordered pairwise combi between subgraphs 
	index_pairs = [i for i in combinations(range(len(nxsubgraphs_list)),2)]
	for index_pair in index_pairs:
		ged = nx.graph_edit_distance(nxsubgraphs_list[index_pair[0]], nxsubgraphs_list[index_pair[1]],
									node_match=node_match, edge_match=edge_match) # compute the ged
		affinity_matrix[index_pair[0]][index_pair[1]] = ged # add the score to the affinity matrix

	return affinity_matrix


########## Clustering functions - at AMR relation, subgraph stepsize level ##########

def iterate_stepsizes(nxsubgraphs, stepsizerange, n_range, _fit_cluster, cluster_algo="spectral", 
						using_affinmatrix = False, affinity="cosine", agglo_link="complete"):
	'''
	given different sets of X (each set of X being a collection of subgraphs of a certain step size), iterate through sets,
	as well as for each step size through n_range different cluster size. returns a collection of labels and evaluation 
	scores for each X_set-n_cluster. 
	inputs | X_sets is a collection of sets. Each set is a collection of flattened matrices obtained from get_graphcuts
	'''
	model_scores = dict()
	for iteration in range(stepsizerange[1]-stepsizerange[0]):
		if iteration == 0: 
			X = _compute_affinity()
		else: 
			nxsubgraphs = _trim_nxsubgraph_leaves(nxsubgraphs)
			X = _compute_affinity(nxsubgraphs)

		model_scores[str(stepsize)+"steps"] = _iterate_ncluster(X, n_range, 
		_fit_cluster, cluster_algo=cluster_algo, affinity=affinity, agglo_link=agglo_link)
	return model_scores


def _iterate_ncluster(X, n_range, _fit_cluster, cluster_algo="spectral", 
						affinity="cosine", agglo_link="complete"): 
	'''
	
	'''
	model_scores = dict()
	for n_clusters in n_range:
		model_scores[str(n_clusters+1)+"clusters"] = _fit_cluster(X, n_clusters=n_clusters, cluster_algo=cluster_algo, 
						affinity=affinity, agglo_link=agglo_link)
    
	return model_scores

def _fit_cluster(X, n_clusters, cluster_algo="spectral", affinity="cosine", agglo_link="complete"):
	'''
	
	'''
	if cluster_algo=="spectral":
		spec_clust = SpectralClustering(n_clusters = n_clusters, assign_labels="discretize", 
							n_neighbors =int(len(X)/n_clusters)/2 , n_init=100,
							affinity=affinity, n_jobs=-1)
    
		# run fit to partition the graph into clusters 
		spec_clust.fit(X)
		# extract cluster labels 
		labels = spec_clust.labels_
		# extract the computed affinity matrix to pass into scorers
		affinity_matrix = spec_clust.affinity_matrix_

		sil_score = silhouette_score(X, labels, metric="precomputed")
		ch_score = calinski_harabaz_score(X, labels)
		db_score =  davies_bouldin_score(X, labels)
        
	elif cluster_algo=="agglomerative": 
		agglo_clust = AgglomerativeClustering(n_clusters = n_clusters,
								affinity=affinity, linkage="complete")
    
		# run fit to partition the graph into clusters 
		agglo_clust.fit(X)
		# extract cluster labels 
		labels = agglo_clust.labels_
        
		sil_score = silhouette_score(X, labels, metric="cosine")
		ch_score = calinski_harabaz_score(X, labels)
		db_score =  davies_bouldin_score(X, labels)
    
	return {"labels": labels, "silhouette":sil_score, "calinski_harabaz":ch_score, "davies_bouldin":db_score}



def get_best_stepnclust(model_scores, eval_metric="silhouette"):
	'''
	'''
	if eval_metric == "silhouette" or "calinski_harabaz": # higher scores better 
		# for each stepsize, retain only the results for the cluster size setting with the 
        
		step, cluster, score, labels = 0, 0, float("-inf"), 0 # negative infinity to handle negative silhouette scores
		for step_size in model_scores:
			for cluster_size in model_scores[step_size]: 
				if model_scores[step_size][cluster_size][eval_metric] >= score:
					score=model_scores[step_size][cluster_size][eval_metric]
					cluster=cluster_size
					step=step_size
					labels = model_scores[step_size][cluster_size]["labels"]
    
	elif eval_metric == "davies_bouldin": # db_scores closer to zero better
		step, cluster, score, labels = 0, 0, float("inf"), 0
		for step_size in model_scores:
			for cluster_size in model_scores[step_size]: 
				if model_scores[step_size][cluster_size][eval_metric] < score:
					score=model_scores[step_size][cluster_size][eval_metric]
					cluster=cluster_size
					step=step_size
					labels = model_scores[step_size][cluster_size]["labels"]
                    
	return step, cluster, score, labels


########## Result extraction functions ##########

def get_graphcuts(nxgraph, rootnode_num, stepsize):
	'''
	for a given nxgraph, selected stepsize and the root node number as well as specified step size, return the subgraph
	'''
	pass


def _find_max_subgraph():
	'''
	given each subset of graphcuts of a certain size (corresponding to instances from one cluster), find the maximal 
	subgraph shared between all of them. This will be the relation pattern for 1x rewriting rule for the AMR relation. 
	A linguistic analysis of this pattern (to remove potentially unnecessary UD relations - e.g. determiners etc)
	'''
	pass

if __name__ == "__main__":
	grew.init()
	sentence_nums = range(1,5) 
	# load the GRS 
	grs_filename = './grs/grs_amr_main.grs' 
	__amr_grewgraphs = [grew.graph("./data/amr_bank_data/ud/sentence{:04d}.conll".format(i)) for i in sentence_nums]
	# generate the graph(s) from the application of the grs in grs_filename
	amr_grewgraphs = [ud_to_amr.ud_to_amr(grs_filename, ud_graph, strat="test_new_lex")[0] for ud_graph in __amr_grewgraphs] 

	ud_grewgraphs = [grew.graph("./data/amr_bank_data/ud/sentence{:04d}.conll".format(i)) for i in sentence_nums]

	print ("UD Graph:",  ud_grewgraphs[0])
	print ("AMR Graph:",  amr_grewgraphs[0], "\n")


	print("test _make_ud_nxgraph", [i for i in _make_ud_nxgraph(ud_grewgraphs[0]).adjacency()])

	print('test _map_lemma_udgrew_amrgrew', _map_lemma_udgrew_amrgrew(ud_grewgraphs[0], amr_grewgraphs[0], "nummod"))

	print('test _sentences_by_amr_relations', _sentences_by_amr_relations(amr_grewgraphs, ["nsubj", "obl"]))

	allsentences_graphs = {}
	for sentence_num in sentence_nums: 
		__ = Sentence(sentence_num)
		__.
		allsentences_graphs[sentence_num] = __