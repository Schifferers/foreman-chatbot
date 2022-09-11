__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
"""

import logging
import os
import slack
from slackbot.dispatcher import dispatch_action
from slackbot.process import assemble_text, process_text
from slackbot.responder import respond


my_info = {}


def get_client(token:str = os.environ['SLACK_API_TOKEN']):
    logging.info("Creating Slack client.")
    client = slack.RTMClient(token=token)
    logging.debug("client: %s", client)
    return client


@slack.RTMClient.run_on(event='open')
def handle_open(**payload):
    logging.debug("payload: %s", payload)
    global my_info
    my_info = payload.get('data', {}).get('self', {})
    logging.info("Me: %s", my_info)


@slack.RTMClient.run_on(event='message')
def handle_message(**payload):
    logging.debug("payload: %s", payload)

    try:
        data = payload['data']
        user = data.get('user')
        logging.debug("user: %s", user)

        if not user:
            logging.debug("Incoming message has no user; ignoring.")
            return

        if user == my_info.get('id'):
            logging.debug("Incoming message is from me; ignoring.")
            return

        # web_client = payload['web_client']
        # rtm_client = payload['rtm_client']

        text = assemble_text(data)
        logging.debug("assembled text: %s", text)

        action = process_text(text)
        dispatch_action(payload, action, user)
    except:
        logging.exception("Exception while trying to process Slack message:")
        respond(payload.get('web_client'),
                payload.get('data'),
                "Sorry, my bits got twisted on that last message.")
