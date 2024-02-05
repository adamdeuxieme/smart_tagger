import os
from abc import ABC, abstractmethod
from enum import Enum

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

from prompt_provider import Prompt
from validator import AbstractValidator, NotValidException


class AbstractAi(ABC):

    def __init__(self, temperature: float = 0.0, validator: AbstractValidator = None):
        self._temperature = temperature
        self._validator = validator

    @property
    def temperature(self) -> float:
        return self._temperature

    @temperature.setter
    def temperature(self, new_value: float) -> None:
        if new_value < 0.0 or new_value > 1.0:
            raise ValueError("Temperature must be between 0.0 and 1.0.")
        self._temperature = new_value

    @property
    def validator(self) -> AbstractValidator:
        return self._validator

    @validator.setter
    def validator(self, validator: AbstractValidator) -> None:
        if validator is not isinstance(validator, AbstractValidator):
            raise ValueError("Validator is not an instance of Validator.")

    def compute(self, prompt: Prompt) -> str:
        value_computed = self._compute(prompt)
        if self.validator:
            self._validator.validate(value_computed)
        return value_computed

    @abstractmethod
    def _compute(self, prompt: Prompt) -> str:
        pass

    def _validate(self, response: str) -> None:
        if not self._validator.validate(response):
            raise NotValidException()


class MistralAiModel(Enum):
    TINY = "mistral-tiny"
    SMALL = "mistral-small"
    MEDIUM = "mistral-medium"


class MistralAi(AbstractAi):

    def __init__(self,
                 temperature: float,
                 validator: AbstractValidator,
                 model: MistralAiModel = None):

        super().__init__(temperature, validator)
        # Set api key
        self.api_key = os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY environment variable is not set.")

        # Set model
        if model is None:
            model = MistralAiModel.SMALL
        elif model is not isinstance(model, MistralAiModel):
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
        if model is not isinstance(model, MistralAiModel):
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
