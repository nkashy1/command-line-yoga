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
    count_parser.add_argument(
        '--index',
        action='store_true',
        help='If set, expects the input file to be a precomputed index (in JSON format)',
    )
    count_parser.add_argument(
        '--sort',
        '-s',
        action='store_true',
        help='If set, sorts words by frequency in output',
    )
    count_parser.add_argument(
        '--gt',
        type=int,
        help='(Optional) Only use words that occur more than this many times',
    )
    count_parser.add_argument(
        '--lt',
        type=int,
        help='(Optional) Only use words that occur less than this many times',
    )

    def count_handler(args):
        with args.infile as ifp, sys.stderr:
            if args.index:
                index = json.load(ifp)
            else:
                document = ifp.read()
                index = index_document(document)

            freqs = [(key, len(value)) for key, value in index.items()]
            if args.lt is not None:
                freqs = [item for item in freqs if item[1] < args.lt]
            if args.gt is not None:
                freqs = [item for item in freqs if item[1] > args.gt]
            if args.sort:
                freqs.sort(key=lambda item: item[1], reverse=True)

            for key, value in freqs:
                try:
                    print(f'{key} {value}')
                except BrokenPipeError:
                    break

    count_parser.set_defaults(func=count_handler)

    args = parser.parse_args()
    args.func(args)
