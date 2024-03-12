from abc import ABC, abstractmethod
from typing import TypeVar, Generic, get_type_hints, override

T = TypeVar("T")


class AbstractValidator(Generic[T], ABC):
    _expected_type = None

    @override
    def __init_subclass__(cls, **kwargs):
        """
        Override to Define _expected_type based on input_value attribute in _validate overridden method.
        """

        super().__init_subclass__(**kwargs)

        hints = get_type_hints(cls._validate)

        if 'input_value' in hints:  # Try to retrieve input_value attribute type
            cls._expected_type = hints['input_value']

        else:
            raise TypeError("Cannot infer 'input_value' type for {}".format(cls.__name__))

    def __init__(self):
        super().__init__()

    def validate(self, input_value: T, raise_error: bool = False) -> bool:
        """
        Validate the given input_value.
        :param input_value: Input value to validate
        :param raise_error: Optional flag. Set to True to raise a NotValidException, set to False otherwise.
        :return: Return True if valid, False otherwise
        """

        if not isinstance(input_value, self._expected_type):
            raise NotValidException(f"input value of Validator must be a {self._expected_type}")

        result = self._validate(input_value)

        if raise_error and not result:
            raise NotValidException(f"The input is not valid. input={input_value}")

        return result

    @staticmethod
    @abstractmethod
    def _validate(input_value: T) -> bool:
        pass


class NotValidException(Exception):
    """Custom exception class for Validator Exceptions."""
    def __init__(self, message="The provided input is not valid"):
        super().__init__(message)
