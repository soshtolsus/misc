#!/usr/bin/env python3

'''
convert JSON to YAML

Copyright 2014 Carl Johnson IV
'''

import argparse
import yaml
import json
import sys
import pdb

def getargs():
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('--with-tabs', action='store_true', help='indent YAML with tabs')
	parser.add_argument('from_file', metavar='from-file', nargs='?', default=None, help='file to load - defaults to stdin')

	return parser.parse_args()

def main(args):
	with sys.stdin if args.from_file is None else open(args.from_file, 'r') as r:
		if args.with_tabs:
			post_process = lambda x: x.replace(' '*4, '\t')
		else:
			post_process = lambda x: x

		print(post_process(yaml.dump(json.load(r), default_flow_style=False, indent=4)), flush=True)

if __name__=='__main__':
	try:
		main(getargs())
	except KeyboardInterrupt:
		print('exiting gracefully', file=sys.stderr)
