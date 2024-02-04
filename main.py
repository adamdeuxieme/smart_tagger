import argparse
from pathlib import Path

from tagger import Tagger


def main():

    # Manager args
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command')
    tag_parser = subparser.add_parser('tag')
    tag_parser.add_argument('--filePath', '-f', type=str, required=True)
    tag_parser.add_argument('--tagPath', '-t', type=str, required=True)
    tag_parser.add_argument('--tagNumber', '-tn', type=int, required=True)
    args = parser.parse_args()

    if args.command == 'tag':
        tagger = Tagger(args.tagNumber)
        tagger.ask_mistral(args.filePath, args.tagPath)


if __name__ == '__main__':
    main()
