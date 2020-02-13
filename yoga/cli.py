"""
CLI implementation
"""

import argparse
import json
import sys

from .index import index_document

def add_common_args(parser):
    parser.add_argument(
        'infile',
        type=argparse.FileType(mode='r'),
        nargs='?',
        default=sys.stdin,
        metavar='<input file>',
        help='Input file (default: stdin)',
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='yoga: Index documents and corpora')
    subcommands = parser.add_subparsers()

    index_parser = subcommands.add_parser('index', description='Index a document')
    add_common_args(index_parser)

    def index_handler(args):
        with args.infile as ifp:
            document = ifp.read()
            print(json.dumps(index_document(document)))

    index_parser.set_defaults(func=index_handler)

    count_parser = subcommands.add_parser(
        'count',
        description='Count word occurrences in a document',
    )
    add_common_args(count_parser)

    def count_handler(args):
        with args.infile as ifp:
            document = ifp.read()
            index = index_document(document)
            counts = {key:len(value) for key, value in index.items()}
            print(json.dumps(counts))

    count_parser.set_defaults(func=count_handler)

    args = parser.parse_args()
    args.func(args)
