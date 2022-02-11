from enum import Enum


class ControllerStatus(Enum):
    SUCCESS = 0
    ERROR = 1
    ALREADY_EXISTS = 2
    WRONG_CREDS = 3
    NOT_VERIFIED = 4
