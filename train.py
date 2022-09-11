import os
import argparse
import pathlib
import re
import json
from n_gram_model import NGramModel

def get_commandline_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('--input-dir', help='path directory where data is stored')
	parser.add_argument('--model', help='path to model')
	args = parser.parse_args()
	return args

def get_paths(args):
	return args.input_dir, args.model

args = get_commandline_arguments()

path_to_data, path_to_model = get_paths(args)

data_dir = pathlib.Path(path_to_data)


model = NGramModel(2)

model.load_model(path_to_model)

model.fit(data_dir)

model.write_to_file(path_to_model)
