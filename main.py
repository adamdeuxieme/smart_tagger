import argparse

from ai import MistralAi, MistralAiModel
from tagger import Tagger, TaggerValidator


def main():

    # Manager args
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command')
    tag_parser = subparser.add_parser('tag')
    tag_parser.add_argument('--filePath', '-f', type=str, required=True)
    tag_parser.add_argument('--tagPath', '-t', type=str, required=True)
    tag_parser.add_argument('--tagNumber', '-tn', type=int, required=False)
    tag_parser.add_argument('--temperature', '-temp', type=float, required=False)
    tag_parser.add_argument('--model', '-m', type=MistralAiModel, required=False)
    tag_parser.add_argument('--mistralai', action="store_true")
    tag_parser.add_argument('--chatgpt', action="store_true")
    args = parser.parse_args()

    if args.command == 'tag':
        if args.mistralai:
            print(f"Args was: {args}")
            mistralai = MistralAi(
                temperature=args.temperature,
                validator=TaggerValidator(),
                model=args.model
            )
            tagger = Tagger(mistralai)
            tagger.tag_file(args.filePath, args.tagPath, args.tagNumber)

        elif args.chatgpt:
            print("Not implemented yet. For now, use mistralai instead.")
        else:
            print("Artificial Intelligence to use not specified. Please specify it.")


if __name__ == '__main__':
    main()
