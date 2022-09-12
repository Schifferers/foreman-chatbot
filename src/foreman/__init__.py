__author__ = "Paul Schifferer <paul@schifferers.net>"
__version__ = "1.0.2"
"""
"""

import logging
import argparse
from dotenv import load_dotenv


parser = argparse.ArgumentParser(description='Command-line arguments.')
parser.add_argument('--debug', help='output debug messages', action='store_true')
parser.add_argument('--quiet', '-q', help='be quiet', action='store_true')
args = parser.parse_args()
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s %(module)s: %(message)s')
if args.debug:
    logging.getLogger().setLevel(logging.DEBUG)
elif args.quiet:
    logging.getLogger().setLevel(logging.WARNING)


load_dotenv()
