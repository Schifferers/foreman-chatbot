__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
"""

from slackbot.client import get_client
from slackbot import args
import logging
import time
import sentry_sdk
import os
from foreman import constants


logging.info("Initializing Sentry.")
sentry_sdk.init(dsn=os.environ[constants.SENTRY_DSN])


logging.info("Starting Foreman Slack bot.")
sc = get_client()
sc.start()
