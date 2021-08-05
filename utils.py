"""
Utils module for test task with email.

Created on 04.08.2021

@author: Ruslan Dolovanyuk

"""

import random
import string


TEMPLATE_EMAIL = """
Received mail on theme {0} with message: {1}. It contains {2} letters and {3} numbers
"""


def get_string(length):
    symbols = string.ascii_letters + string.digits
    return ''.join(random.sample(symbols, length))


def create_email(emails):
    """Create answer email with all input emails."""
    answer_list = []
    for subject, message in emails.items():
        answer_list.append(TEMPLATE_EMAIL.format(subject, message, count_letters(message), count_digits(message)))
    return '\n'.join(answer_list)


def count_letters(message):
    return sum([1 for s in message if s.isalpha()])


def count_digits(message):
    return sum([1 for s in message if s.isdigit()])
