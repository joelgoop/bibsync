# -*- coding: utf-8 -*-
import click
import logging, logging.config

logger = logging.getLogger("bibsync")


@click.group(help='tools to sync bibtex .bib files')
@click.option('--debug',is_flag=True,help='show debug messages')
def cli(debug):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(format="%(asctime)s [%(levelname)-8s] %(message)s",
                        datefmt="%H:%M:%S")
    logger.setLevel(level)



@cli.command(help='merge several source files into one target')
@click.argument('src', nargs=-1, type=click.Path(exists=True,dir_okay=False))
@click.argument('dest', nargs=1, type=click.Path(dir_okay=False))
@click.option('--strip-fields', '-s', multiple=True,
    help='fields to remove from source files')
@click.option('--watch', '-w', is_flag=True, help='watch for changes in src')
def merge(src, dest, strip_fields, watch):
    """
    Merge a number of source files into one destination. Strip unwanted fields
    and keep fields that already exist in destination, but not in source. 
    """
    from .bib import merge

    merge(src, dest, strip_fields)
    if watch:
        logger.info("Watching for changes.")
        from collections import defaultdict
        from os.path import dirname, abspath, basename
        from .watching import watch

        watch_paths = defaultdict(list)
        for p in src:
            d = abspath(dirname(p))
            watch_paths[d].append(basename(p))

        mergefunc = lambda e: merge(src, dest, strip_fields)
        watch(watch_paths, mergefunc)