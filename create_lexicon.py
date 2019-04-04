import os
import re

class Predicate:
	def __init__(self,pred,concept):
		self.pred = pred
		self.concept = concept
		# self.arg0 = None
		# self.arg1 = None
		# self.arg2 = None
		# self.arg3 = None
		# self.arg4 = None
		# self.arg5 = None
		# self.arg6 = None
		# self.arg7 = None
		# self.arg8 = None
		# self.arg9 = None
		# self.arg10 = None
		self.args = ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-']

	def to_string(self):
		return '\t'.join([self.pred, self.concept]+self.args)

def create_lexicon(load_path, save_path):
	with open(save_path, 'a') as writefile:
		with open(load_path, 'r') as file:
			lines = file.readlines()
		for line in lines:
			# print(line)
			concept = line.split(' ')[0]
			pred = concept.split(re.search(r'-\d+$', concept).group())[0]
			# print(concept, pred)
			args = line.replace(concept,'').strip().split('ARG')
			# print(args)
			predicate = Predicate(pred, concept)
			agent = [' agent ', pred+'or', pred+'er', pred[:-1]+'or', pred[:-1]+'er']
			patient = [' patient ', 'thing '+pred+'ed', 'thing '+pred[:-1]+'ed']
			for idx, arg in enumerate(args[1:]):
				#
				for a in agent:
					if a in arg:
						predicate.args[idx] = 'agent'
						print(arg)
						continue
				for p in patient:
					if p in arg:
						predicate.args[idx] = 'patient'
						print(arg)
						continue
				# if ' location ' in arg:
				# 	predicate.args[idx] = 'location'
				# 	continue
			#if all args for a line are classified, write the predicate line to the lexicon
			for idx, arg in enumerate(args[1:]):
				complete = 1
				if predicate.args[idx] == '-':
					complete = 0
			if complete:
				writefile.write(predicate.to_string()+'\n')
				pass
			print(predicate.to_string())



if __name__ == "__main__":
	create_lexicon('./grs/lexicons/original_amr_lexicons/propbank-amr-frames-arg-descr.txt',
					'./grs/lexicons/subcat/propbank_predicates.lp')


