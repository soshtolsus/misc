#!/usr/bin/env python3

'''
convert YAML to JSON

Copyright 2014 Carl Johnson IV
'''

import argparse
import yaml
import json
import sys
import pdb

def getargs():
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('--compact', action='store_true', help='output the most compact JSON possible')
	parser.add_argument('--with-tabs', action='store_true', help='presume YAML has been output with tabs')
	parser.add_argument('from_file', metavar='from-file', nargs='?', default=None, help='file to load - defaults to stdin')

	return parser.parse_args()

def main(args):
	with sys.stdin if args.from_file is None else open(args.from_file, 'r') as r:
		if args.with_tabs:
			preprocess = lambda x: x.replace('\t', ' '*4)
		else:
			preprocess = lambda x: x

		if args.compact:
			dump_kwargs = {'separators': (',',':')}
		else:
			dump_kwargs = {
				'sort_keys': True,
				'indent': 4,
				'separators': (',', ': ')}

		print(json.dumps(preprocess(yaml.load(r.read())), **dump_kwargs))

if __name__=='__main__':
	try:
		main(getargs())
	except KeyboardInterrupt:
		print('exiting gracefully', file=sys.stderr)
