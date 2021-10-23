import random
import string


def random_lower_string(length=32) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_email(length=10) -> str:
    return f"{random_lower_string(length)}@{random_lower_string(length)}.com"
