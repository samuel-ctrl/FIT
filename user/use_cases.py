import re


class PhoneNumberValidator:
    """It will validate the phone number."""

    def __init__(self, phone_number):
        self.phone_number = phone_number

    def is_valid(self):
        # Regular expression pattern to validate phone numbers in a simple format.
        # You may adjust the pattern based on your specific requirements.
        pattern = r"^\+?(\d{12})\Z"

        if not re.match(pattern, self.phone_number):
            return False
        return True

