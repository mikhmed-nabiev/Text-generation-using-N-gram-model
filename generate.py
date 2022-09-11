import argparse
from n_gram_model import NGramModel

def get_commandline_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('--model', help='path to model')
	parser.add_argument('--prefix', help='a word to start text generation')
	parser.add_argument('--length', help='length of a generated text', type=int)
	args = parser.parse_args()
	return args

args = get_commandline_arguments()

def get_paramters(args):
	return args.model, args.prefix, args.length

path_to_model, prefix, length_of_text = get_paramters(args)


model = NGramModel(2)

model.load_model(path_to_model)

model.generate(prefix, length_of_text)