__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
"""

import random


def randhex(size=1):
    result = []
    for i in range(size):
        result.append(str(random.choice("0123456789ABCDEF")) + str(random.choice("0123456789ABCDEF")))
    return "".join(result)
