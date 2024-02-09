import argparse

from ai import MistralAi, MistralAiModel, ChatGptAi, ChatGPTModel
from bat_creator import BatCreator, AiEnum
from prompt_provider import Prompt
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
    ai_group = tag_parser.add_mutually_exclusive_group()
    ai_group.add_argument('--mistralai', action="store_true")
    ai_group.add_argument('--chatgpt', action="store_true")

    bat_parser = subparser.add_parser("bat")
    folder_scope_output_path_exclusive_grp = bat_parser.add_mutually_exclusive_group()
    ai_group = bat_parser.add_mutually_exclusive_group()
    bat_parser.add_argument('--mainPath', '-f', type=str, required=False)
    bat_parser.add_argument('--tagPath', '-t', type=str, required=False)
    folder_scope_output_path_exclusive_grp.add_argument('--outputPath', '-o', type=str, required=False)
    bat_parser.add_argument('--tagNumber', '-tn', type=int, required=False)
    ai_group.add_argument('--mistralai', action="store_true")
    ai_group.add_argument('--chatgpt', action="store_true")
    folder_scope_output_path_exclusive_grp.add_argument('--folderScope', action="store_true")
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
            chat_gpt_ai = ChatGptAi(
                args.temperature,
                TaggerValidator(),
                ChatGPTModel.GPT3_turbo_flagship
            )
            tagger = Tagger(chat_gpt_ai)
            tagger.tag_file(args.filePath, args.tagPath, args.tagNumber)
        else:
            print("Artificial Intelligence to use not specified. Please specify it.")

    elif args.command == 'bat':
        model = None
        if args.mistralai or args.chatgpt:
            model = AiEnum.CHATGPT if args.chatgpt else AiEnum.MISTRAL

        if args.folderScope:
            BatCreator.create_bat_script_folder(args.mainPath, args.tagPath, args.tagNumber, model)
        else:
            BatCreator.create_bat_script(args.mainPath, args.tagPath, args.outputPath, args.tagNumber, model)


if __name__ == '__main__':
    main()
