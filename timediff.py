#!/usr/bin/env python3

'''
Diff some times, dawg.

Copyright 2014 Carl Johnson IV
'''

import argparse
import sys
from collections import namedtuple
import time
import datetime
import re


class TimePairAction(argparse.Action):
	TimePair = namedtuple('TimePair', ['start', 'end'])
	Time = namedtuple('Time', ['hour', 'minute'])

	def __init__(self, option_strings, dest, **kwargs):
		self.dest = dest
		super().__init__(option_strings, dest, **kwargs)

	def __call__(self, parser, namespace, values, option_string):
		setattr(namespace, self.dest, list(self.parse(values)))

	def parse(self, values):
		values_iterator = iter(values)
		for first_value in values_iterator:
			#KLUGE: totally cheating to group into pairs
			second_value = next(values_iterator, None)

			try:
				yield self.parse_pair(first_value, second_value)
			except ValueError:
				continue

	def parse_pair(self, start_str, end_str=None):
		if end_str is None:
			now = datetime.datetime.fromtimestamp(time.time())
			end_time = self.Time(*[getattr(now, x) for x in ('hour', 'minute')])
		else:
			end_time = self.parse_time(end_str)

		return (self.parse_time(start_str), end_time)

	def parse_time(self, value):
		match = re.match('(?P<hour>[01][0-9]|2[0-3])(?P<minute>[0-5][0-9])', value)

		if match is None:
			raise ValueError("didn't match regex ({})".format(value))
		else:
			return self.Time(hour=int(match.group('hour')), minute=int(match.group('minute')))

def getargs():
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('time_pairs', metavar='begin_time end_time', nargs='+', action=TimePairAction, help='Format must be HHMM.')

	return parser.parse_args()

def main(args):
	print(args)

if __name__ == '__main__':
	try:
		main(getargs())
	except KeyboardInterrupt:
		print('exiting gracefully', file=sys.stderr)
