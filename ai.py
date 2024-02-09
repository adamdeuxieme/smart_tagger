import os
from abc import ABC, abstractmethod
from enum import Enum
from typing import Union

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from openai import OpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

from prompt_provider import Prompt
from validator import AbstractValidator


class AbstractAi(ABC):

    def __init__(self, temperature: Union[float, None] = None, validator: AbstractValidator[str] = None):
        if temperature is None:
            temperature = 0.0
        elif not isinstance(temperature, float):
            raise TypeError("Temperature must be a float!")
        self._temperature = temperature
        self._validator = validator

    @property
    def temperature(self) -> float:
        return self._temperature

    @temperature.setter
    def temperature(self, new_value: float) -> None:
        if not isinstance(new_value, float):
            raise TypeError("Temperature must be a float!")
        if new_value < 0.0 or new_value > 1.0:
            raise ValueError("Temperature must be between 0.0 and 1.0!")
        self._temperature = new_value

    @property
    def validator(self) -> AbstractValidator[str]:
        return self._validator

    @validator.setter
    def validator(self, validator: AbstractValidator[str]) -> None:
        if not isinstance(validator, AbstractValidator):
            raise ValueError("Validator is not an instance of Validator.")

    def compute(self, prompt: Prompt) -> str:
        value_computed = self._compute(prompt)
        if self.validator:
            self._validator.validate(input_value=value_computed, raise_error=True)
        return value_computed

    @abstractmethod
    def _compute(self, prompt: Prompt) -> str:
        pass


class MistralAiModel(Enum):
    TINY = "mistral-tiny"
    SMALL = "mistral-small"
    MEDIUM = "mistral-medium"


class MistralAi(AbstractAi):

    def __init__(self,
                 temperature: float,
                 validator: AbstractValidator[str],
                 model: MistralAiModel = None):

        super().__init__(temperature, validator)

        # Set api key
        self.api_key = os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY environment variable is not set.")

        # Set model
        if model is None:
            model = MistralAiModel.SMALL
        elif not isinstance(model, MistralAiModel):
            raise ValueError("The model must be an instance of MistralAiModel.")
        self._model = model

        # Set client
        self._client = MistralClient(self.api_key)

        # Declare conversation history
        self._conversation_history = []

    @property
    def model(self) -> MistralAiModel:
        return self._model

    @model.setter
    def model(self, model: MistralAiModel):
        if not isinstance(model, MistralAiModel):
            raise ValueError("The model must be an instance of MistralAiModel.")
        self._model = model

    def _compute(self, prompt: Prompt) -> str:
        self._conversation_history.append(
            ChatMessage(role="system", content=prompt.system_prompt)
        )
        self._conversation_history.append(
            ChatMessage(role="user", content=prompt.user_prompt)
        )

        chat_response = self._client.chat(
            model=self.model.value,
            messages=self._conversation_history,
            temperature=self.temperature,
        )
        return chat_response.choices[0].message.content


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
