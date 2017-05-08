# Bibsync -- a tool to sync bibtex files

## Installation

```
git clone https://github.com/joelgoop/bibsync.git && cd bibsync
pip install .
```

### Dependencies

Bibsync needs `click` for the CLI, `bibtexparser` for reading and writing .bib files and `watchdog` for watching for file changes. 

## Usage

To run once:
```
bibsync merge source1.bib [source2.bib ...] destination
```

To watch files for changes:
```
bibsync merge --watch source1.bib [source2.bib ...] destination
```

Running `bibsync` without any arguments or with the `--help` flag will show the command line help message. Help is also available for each subcommand with `bibsync <subcommand> --help`.