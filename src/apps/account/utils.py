import re


def check_phone_number(number):
    return bool(re.fullmatch(r"^09\d{9}$", number))
