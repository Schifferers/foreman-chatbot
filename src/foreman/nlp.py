__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
"""

import requests
import os
import logging
import json
from foreman import constants


def get_intent(text:str) -> dict:
    rasa_url = f"{os.environ[constants.RASA_URL]}/model/parse"
    rasa_token = os.environ[constants.RASA_AUTH_TOKEN]

    r = requests.post(rasa_url,
                      headers={
                          'Accept': 'application/json',
                          'Content-type': 'application/json',
                      },
                      params={
                          'token': rasa_token,
                      },
                      data=json.dumps({
                          'text': text,
                      }))
    logging.debug("r: %s", r)

    if r.status_code != 200:
        logging.info("Unexpected response from NLP: %d, %s", r.status_code, r.text)
        return None

    response = r.json()
    logging.debug("response: %d, %s", r.status_code, response)

    entities = {}
    for entity in response['entities']:
        entities[entity['entity']] = entity['value']

    action = {
        'action': response['intent']['name'],
        'entities': entities,
    }
    logging.debug("action: %s", action)

    return action
