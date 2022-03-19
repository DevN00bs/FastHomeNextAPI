from enum import Enum


class ControllerStatus(Enum):
    SUCCESS = 0
    ERROR = 1
    ALREADY_EXISTS = 2
    WRONG_CREDS = 3
    NOT_VERIFIED = 4
    INVALID_LINK = 5
    DOES_NOT_EXISTS = 6
    UNAUTHORIZED = 7
    NOT_AN_IMAGE = 8
    NOT_AVAILABLE = 9
