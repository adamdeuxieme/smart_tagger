from abc import ABC, abstractmethod


class Validator(ABC):

    @abstractmethod
    def validate(self, txt: str) -> bool:
        pass


class NotValidException(Exception):
    def __init__(self, message="The provided input is not valid"):
        super().__init__(message)
