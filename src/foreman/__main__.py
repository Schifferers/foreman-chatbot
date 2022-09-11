__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
"""

from slackbot.client import get_client
from slackbot import args
import logging
import time
import sentry_sdk


logging.info("Initializing Sentry.")
sentry_sdk.init(dsn="https://7f0acdcf494c418aadccf30c5dc45f71@sentry.io/2605676")


logging.info("Starting Foreman Slack bot.")
sc = get_client()
sc.start()
