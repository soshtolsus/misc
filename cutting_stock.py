#!/usr/bin/env python3

'''
Solve the cutting stock problem by brute force.
'''

import argparse
import itertools
import sys
import math


def getargs():
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('stock_length', type=float, help='length of stock from which to cut pieces')
	parser.add_argument('pieces', type=float, nargs='+', help='the lengths of required pieces to cut')
	parser.add_argument('--good-enough', type=float, help='find a solution with the given minumum efficiency')
	
	return parser.parse_args()

def main(args):
	print('number of permutations: {:d}'.format(math.factorial(len(args.pieces))))
	
	if hasattr(args, 'good_enough'):
		most_efficient_permutation = search_lazily(args.stock_length, args.pieces, args.good_enough)
	else:
		most_efficient_permutation = search_exhaustively(args.stock_length, args.pieces)
	
	print('cut order: {}\nstock pieces required: {:d}\nefficiency: {:.4f}'.format(*most_efficient_permutation))

def search_lazily(stock_length, pieces, threshold):
	if threshold < 0:
		threshold = 0
	elif threshold > 1:
		threshold = 1
	
	maximum_possible_efficiency = (sum(pieces) / stock_length) / (math.ceil(sum(pieces) / stock_length))
	print('maximum possible efficiency: {:.4f}'.format(maximum_possible_efficiency))
	
	for piece_permutation in itertools.permutations(pieces):
		candidate_results = make_cuts(stock_length, piece_permutation)
		if candidate_results[1] >= threshold * maximum_possible_efficiency:
			return tuple([piece_permutation] + list(candidate_results))
		else:
			pass #there will always be an optimal solution (I think)

def search_exhaustively(stock_length, pieces):
	most_efficient_permutation = None
	
	for piece_permutation in itertools.permutations(pieces):
		if most_efficient_permutation is None:
			most_efficient_permutation = tuple([piece_permutation] + list(make_cuts(stock_length, piece_permutation)))
		else:
			candidate_results = make_cuts(args.stock_length, piece_permutation)
			if candidate_results[1] > most_efficient_permutation[2]:
				most_efficient_permutation = tuple([piece_permutation] + list(candidate_results))
		
		if most_efficient_permutation[2] == 1:
			return most_efficient_permutation
	
	return most_efficient_permutation

def make_cuts(stock_length, piece_lengths):
	'''
	chop up the stock into pieces sequentially
	returns stock pieces required, usage percentage
	
	TODO: maybe add consideration for kerf
	'''
	
	wasted_length = 0
	remaining_stock_length = 0
	stock_pieces = 0
	
	for i in piece_lengths:
		if remaining_stock_length < i:
			wasted_length += remaining_stock_length
			remaining_stock_length = stock_length
			stock_pieces += 1
		
		remaining_stock_length -= i
	
	wasted_length += remaining_stock_length
	
	return stock_pieces, 1 - wasted_length / (stock_pieces * stock_length)

if __name__=='__main__':
	try:
		main(getargs())
	except KeyboardInterrupt:
		print('exiting gracefully', file=sys.stderr)
