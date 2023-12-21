from enum import Enum


class CustomRegex(Enum):
    PHONE_NUMBER = r"^\+?(\d{12})\Z"
    SINGLE_EMAIL = r"^[-!#-\'*+\/-9=?^-~]+(?:\.[-!#-\'*+\/-9=?^-~]+)*@[-!#-\'*+\/-9=?^-~]+(?:\.[-!#-\'*+\/-9=?^-~]+)+$"