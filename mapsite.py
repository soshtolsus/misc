#!/usr/bin/env python3

'''simple sitemap generator'''

#Copyright 2014 Carl Johnson IV

import yattag
import sys
import argparse


def getargs():
	pass

def main(args):
	doc, tag, text = yattag.SimpleDoc().tagtext()
	
	doc.asis('<?xml version="1.0" encoding="UTF-8"?>')
	with tag('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'):
		for url in urls:
			with tag('url'):
				with tag('loc'):
					text('{}/{}'.format(args.root, url.ltrim('/')))
				with tag('lastmod'):
					pass
				with tag('changefreq'):
					pass #default to weekly
				with tag('priority'):
					pass #default to 0.5
	
	return yattag.indent(doc.getValue(), indentation='\t')

if __name__=='__main__':
	try:
		print(main(getargs()))
	except KeyboardInterrupt:
		print('exiting gracefully', file=sys.stderr)
