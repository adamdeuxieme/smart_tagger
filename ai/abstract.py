from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Union

from utils import AbstractValidator


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


class AiEnum(Enum):
    MISTRAL = "--mistralai"
    CHATGPT = "--chatgpt"


@dataclass
class Prompt:
    user_prompt: str
    system_prompt: Union[str, None] = None


class AbstractPromptProvider(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def construct_prompt(self, *args) -> Prompt:
        pass
