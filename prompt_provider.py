from abc import ABC, abstractmethod


class Prompt:
    def __init__(self, system_prompt: str, user_prompt: str):
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt


class AbstractPromptProvider(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def construct_prompt(self, *args) -> Prompt:
        pass
