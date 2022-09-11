__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
"""

import logging
from slackbot.nlp import get_intent


def process_text(text:str):
    logging.debug("text: %s", text)

    action = get_intent(text)
    # TODO?

    return action


def assemble_text(payload:dict) -> str:
    logging.debug("payload: %s", payload)

    text = ""

    blocks = payload.get('blocks', [])
    for block in blocks:
        logging.debug("block: %s", block)
        block_type = block.get('type', '')
        if block_type == 'rich_text':
            block_elements = block.get('elements', [])
            for bel in block_elements:
                logging.debug("element: %s", bel)
                bel_type = bel.get('type', '')
                if bel_type == 'rich_text_section':
                    section_elements = bel.get('elements', [])
                    for sel in section_elements:
                        sel_type = sel.get('type', '')
                        if sel_type == 'text':
                            text += sel.get('text', '')
                        else:
                            logging.warning("Unknown section element type: %s", sel_type)
                else:
                    logging.warning("Unknown block element type: %s", bel_type)
        else:
            logging.warning("Unknown block type: %s", block_type)

    return text
