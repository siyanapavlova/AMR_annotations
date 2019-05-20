import ud_to_amr, amr_graph_to_text, smatcher, parser
import grew
import pprint

pp = pprint.PrettyPrinter(indent=4)

if __name__ == "__main__":

	grew.init()
	ud_graph = ud_to_amr.load_data('./data/amr_bank_data/ud/sentence0005.conll')

	# run a simple GRS 
	grs_filename = './grs/grs_amr_main.grs'
	print("Grew initiated \n")

	result = grew.run(grs_filename, ud_graph, 'test_new_lex')
	pp.pprint(result)