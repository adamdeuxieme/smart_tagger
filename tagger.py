import json
import os
from typing import AnyStr, List

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


class Tagger:

    def __init__(self, tag_number: int):
        self.initial_user_instruction = \
            (f"Determine {tag_number} tags for this markdown file below based on your analysis and on this list:"
             + os.linesep)

        self.initial_system_instruction = ("Your answer will only contains this json format only :"
                                           + os.linesep + "{" + os.linesep
                                           + "\"tags\" : [#tag1, #tag2, ...]"
                                           + os.linesep + "}" + os.linesep
                                           + "Each tag start with '#' and space are '_' with no escape symbol."
                                           + "Warning! Do not write anything after the json. "
                                           + "Your response will be interpreted by a Software. "
                                           + "The user will provide you a list of existing tags. "
                                           + "Use a maximum of pertinent tags from this list. "
                                           + os.linesep)

    @staticmethod
    def _read_file(file_path: str) -> AnyStr:
        with open(file_path, 'r') as file:
            data = file.read()
        return data

    @staticmethod
    def _read_file_into_list(file_path: str) -> List[str]:
        with open(file_path, 'r') as file:
            data = file.read().splitlines()
        return data

    def ask_mistral(self, file_path: str, tag_path: str) -> None:
        data = Tagger._read_file(file_path)
        current_tags = self._read_file_into_list(tag_path)

        api_key = os.getenv("MISTRAL_API_KEY")
        model = "mistral-medium"

        client = MistralClient(api_key=api_key)
        conversation_history = [
            ChatMessage(role="system", content=self.initial_system_instruction),
            ChatMessage(role="user", content=self.initial_user_instruction
                                             + current_tags.__repr__()
                                             + os.linesep
                                             + "This is the markdown file: "
                                             + os.linesep
                                             + data)
        ]
        print(self.initial_system_instruction)
        print(self.initial_user_instruction + data)

        chat_response = client.chat(
            model=model,
            messages=conversation_history,
            temperature=0.0,
        )

        print(f"Mistral response : {chat_response.choices[0].message.content}")

        chat_response_values = json.loads(chat_response.choices[0].message.content)

        if chat_response_values["tags"][0].count("#") != 1 or chat_response_values["tags"][0].count(" ") != 0:
            raise Exception("The tags are not in a good syntax.")

        determined_tags = chat_response_values["tags"]

        with open(file_path, 'a') as file:
            file.write(os.linesep)
            file.write("_tags_ : " + " ".join(determined_tags))

        print(f"Determined tags: {determined_tags}")
        new_tags = list(set(determined_tags) - set(current_tags))
        print(f"Number of new tags: {len(new_tags)}")
        print(f"Number of old tags: {len(determined_tags) - len(new_tags)}")

        # Write each new_tag to the file at "tag_path"
        if len(new_tags) != 0:
            with open(tag_path, 'a') as file:
                filtered_tags = list(filter(lambda item: item.strip() != "", new_tags))
                file.writelines(tag + "\n" for tag in filtered_tags)
