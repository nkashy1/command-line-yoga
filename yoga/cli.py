"""
CLI implementation
"""

from .index import index_document

if __name__ == '__main__':
    import argparse
    import json
    import sys

    parser = argparse.ArgumentParser('yoga: Index documents and corpora')
    parser.add_argument(
        'infile',
        type=argparse.FileType(mode='r'),
        nargs='?',
        default=sys.stdin,
        metavar='<input file>',
        help='Input file (default: stdin)',
    )

    args = parser.parse_args()

    with args.infile as ifp:
        document = ifp.read()
        print(json.dumps(index_document(document)))
