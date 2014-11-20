#!/usr/bin/env python3

'''create an email address that has meaning but isn't predictable'''

import string
import skein
import sys
import argparse


def parse_args():
	parser = argparse.ArgumentParser(description=__doc__.strip('\n'), formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('key', action='store', help='key with which to munge')
	parser.add_argument('name', action='store', help='the legible part of the address')
	parser.add_argument('--size', action='store', type=int, default=16, help='number of hash characters to keep')
	
	return parser.parse_args()

def main(args):
	hash_key = skein.skein1024(init=args.key.encode(), digest_bits=512+args.size, pers=b'emaddygen').digest()
	hash_name = skein.skein1024(init=args.name.encode(), digest_bits=512+args.size, pers=b'emaddygen').digest()

	total_hash = tuple(map(lambda x: x[0]^x[1], zip(hash_key, hash_name)))

	hash_int = int.from_bytes(total_hash, 'big')

	hash_str = letterify(hash_int)[:args.size]

	insert_position = hash_int % (args.size - 2) + 1

	print('{}.{}.{}'.format(hash_str[:insert_position], args.name, hash_str[insert_position:]))

def letterify(hash_int):
	to_return = []
	while hash_int > 0:
		hash_int, to_add = divmod(hash_int, 26)
		to_return.append(string.ascii_lowercase[to_add])
	return ''.join(tuple(reversed(to_return)))

if __name__ == '__main__':
	try:
		main(parse_args())
	except KeyboardInterrupt:
		print('exiting gracefully', file=sys.stderr)
