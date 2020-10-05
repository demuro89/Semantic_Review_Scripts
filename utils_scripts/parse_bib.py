import sys
import os
from pybtex.database.input import bibtex

parser = bibtex.Parser()
bib_data = parser.parse_file('biblio_all')

for e in bib_data.entries:
	print("Title: "+bib_data.entries[e].fields[u'title']+" Anno: "+bib_data.entries[e].fields[u'year'])
