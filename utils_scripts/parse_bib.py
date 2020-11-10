#!/usr/bin/env python3

import sys
import argparse

import bibtexparser

unknown_field = 'UNKNOWN'

class ParserState(object):
    def __init__(self,
                 skip_single_journals=True,
                 skip_single_conferences=True,
                 skip_single_books=True,
                 skip_single_authors=True):
        self.years = {}
        self.authors = {}
        self.conferences = {}
        self.books = {}
        self.journals = {}

        # Counter for differentiate unknown entries
        self.unknown_counter = 0

        # Do not print journals with single entries
        self.skip_single_journals = skip_single_journals

        # Do not print conferences with single entries
        self.skip_single_conferences = skip_single_conferences

        # Do not print books with single entries
        self.skip_single_books = skip_single_books

        # Do not print authors with single entries
        self.skip_single_authors = skip_single_authors

    def _get_unknown_unique_entry(self):
        retval = "{}_{}".format(unknown_field, self.unknown_counter)
        self.unknown_counter += 1
        return retval

    def append_journal(self, journalentry):
        journalname = journalentry.get('journal', unknown_field)
        if (journalname == unknown_field):
            journalname = self._get_unknown_unique_entry()
        self.journals[journalname] = self.journals.get(journalname, 0) + 1

    def append_conference(self, conferenceentry):
        confname = conferenceentry.get('booktitle', unknown_field)
        if (confname == unknown_field):
            confname = self._get_unknown_unique_entry()
        self.conferences[confname] = self.conferences.get(confname, 0) + 1

    def append_book(self, bookentry):
        bookname = bookentry.get('title', unknown_field)
        if (bookname == unknown_field):
            bookname = self._get_unknown_unique_entry()
        self.books[bookname] = self.books.get(bookname, 0) + 1

    def increment_authors(self, entryauthorfield):
        for author in entryauthorfield.split(' and '):
            # The "other" author should not be accounted
            if ('other' in author):
                author = self._get_unknown_unique_entry()
            self.authors[author] = self.authors.get(author, 0) + 1

    def increase_year(self, year):
        self.years[year] = self.years.get(year, 0) + 1

    def print_summary(self):
        print("=== BibTeX summary ===")
        print("Total journal articles:\t\t{}".format(sum(self.journals.values())))
        print("Total conference articles:\t{}".format(sum(self.conferences.values())))
        print("Total books:\t\t\t{}".format(sum(self.books.values())))
        print("")
        print("Total different journals:\t{}".format(len(self.journals.keys())))
        print("Total different conferences:\t{}".format(len(self.conferences.keys())))
        print("Total different books:\t\t{}".format(len(self.books.keys())))
        print("")
        print("Years")
        for year,num in sorted(self.years.items(), reverse=True, key=lambda x: x[0]):
            print("\t{}\t{}".format(year,num))
        if (len(self.authors) > 0):
            print("")
            print("Common authors by number of entries")
            for author,num in sorted(self.authors.items(), reverse=True, key=lambda x: x[1]):
                if (num == 1 and self.skip_single_authors):
                    continue
                print("\t{}{}{}".format(author,' '*(40-len(author)),num))
        if (len(self.conferences) > 0):
            print("")
            print("Common conferences by number of entries")
            for conference,num in sorted(self.conferences.items(), reverse=True, key=lambda x: x[1]):
                if (num == 1 and self.skip_single_conferences):
                    continue
                print("\t{}\t{}".format(num, conference))
        if (len(self.books) > 0):
            print("")
            print("Common books by number of entries")
            for book,num in sorted(self.books.items(), reverse=True, key=lambda x: x[1]):
                if (num == 1 and self.skip_single_books):
                    continue
                print("\t{}\t{}".format(num,book))
        if (len(self.journals) > 0):
            print("")
            print("Common journals by number of entries")
            for journal,num in sorted(self.journals.items(), reverse=True, key=lambda x: x[1]):
                if (num == 1 and self.skip_single_journals):
                    continue
                print("\t{}\t{}".format(num, journal))

    def _search_keywords(self, entryfield, keywords):
        for keyword in keywords:
            if keyword in entryfield:
                return True
        return False

    # Check if the name of the book is a workshop
    def is_workshop(self, entrybooktitle):
        return self._search_keywords(entrybooktitle, ( "Workshop", "workshop" ))

    # Check if the name of the book is a conference
    def is_conference(self, entrybooktitle):
        keywords = []
        keywords.append("Conf")
        keywords.append("conf")
        keywords.append("Symposium")
        keywords.append("symposium")
        keywords.append("Convention")
        keywords.append("convention")

        # Known conferences
        keywords.append("(SecDev)")
        keywords.append("IPTComm")

        return self._search_keywords(entrybooktitle, keywords)

    # Check if the name of the book is a forum
    def is_forum(self, entrybooktitle):
        keywords = []
        keywords.append("Forum")
        keywords.append("forum")

        return self._search_keywords(entrybooktitle, keywords)

    # Check if the name of the book is a seminar
    def is_seminar(self, entrybooktitle):
        keywords = []
        keywords.append("Seminar")
        keywords.append("seminar")

        return self._search_keywords(entrybooktitle, keywords)

    # Insert the entry in the parser
    def parse(self, entry):
        entryauthors = entry.get('author', unknown_field)
        entrytype = entry.get('ENTRYTYPE', unknown_field)
        entryconf = entry.get('booktitle', unknown_field)
        entryyear = entry.get('year', 0)

        # Check journal entries
        if (entry.get('journal', False)):
            self.append_journal(entry)
        elif (entrytype == 'book'):
            self.append_book(entry)
        elif (self.is_seminar(entryconf) or
              self.is_conference(entryconf) or
              self.is_forum(entryconf) or
              self.is_workshop(entryconf)):
            self.append_conference(entry)
        else:
            # Fallback to conference paper
            print('Warning: unclassified conference "{}"'.format(entryconf), file=sys.stderr)
            gstate.append_conference(entry)

        self.increase_year(entryyear)
        self.increment_authors(entryauthors)

parser = argparse.ArgumentParser(
        description='Parse and print information from bibtex files'
)

parser.add_argument('--single_journals',    action='store_true',
                    help="Display journals with a single entry")
parser.add_argument('--single_authors',     action='store_true',
                    help="Display authors with a single entry")
parser.add_argument('--single_books',       action='store_true',
                    help="Display books with a single entry")
parser.add_argument('--single_conferences', action='store_true',
                    help="Display conferences with a single entry")

parser.add_argument('bibtex_path', metavar='BibTeX file', nargs=1,
                    help='The target BibTeX file')

args = parser.parse_args()

gstate = ParserState(
        skip_single_journals    = not args.single_journals,
        skip_single_conferences = not args.single_conferences,
        skip_single_books       = not args.single_books,
        skip_single_authors     = not args.single_authors
);

with open(args.bibtex_path[0]) as bibtexfile:
    bib_data = bibtexparser.load(bibtexfile)

for bibtex_entry in bib_data.entries:
    gstate.parse(bibtex_entry)

gstate.print_summary()
