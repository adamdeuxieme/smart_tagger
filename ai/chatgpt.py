from enum import Enum
from typing import Union

from openai import OpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

from utils.validator import AbstractValidator
from .abstract import AbstractAi, Prompt


class ChatGPTModel(Enum):
    GPT3_turbo_flagship = "gpt-3.5-turbo-0125"
    GPT4 = "gpt-4"


class ChatGptAi(AbstractAi):

    def __init__(self,
                 temperature: Union[float, None],
                 validator: Union[AbstractValidator[str], None],
                 model: Union[ChatGPTModel, None] = None
                 ):
        super().__init__(temperature, validator)

        # Set model
        if model is None:
            model = ChatGPTModel.GPT3_turbo_flagship
        elif not isinstance(model, ChatGPTModel):
            raise ValueError("The model must be an instance of ChatGPTModel.")
        self._model = model

        # Set client
        self._client = OpenAI()

        # Declare conversation history
        self._conversation_history = []

    def _compute(self, prompt: Prompt) -> str:
        self._conversation_history.append(
            ChatCompletionSystemMessageParam(content=prompt.system_prompt, role="system")
        )

        self._conversation_history.append(
            ChatCompletionUserMessageParam(content=prompt.user_prompt, role="user")
        )

        completion = self._client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self._conversation_history
        )

        return completion.choices[0].message.content
