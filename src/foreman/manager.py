__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
"""

import logging
import requests
import os
import json
from foreman.exceptions import ForbiddenException, NotFoundException
from foreman import constants


def _handle_response(response):
    logging.debug("response: %s", response)

    if response.status_code == 403:
        raise ForbiddenException
    if response.status_code == 404:
        raise NotFoundException


def request_server(server_id:str, user:str) -> dict:
    logging.debug("server_id: %s, user: %s", server_id, user)

    url = f"{os.environ[constants.MANAGER_URL]}/api/v1/servers/{server_id}"

    r = requests.get(url,
                      headers={
                          'Authorization': f"Bearer {os.environ[constants.MANAGER_AUTH_TOKEN]}",
                          'Accept': 'application/json',
                          'X-User-ID': user,
                      },
                      params={
                      })
    logging.debug("response: %d, %s", r.status_code, r.text)
    _handle_response(r)

    # TODO

    return r.json()


def request_list(user:str):
    logging.debug("user: %s", user)

    url = f"{os.environ[constants.MANAGER_URL]}/api/v1/servers"

    r = requests.get(url,
                      headers={
                          'Authorization': f"Bearer {os.environ[constants.MANAGER_AUTH_TOKEN]}",
                          'Accept': 'application/json',
                          'X-User-ID': user,
                      },
                      params={
                      })
    logging.debug("response: %d, %s", r.status_code, r.text)
    _handle_response(r)

    # TODO

    return r.json()


def submit_action(action:dict, user:str):
    logging.debug("action: %s, user: %s", action, user)

    server_id = action.get('entities', {}).get('server_id')
    if server_id is None:
        raise InvalidActionException
    url = f"{os.environ[constants.MANAGER_URL]}/api/v1/servers/{server_id}/action"

    body = {
        'action': action['action'],
        **action['entities'],
    }

    r = requests.post(url,
                      headers={
                          'Authorization': f"Bearer {os.environ[constants.MANAGER_AUTH_TOKEN]}",
                          'Content-type': 'application/json',
                          'X-User-ID': user,
                      },
                      data=json.dumps(body))
    logging.debug("response: %d, %s", r.status_code, r.text)
    _handle_response(r)

    # TODO

    return r.json()
