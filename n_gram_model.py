import os
import re
import json
import random
import numpy as np

class NGramModel:
	def __init__(self, n_for_ngram):
		self.n_for_ngram = n_for_ngram
		self.model = {}
		self.processed_data = []
		self.array_of_words = []
		self.array_of_ngrams = []

	def load_model(self, path_to_model):
		if os.path.isfile(path_to_model):
			model_file = open(path_to_model, 'r')
			self.model = json.load(model_file)
		else: 
			print('Model is not yet created')
		
		if os.path.isfile('data/processed_data.json'):
			processed_data_file = open('data/processed_data.json', 'r')
			self.processed_data = json.load(processed_data_file)
		
		for n_gram in self.model:
			self.array_of_ngrams.append(n_gram)

	def clear_text(self, content) -> list:
		stopwords_file = open('data/stop_words_english.json', 'r')
		stopwords_array = json.load(stopwords_file)
		content = content.lower()
		regex = re.compile('[^a-z]')
		content = regex.sub(',', content)
		content = re.split(',', content)
		words = []
		for word in content:
			if word.isalpha() == True and not(word in stopwords_array):
				words.append(word)
		return words

	def read_data(self, data_dir):
		for file in data_dir.iterdir():
			if file.name.endswith('.txt') and not(file.name in self.processed_data):
				print('Collecting data from ', file.name)
				self.processed_data.append(file.name)
				content = open(file, 'r').read()
				words_array_from_a_text = self.clear_text(content)
				self.array_of_words.extend(words_array_from_a_text)
		self.write_to_file('data/processed_data.json', 0)

	def count_probability(self, cur_model) -> dict:
		for prefix, words_and_probabilites in cur_model.items():
			for j in range(len(self.array_of_words) - self.n_for_ngram):
				n_gram_to_compare = ' '.join(self.array_of_words[j:j+self.n_for_ngram])
				if n_gram_to_compare == prefix:
					cur_model[prefix][self.array_of_words[j+self.n_for_ngram]] += 1.0
			all_occurences = 0
			for word in cur_model[prefix]:
				all_occurences += cur_model[prefix][word]
			for word in cur_model[prefix]:
				cur_model[prefix][word] = cur_model[prefix][word] / all_occurences
		return cur_model

	def update_model(self, n_gram) -> dict:
		cur_model = {}
		for key in n_gram:
			cur_model[key] = {}
			for j in range(len(self.array_of_words) - self.n_for_ngram):
				n_gram_to_compare = ' '.join(self.array_of_words[j:j+self.n_for_ngram])
				if key == n_gram_to_compare:
					if not(self.array_of_words[j + self.n_for_ngram] in cur_model[key]):
						cur_model[key][self.array_of_words[j + self.n_for_ngram]] = 0.0
		return self.count_probability(cur_model)
	

	def make_ngram(self):
		n_grams = []
		for i in range(len(self.array_of_words)):
			n_gram = " ".join(self.array_of_words[i:i+self.n_for_ngram])
			self.array_of_ngrams.append(n_gram)
			n_grams.append(n_gram)

		new_model = self.update_model(n_grams)
		self.model = merge_dicts(self.model, new_model)

	def write_to_file(self, path_to_write, flag = 1):
		with open(path_to_write, 'w') as write_file:
			if flag:
				json.dump(self.model, write_file)
			else:
				json.dump(self.processed_data, write_file)

	def fit(self, data_dir):
		print('Training started\n')
		self.read_data(data_dir)
		self.make_ngram()

	def generate(self, prefix, length):
		index = 0
		generated_text = prefix
		length -= 1
		while (length > 0):
			if index >= len(self.array_of_ngrams):
				print("Did not found such word")
				return
			if prefix in self.array_of_ngrams[index]:
				entry_point = self.array_of_ngrams[index]
				length -= 1
				possible_words = []
				probability_of_words = []
				for word, probability in self.model[entry_point].items():
					possible_words.append(word)
					probability_of_words.append(probability)
				generated_word = np.random.choice(possible_words, p=probability_of_words)
				generated_text += " " + generated_word
				prefix = generated_word
				index = 0
				random.shuffle(self.array_of_ngrams)
			index += 1
		print(generated_text + '\n')


def merge_dicts(dict1, dict2) -> dict:
	result = {}
	for key1, val_dict1 in dict1.items():
		if key1 in dict2:
			temp_dict = {}
			min_dict = val_dict1 if len(val_dict1) < len(dict2[key1]) else dict2[key1]
			for min_key, min_value in min_dict.items():
				if min_key in dict2[key1]:
					temp_dict[min_key] = min_value if min_value > dict2[key1][min_key] else dict2[key1][min_key]
				else:
					temp_dict[min_key] = min_value
			max_dict = val_dict1 if len(val_dict1) > len(dict2[key1]) else dict2[key1]
			for max_key, max_value in max_dict.items():
				if not(max_key in min_dict):
					temp_dict[max_key] = max_value
			result[key1] = temp_dict
		else:
			result[key1] = val_dict1
	
	for key2, val_dict2 in dict2.items():
		if not(key2 in dict1):
			result[key2] = val_dict2

	return result
