from random import seed, sample

if __name__ == "__main__":
	common = []
	for annoFile in ['./grs/lexicons/original_amr_lexicons/annotator1.txt', './grs/lexicons/original_amr_lexicons/annotator2.txt']:
		#Open each of the annotation files
		with open(annoFile, 'r') as f:
			lines = f.readlines()
		#select 50 random chunks with a step 5 (each chunk will be of size 5, that's why the step is 5)
		seed(1)
		chunk_starts = sorted(sample(range(1,len(lines),5),50))
		#for each of the starts, add a chunk of 5 lines to common
		for start in chunk_starts:
			common += lines[start: start+5]
	#sort the common lines
	common = sorted(common)
	#write them to a file
	with open('./grs/lexicons/original_amr_lexicons/common.txt', 'w') as f:
		for line in common:
			f.write(line)
