import re
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

import logging
logger = logging.getLogger("bibsync")

DEFAULT_STRIP_FIELDS = [
    'abstract',
    'keywords',
    'file',
    'mendeley-.*'
]

def merge(src, dest, strip_fields=DEFAULT_STRIP_FIELDS):
    # Configure parser to not change 'url' to 'link'
    logger.info("(Re)constructing '{}' from {} sources.".format(dest, len(src)))
    if strip_fields is None:
        strip_fields = []
    elif not strip_fields:
        strip_fields = DEFAULT_STRIP_FIELDS
    
    parser = BibTexParser()
    del parser.alt_dict['url']
    del parser.alt_dict['urls']

    # Configure writer to only write entries and indent with 2 spaces
    writer = BibTexWriter()
    writer.contents = ['entries']
    writer.indent = '  '

    logger.debug("Fields to strip are: '{}'".format(strip_fields))
    strip_re = re.compile(r'({})'.format('|'.join(strip_fields)))

    # Construct a dictionary of all source entries
    parsed_source = {}
    for fn in src:
        with open(fn, 'r', encoding='utf8') as f:
            source_bib = parser.parse_file(f)

        # Filter out unwanted fields
        for entry in source_bib.entries:
            keys = [m.group(1) for m in 
                        (re.search(strip_re, k) for k in entry.keys()) 
                        if m is not None]
            for key in keys:
                del entry[key]

        parsed_source.update(source_bib.entries_dict)

    # Construct dictionary of dest entries if available
    try:
        with open(dest, 'r', encoding='utf8') as f:
            dest_bib = parser.parse_file(f).entries_dict
    except FileNotFoundError:
        dest_bib = {}

    # Update dest, but keep fields that only exist in dest
    for k, v in parsed_source.items():
        tmp = dest_bib.get(k, {})
        tmp.update(v)
        dest_bib[k] = tmp

    write_dict_to_file(dest_bib, dest, writer=writer)


def write_dict_to_file(dest_bib, dest, writer=None):
    dest_bib_database = BibDatabase()
    dest_bib_database.entries = dest_bib.values()

    with open(dest, 'w', encoding='utf8') as f:
        bibtexparser.dump(dest_bib_database, f, writer=writer)
