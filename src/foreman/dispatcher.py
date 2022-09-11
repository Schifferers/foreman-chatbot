__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
"""

import logging
from foreman.handlers import *
from foreman.exceptions import ForbiddenException, NotFoundException, ActionNotSupportedException
from foreman.responder import respond


def dispatch_action(message_data:dict, action_data:dict, user:str):
    logging.debug("message_data: %s, action_data: %s, user: %s", message_data, action_data, user)

    method_name = f"handle_{action_data['action']}"
    logging.debug("method_name: %s", method_name)
    possibles = globals().copy()
    possibles.update(locals())
    method = possibles.get(method_name)
    logging.debug("method: %s", method)

    if method is None:
        logging.warning("Could not find method for %s", method_name)
        return

    try:
        method(message_data, action_data, user)
    except ForbiddenException:
        web_client = message_data["web_client"]
        text = "You are not allowed to access that server."
        respond(web_client, message_data['data'], text=text)
    except NotFoundException:
        web_client = message_data["web_client"]
        text = "I couldn't find that server."
        respond(web_client, message_data['data'], text=text)
    except ActionNotSupportedException:
        web_client = message_data["web_client"]
        text = f"It looks like the '{action_data['action']}' action isn't supported for that server."
        respond(web_client, message_data['data'], text=text)
    except:
        logging.exception("Exception while trying to call method %s", method_name)
