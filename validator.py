from abc import ABC


class Validator(ABC):

    def validate(self, txt: str) -> bool:
        raise NotImplementedError()


class NotValidException(Exception):
    def __init__(self, message="The provided input is not valid"):
        super().__init__(message)
