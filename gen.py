"""
Generator module for test task with email.

Created on 04.08.2021

@author: Ruslan Dolovanyuk

"""

import random
import string


def get_string(length):
    symbols = string.ascii_letters + string.digits
    return ''.join(random.sample(symbols, length))
