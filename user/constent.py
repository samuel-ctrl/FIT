from enum import Enum


class CustomRegex(Enum):
    PHONE_NUMBER = r"^\+?(\d{12})\Z"
