import json
import os
from typing import AnyStr, List, override

import core
from ai.abstract import AbstractAi
from ai import AbstractPromptProvider, Prompt
from utils import AbstractValidator

logger = core.get_logger(__name__)


class TaggerPromptProvider(AbstractPromptProvider):

    def __init__(self):
        super().__init__()

    def construct_prompt(self,
                         tag_number: int,
                         current_tags: [str],
                         data: str) -> Prompt:
        tag_number = 5 if tag_number is None else tag_number

        system_instruction = ("Your answer will only contains this json format only :"
                              + os.linesep + "{" + os.linesep
                              + "\"tags\" : [#tag1, #tag2, ...]"
                              + os.linesep + "}" + os.linesep
                              + "Each tag start with '#' and follow CamelCase. "
                              + "(An example: '#ThisIsATag'). "
                              + "Tags are always singular! "
                              + "Warning! Do not write anything after the json. "
                              + "Your response will be interpreted by a Software. "
                              + "The user will provide you a list of existing tags. "
                              + "Use a maximum of pertinent tags from this list. "
                              + os.linesep)

        user_instruction = (f"Determine {tag_number} tags for this markdown"
                            f"file below based on your analysis and on this list:"
                            + os.linesep
                            + current_tags.__repr__()
                            + os.linesep
                            + "This is the markdown file: "
                            + os.linesep
                            + data)
        return Prompt(system_prompt=system_instruction, user_prompt=user_instruction)


class TaggerValidator(AbstractValidator[str]):

    def __init__(self):
        super().__init__()

    @staticmethod
    @override
    def _validate(input_value: str) -> bool:
        logger.info("Start validating.")

        try:
            tags = json.loads(input_value)
        except Exception as e:
            logger.error(f"Error parsing: {e}")
            return False

        return not (tags["tags"][0].count("#") != 1
                    or tags["tags"][0].count(" ") != 0)


class Tagger:

    def __init__(self, ai: AbstractAi):
        self._prompt_provider = TaggerPromptProvider()
        self._prompt = None
        self._ai = ai

    @staticmethod
    def _read_file(file_path: str) -> AnyStr:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read()
        return data

    @staticmethod
    def _read_file_into_list(file_path: str) -> List[str]:
        with open(file_path, 'r') as file:
            data = file.read().splitlines()
        return data

    def tag_file(self, file_path: str, tag_path: str, tag_number: int) -> None:
        data = Tagger._read_file(file_path)
        current_tags = self._read_file_into_list(tag_path)

        self._prompt = self._prompt_provider.construct_prompt(tag_number=tag_number,
                                                              current_tags=current_tags,
                                                              data=data)
        chat_response = self._ai.compute(self._prompt)
        chat_response_values = json.loads(chat_response)

        determined_tags = chat_response_values["tags"]

        with open(file_path, 'a') as file:
            file.write("\n")
            file.write("_tags_ : " + " ".join(determined_tags))

        logger.info(f"Determined tags: {determined_tags}")
        new_tags = list(set(determined_tags) - set(current_tags))
        logger.info(f"Number of new tags: {len(new_tags)}")
        logger.info(f"Number of old tags: {len(determined_tags) - len(new_tags)}")

        # Write each new_tag to the file at "tag_path"
        if len(new_tags) != 0:
            with open(tag_path, 'a') as file:
                filtered_tags = list(filter(lambda item: item.strip() != "", new_tags))
                file.writelines(tag + "\n" for tag in filtered_tags)
