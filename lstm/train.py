#!/usr/bin/python
# -*- coding: utf-8 -*-

from model import *
import os
import argparse
from time import time
import json

def main():
	parser = argparse.ArgumentParser(description='Ancient Chinese poetry generator.')
	parser.add_argument('-m','--model',type = str,help = "Model weights directory path to save.",default = "../model/weights")
	# parser.add_argument('-p','--prime',type = str,help = "Initial Chinese characters for each sentence.",default = "")
	# parser.add_argument('-s','--sentence',type = str,help = "First sentence for the poem.",default = "")
	parser.add_argument('-d','--data',type = str,help = "Training data.",default = "../datasets/data_sample.txt")
	# parser.add_argument('-t','--train',nargs = 0,help = "If -t is set, model will be trained and not generating poems")


	args = parser.parse_args()

	data_t = open(args.data,'r',encoding = 'utf-8')
	raw_dict = json.loads(data_t.read())
	data_t.close()

	#build vocabulary
	voc_count = {}
	voc = ['$']
	print("Counting characters...")
	for poem in raw_dict:
		for c in poem['paragraphs']:
			if c not in voc:
				voc_count[c] = 1
				voc.append(c)
			elif c != '$':
				voc_count[c] += 1

	n_voc = len(voc)

	char_to_int = dict((c, i) for i, c in enumerate(voc))
	# int_to_char = dict((i, c) for i, c in enumerate(voc))

	out = open(args.model + '/vocabulary.json','w',encoding='utf8')
	out.write(json.dumps([voc,voc_count],indent = 4,ensure_ascii=False))
	out.close()

	# getting training data
	print("Getting training data...")
	data_x , data_y = get_training_data(raw_dict,char_to_int)
	print(data_x[:6])
	print(data_y[:6])
	# one-hot encoding
	print("Encoding training data...")
	X,Y = one_hot_encode(data_x,data_y,n_voc)

	# build and train
	print("Training...")
	train(X,Y,args.model)
	print("Training stop.")





if __name__ == "__main__":
	start = time()
	main()
	print('Processing Time: {}s\n'.format(time() - start))