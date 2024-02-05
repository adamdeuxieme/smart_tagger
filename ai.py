from abc import ABC, abstractmethod

from prompt_provider import Prompt
from validator import Validator, NotValidException


class AiAbstract(ABC):

    def __init__(self, validator: Validator):
        self._temperature = 0.0
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
    def validator(self) -> Validator:
        return self._validator

    @validator.setter
    def validator(self, validator: Validator) -> None:
        if validator is not isinstance(validator, Validator):
            raise ValueError("Validator is not an instance of Validator.")

    def compute(self, prompt: Prompt) -> str:
        value_computed = self._compute(prompt)
        self._validator.validate(value_computed)
        return value_computed

    @abstractmethod
    def _compute(self, prompt: Prompt) -> str:
        pass

    def _validate(self, response: str) -> None:
        if not self._validator.validate(response):
            raise NotValidException()
