# -*- coding: utf-8 -*-
import click
import logging, logging.config

logger = logging.getLogger(__name__)

DEFAULT_STRIP_FIELDS = [
    'abstract',
    'keywords',
    'file',
    'mendeley-.*'
]

@click.group(help='tools to sync bibtex .bib files')
@click.option('--debug',is_flag=True,help='show debug messages')
def cli(debug):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level,
                        format="%(asctime)s [%(levelname)-8s] %(message)s",
                        datefmt="%H:%M:%S")

@cli.command(help='merge several source files into one target')
@click.argument('src', nargs=-1, type=click.Path(exists=True,dir_okay=False))
@click.argument('dest', nargs=1, type=click.Path(dir_okay=False))
@click.option('--strip-fields', '-s', multiple=True,
    help='fields to remove from source files')
def merge(src, dest, strip_fields=DEFAULT_STRIP_FIELDS):
    """
    Merge a number of source files into one destination. Strip unwanted fields
    and keep fields that already exist in destination, but not in source. 
    """
    import re
    import bibtexparser
    from bibtexparser.bparser import BibTexParser
    from bibtexparser.bwriter import BibTexWriter
    from bibtexparser.bibdatabase import BibDatabase

    # Configure parser to not change 'url' to 'link'
    parser = BibTexParser()
    del parser.alt_dict['url']
    del parser.alt_dict['urls']

    # Configure writer to only write entries and indent with 2 spaces
    writer = BibTexWriter()
    writer.contents = ['entries']
    writer.indent = '  '

    logger.debug(strip_fields)
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

    dest_bib_database = BibDatabase()
    dest_bib_database.entries = dest_bib.values()

    with open(dest, 'w', encoding='utf8') as f:
        bibtexparser.dump(dest_bib_database, f, writer=writer)
