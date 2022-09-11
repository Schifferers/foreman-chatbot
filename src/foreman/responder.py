__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
"""

import logging


def respond(client:object, data:dict, **kwargs):
    try:
        channel_id = data.get('channel')
        if channel_id is None:
            logging.warning("No channel_id found in data.")
            return

        thread_ts = data.get('ts')

        client.chat_postMessage(channel=channel_id,
                                # thread_ts=thread_ts,
                                # reply_broadcast=True,
                                **kwargs)
    except:
        logging.exception("Exception while trying to respond to Slack message:")
