import os
from enum import Enum

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

from utils.validator import AbstractValidator
from .abstract import AbstractAi, Prompt


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

        if prompt.system_prompt is not None:
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

