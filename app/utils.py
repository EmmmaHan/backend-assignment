import string
import random

def generate_random_numbers(length):
    return ''.join(random.choice(string.digits) for _ in range(length))


def generate_random_string(length):
    return ''.join(random.choice(string.digits + string.ascii_uppercase) for _ in range(length))
