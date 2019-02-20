def __amr_graph_to_conllu__(amr_graph):
	'''
	Helper function. Takes an AMR in graph format, converts it into a format 
	for convenient writing to conllu file format with the save_data function. 
	'''
	lines = []
	try:
		lines.append("#sentid = " + amr_graph["1"][0]["sentid"])
	except: 
		pass 
	word_idxs = [i for i in amr_graph.keys() if i != "ROOT"]
	word_idxs.sort()
    
	feature_list = ["form", "lemma", "upos", "xpos", "head", "deprel", "deps", "misc"]
	for word_idx in word_idxs:
		line = [word_idx]
		for feat in feature_list: 
			try:
				line.append(amr_graph[word_idx][0][feat])
			except:
				line.append("-")
		morph_feats = set(amr_graph[word_idx][0].keys()).difference(set(feature_list))           
		morph_feats_list = [feat+"="+amr_graph[word_idx][0][feat]+"|" for feat in morph_feats]
		line.insert(5,"".join(morph_feats_list))
		line = "\t".join(line)
		lines.append(line)
	lines = "\n".join(lines)
	return lines

if __name__== "__main__":
	pass