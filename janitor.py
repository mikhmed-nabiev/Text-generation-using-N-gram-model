import argparse
import json

def get_commandline_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('--model', help='path to model')
	args = parser.parse_args()
	return args

args = get_commandline_arguments()

def get_paramters(args):
	return args.model

path_to_model = get_paramters(args)

with open(path_to_model, 'w') as write_file:
	json.dump({}, write_file)

with open('data/processed_data.json', 'w') as write_file:
	json.dump([], write_file)