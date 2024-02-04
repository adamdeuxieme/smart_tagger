from abc import ABC

from validator import Validator, NotValidException


class AiAbstract(ABC):

    def __init__(self, validator: Validator):
        self._temperature = 0.0
        self._validator = validator

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, new_value: float):
        if new_value < 0.0 or new_value > 1.0:
            raise ValueError("Temperature must be between 0.0 and 1.0.")
        self._temperature = new_value

    @property
    def validator(self):
        return self._validator

    @validator.setter
    def validator(self, validator: Validator):
        if validator is not isinstance(validator, Validator):
            raise ValueError("Validator is not an instance of Validator.")

    def ask(self, prompt: str):
        raise NotImplementedError("Please implement.")

    def _validate(self, response: str):
        if not self._validator.validate(response):
            raise NotValidException()
