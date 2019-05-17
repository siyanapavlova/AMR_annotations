import os
import re

roles = ['actor1', 'actor2', 'actor', 'agent', 'asset',
		 'attribute', 'beneficiary', 'cause', 'destination',
		 'experiencer', 'extent', 'instrument', 'location',
		 'material', 'patient', 'patient1', 'patient2',
		 'predicate', 'product', 'recipient', 'source',
		 'stimulus', 'theme', 'theme1', 'theme2', 'time',
		 'topic', 'proposition', "-"]

class Predicate:
	def __init__(self,pred,concept):
		self.pred = pred
		self.concept = concept
		self.args = ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-']

	def to_string(self):
		return '\t'.join([self.pred.strip(), self.concept.strip()]+self.args)

def ask_annotator(predicate, args):
	for idx, arg in enumerate(args[1:]):
		print('-'*10)
		print(arg)
		if arg.split(':')[0].isdigit():
			# print(int(arg.split(':')[0]))
		
			# role = input('Role?\n>>')
			role = input('>>')
			if role.strip() == 'skip':
				return predicate
			if role.strip() == 'stop':
				print(role.strip())
				return None
			if role.strip() in roles:
				predicate.args[int(arg.split(':')[0])] = role.strip()
			else:
				for item in role.strip().split(','):
					if item.strip() not in roles:
						return predicate
				predicate.args[int(arg.split(':')[0])] = role.strip()
	return predicate

def sort_file(file_path):
	with open(file_path, 'r') as readfile:
		lines = readfile.readlines()
	lines = sorted([line for line in lines])
	with open(file_path, 'w') as writefile:
		writefile.write(''.join(lines))

def create_lexicon(load_path, save_path, unprocessed_path):
	#unprocessed string to keep the unprocessed lines
	unprocessed = ''
	with open(save_path, 'a') as writefile:
		with open(load_path, 'r') as file:
			lines = file.readlines()
		flag = 0
		for line in lines:
			if flag == 1:
				unprocessed += line
				continue

			concept = line.split(' ')[0]
			pred = concept.split(re.search(r'-\d+$', concept).group())[0]

			args = line.replace(concept,'').strip().split('ARG')

			predicate = Predicate(pred, concept)

			print('\n\n'+'='*15+'\n\n')
			print(line.strip())

			predicate = ask_annotator(predicate,args)

			# If the user said "stop", flag that and proceed in the function only by copying
			# the remaining lines to unprocessed after which they will be written to the file
			if predicate == None:
				flag = 1
				unprocessed += line
				continue
			
			#Check if the predicate is complete
			complete = 1
			for idx, arg in enumerate(args[1:]):
				if arg.split(':')[0].isdigit():
					if predicate.args[int(arg.split(':')[0])] == '-':
						complete = 0
				else:
					complete = 0
			#if all args for a line are classified, write the predicate line to the lexicon
			if complete:
				writefile.write(predicate.to_string()+'\n')
			else:
				unprocessed += line
	with open(unprocessed_path, 'w') as filewrite:
		filewrite.write(unprocessed)




if __name__ == "__main__":
	create_lexicon('./grs/lexicons/original_amr_lexicons/common-in-progress.txt',
					'./grs/lexicons/subcat/common_predicates_anno1.lp',
					'./grs/lexicons/original_amr_lexicons/common-in-progress.txt')
	sort_file('./grs/lexicons/subcat/common_predicates_anno1.lp')
	


