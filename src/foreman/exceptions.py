__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
"""

import logging


class ForbiddenException(Exception):
    pass

class NotFoundException(Exception):
    pass

class ActionNotSupportedException(Exception):
    pass

class InvalidActionException(Exception):
    pass
