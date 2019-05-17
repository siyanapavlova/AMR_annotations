import grew
import pprint, ud_to_amr
import numpy as np
from itertools import combinations 
from random import seed, sample
import networkx as nx
from sklearn.cluster import SpectralClustering, AgglomerativeClustering
from sklearn.metrics import silhouette_score, calinski_harabaz_score, davies_bouldin_score

pp = pprint.PrettyPrinter(indent = 4)

#TODO: add more relations to this list
amr_rels = ['ARG0', 'ARG1', 'ARG2', 'ARG3', 'ARG4', 'ARG5', 'ARG6', 'ARG7', 'ARG8', 'ARG9',
			'accompanier', 'age', 'beneficiary', 'concession', 'condition', 'consist-of',
			'degree', 'destination', 'direction', 'domain', 'duration', 'example', 'extent',
			'frequency', 'instrument', 'li', 'location', 'manner', 'medium', 'mod', 'mode',
			'name', 'ord', 'part', 'path', 'polarity', 'polite', 'poss', 'purpose', 'quant',
			'range', 'scale', 'source', 'subevent', 'time', 'topic', 'unit', 'value', 'wiki',
			':calendar', ':century', ':day', ':dayperiod', ':decade', ':era', ':month',
			':quarter', ':season', ':timezone', ':weekday', ':year', ':year2',
			'op1', 'op2', 'op3', 'op4']

def amr_text_to_grew(amr_text):
	'''
	Given a AMR graph in text, produce the corresponding GREW graph
	Input:
	amr_text - the text representation of the AMR graph
	Output: a GREW graph
	'''
	pass

def group_by_relation(graphs, relations):
	'''
	Give a list of GREW graphs and a list of relations, for each relation
	return a the list of the indeces of the graphs containing that relation
	Inputs:
	sentences - a list of GREW graphs
	relations  - a list of relations
	Output: a dictionary where the keys are the relations and the values are
			lists of graphs containing the corresponding relation
	'''
	graphs_by_relation = {key: [] for key in relations}
	#For each graph
	for ind, g in enumerate(graphs):
		#Make a set of all the relations contained in that graph
		graph_rels = set()
		for node in g:
			for rel in g[node][1]:
				graph_rels.add(rel[0])
		#For each of the relations contained in the graph,
		#append the graph index to the list of graphs associated with that relation
		for rel in graph_rels:
			if rel in graphs_by_relation:
				graphs_by_relation[rel].append(ind)

	return graphs_by_relation

def split_by_relations(sentences, relations1, relations2):
	'''
	Given a list of GREW graph and two lists of relations,
	split the first list into 4 categories:
	1. graphs not containing any of the relations from any of the lists
	2. graphs containing only relations from the first list
	3. graphs containing only relations from the second list
	4. graphs conitaning relations from both lists
	'''
	pass

def map_lemma_amr_ud(amrgraph, udgraph, amr_relation):
	'''
	given an AMR graph and its associated UD graph, searches for all nodes in the AMR GREW graph that has the 
	amr_relation that is passed into the function. This list of token_num-lemma pairs is searched for
	in the UD GREW graph. The resulting token_num-lemma pairs are for nodes in the UD graph whose token_num and lemmas
	match those of the AMR graph. 
	'''
	# list comprehension. checks every node in the amrgraph to identify those that has the amr_relation. obtains 
	# a set of token_num-lemma pairs for the node (the parent) with the amr_relation. 
	amr_lemmaset = [(i, amrgraph[i][0]["lemma"]) for i in amrgraph for i2 in amrgraph[i][1] if i2[0] == amr_relation]
	# The set of pairs are checked for in the (corresponding) UD GREW is searched for the 
	ud_lemmaset = [pair for pair in amr_lemmaset for i in udgraph if pair[1]==udgraph[i][0]["lemma"]]
    
	return ud_lemmaset

def get_nxgraphs(graphs_by_relation):
	'''
	given a list of index numbers for UD Graph files, together with the AMR relation that they are associated with, 
	1. open and load each file using GREW Python
	2. extract node, node attribute, edge, edge attribute relation for all graphs on networkx (nx)
	3. store each nx graph object 
	'''
	nxgraphs_dict=dict()

	for graph_indexnum in graphs_by_relation:
		load_path= "./data/amr_bank_data/ud/sentence{:04d}.conll".format(graph_indexnum)
		ud_grewgraph = ud_to_amr.load_data(load_path) 
		nxgraph = make_nxgraph(ud_grewgraph) # see make_nxgraph below 
		graph_indexnum[graph_indexnum] = nxgraph
	return nxgraphs_dict 

def _make_nxgraph(udgraph):
	'''
	takes a UD graph in GREW format. extracts node, node attribute, edge, edge attribute relation 
	'''
	nxgraph = nx.DiGraph() # directed graph 
	for node_num in udgraph:
		try:
			nxgraph.add_node(node_num, upos = udgraph[node_num][0]['upos']) # add "upos" attribute as node attribute
		except: 
			nxgraph.add_node(node_num, weight = "root") # for root node
		if len(udgraph[node_num][1])>=1: # only add edges for nodes that have children 
			for edge in udgraph[node_num][1]: 
				nxgraph.add_edge(node_num, edge[1], UDrel=edge[0]) # add "UDrel" attribute as edge attribute
    
	return nxgraph

def _get_nxsubgraphs(nxgraphs_dict):
	'''
	given a dictionary of nxgraph objects (keys are sentence numbers, values the nx graph object), for every graph, 
	1. get list of node_num-lemma pair using map_lemma_amr_ud
	2. iterate through that list (either 1 or more pairs) to:
		a. find the children for a particular node_num
		b. find the subgraph containing node_num and children
		c. add to nxsubgraphs_dict
	'''
	nxsubgraphs_dict = dict() # init an empty dictionary to store the SGs
	for nxgraph_key in nxgraphs_dict: # iterate through the keys of the nx_graphs
		ud_lemmaset = map_lemma_amr_ud(nxgraph_key)
		subgraph_nodes = []
		for set_ in ud_lemmaset: 
			subgraph_nodes.extend(nxgraphs_dict[nxgraph_key].successors(set_[0])) # get its children
			subgraph_nodes.append(nxgraph_key) # add the parent to the list too
            
		nxsubgraphs_dict[set_[0]] = nxgraphs_dict[nxgraph_key].subgraph(subgraph_nodes) # get the SG
    
	return nxsubgraphs_dict

def get_nxsubgraphs_bysteps(nxgraphs_dict, stepsizerange):
	'''
	given a set of a dictionary of nxgraph objects and the stepsizerange, for each graph: 
	1. get the largest stepsize subgraph 
	2. subsequently, working on this "largest" stepsize subgraph, get successively smaller step-sized 
	subgraphs by removing leaf nodes at each layer. (this approach saves a little time by not having to search the 
	original graph and building out the different stepsize SGs each time)
	'''
	nxsubgraphs_bysteps_dict = dict()
    
	return nxsubgraphs_bysteps_dict

def compute_affinity(nxsubgraphs_set, node_match, edge_match):
	'''
	given a set of subgraphs generated with the same stepsize, return an affinity matrix computed with 
	nx's graph edit distance, pairwise between each node.  
	'''
    
	# create a zeros np matrix for storing the GED scores 
	affinity_matrix = np.zeros(len[nxsubgraphs_set], len(nxsubgraphs_set))
    
	# generate unordered pairwise combi between subgraphs 
	index_pairs = [i for i in combinations(range(len(nxsubgraphs_set)),2)]
	for index_pair in index_pairs:
		ged = nx.graph_edit_distance(nxsubgraphs_set[index_pair[0]], nxsubgraphs_set[index_pair[1]],
									node_match=node_match, edge_match=edge_match) # compute the ged
		affinity_matrix[index_pair[0]][index_pair[1]] = ged # add the score to the affinity matrix

	return affinity_matrix

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


def iterate_graphcuts(X_sets, n_range, _fit_cluster, cluster_algo="spectral", 
						using_affinmatrix = False, affinity="cosine", agglo_link="complete"):
	'''
	given different sets of X (each set of X being a collection of subgraphs of a certain step size), iterate through sets,
	as well as for each step size through n_range different cluster size. returns a collection of labels and evaluation 
	scores for each X_set-n_cluster. 
	inputs | X_sets is a collection of sets. Each set is a collection of flattened matrices obtained from get_graphcuts
	'''
	model_scores = dict()
	for X_set_index in range(len(X_sets)): 
		model_scores[str(X_set_index+1)+"steps"] = _iterate_ncluster(n_range, X_sets[X_set_index], 
		_fit_cluster, cluster_algo=cluster_algo, affinity=affinity, agglo_link=agglo_link)
	return model_scores


def _iterate_ncluster(n_range, X, _fit_cluster, cluster_algo="spectral", 
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

		sil_score = silhouette_score(affinity_matrix, labels, metric="precomputed")
		ch_score = calinski_harabaz_score(affinity_matrix, labels)
		db_score =  davies_bouldin_score(affinity_matrix, labels)
        
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


if __name__ == "__main__":
	grew.init()
	seed(1)
	sentence_nums = sorted(sample(range(1,1562,1),20)) # using same test sentences as main.py
	ud_graphs = [grew.graph("./data/amr_bank_data/ud/sentence{:04d}.conll".format(sentence_num) for sentence_num in sentence_nums)]

	#X_sets = [X1_testset, X2_testset, X3_testset, X4_testset, X5_testset]

	#test_results = iterate_graphcuts(X_sets, range(2,5), _fit_cluster, cluster_algo="spectral", 
	#								affinity="cosine", agglo_link="complete")
	#print(get_best_stepnclust(test_results, eval_metric="davies_bouldin"))