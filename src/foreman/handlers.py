__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
"""

import logging
from foreman.manager import request_list, submit_action, request_server
from foreman.responder import respond
import time


def _get_server_info(server:dict) -> dict:
    logging.debug("server: %s", server)

    # TODO: fill this in with real data
    info = {
        'status': "TODO",
        'version': "x.2.3",
        'pid': "?",
        'hostname': 'xxx',
        'port': '25565',
    }
    info.update(server.get('info', {}))

    return info


def _build_server_status(server:dict) -> list:
    logging.debug("server: %s", server)

    blocks = []

    name = server['name']
    server_id = server['id']
    server_url = server.get('url', 'http://minecraft:25565/')

    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"<{server_url}|{server_id}>\n:computer: _{name}_",
        },
        # "accessory": {
        #     "type": "image",
        #     "image_url": "http://localhost:5000/static/images/lotr.png",
        #     "alt_text": "server image",
        # },
    })

    info = _get_server_info(server)

    blocks.append({
        "type": "section",
        "block_id": f"{server_id}-fields",
        "fields": [
            {"type": "mrkdwn", "text": f"*Host*\n{info['hostname']}"},
            {"type": "mrkdwn", "text": f"*Port*\n{info['port']}"},
            {"type": "mrkdwn", "text": f"*Version*\n{info['version']}"},
            {"type": "mrkdwn", "text": f"*Status*\n{info['status']}"},
            {"type": "mrkdwn", "text": f"*Process ID*\n{info['pid']}"},
        ],
    })

    action_block = {
        "type": "actions",
        "block_id": f"{server_id}-actions",
        "elements": [],
    }

    for action_name, action_info in server.get('actions', []).items():
        action_block['elements'].append({
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": action_name.capitalize(),
                    "emoji": True,
                },
                "value": action_name,
            })

    blocks.append(action_block)

    return blocks


def handle_start(message: dict, action: dict, user: str):
    logging.debug("message: %s, action: %s, user: %s", message, action, user)

    web_client = message["web_client"]

    # submit action to manager
    submit_action(action, user)

    # TODO: construct response to user
    # TODO: start poller to monitor

    # respond initially
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"<@{user}>: Underway!",
            },
        },
    ]

    respond(web_client, message["data"], blocks=blocks)


def handle_stop(message: dict, action: dict, user: str):
    logging.debug("message: %s, action: %s, user: %s", message, action, user)

    web_client = message["web_client"]

    # submit action to manager
    submit_action(action, user)

    # TODO: construct response to user
    # TODO: start poller to monitor

    # respond initially
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"<@{user}>: Bringin' 'er down!",
            },
        },
    ]

    respond(web_client, message["data"], blocks=blocks)


def handle_reset(message: dict, action: dict, user: str):
    logging.debug("message: %s, action: %s, user: %s", message, action, user)

    web_client = message["web_client"]

    # submit action to manager
    submit_action(action, user)

    # TODO: construct response to user
    # TODO: start poller to monitor

    # respond initially
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"<@{user}>: Time for spring cleaning!",
            },
        },
    ]

    respond(web_client, message["data"], blocks=blocks)


def handle_upgrade(message: dict, action: dict, user: str):
    logging.debug("message: %s, action: %s, user: %s", message, action, user)

    web_client = message["web_client"]

    # submit action to manager
    submit_action(action, user)

    # TODO: construct response to user
    # TODO: start poller to monitor

    # respond initially
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"<@{user}>: Out with the old, in the with new!",
            },
        },
    ]

    respond(web_client, message["data"], blocks=blocks)


def handle_status(message: dict, action: dict, user: str):
    logging.debug("message: %s, action: %s, user: %s", message, action, user)

    web_client = message["web_client"]
    server_id = action.get('entities', {}).get('server_id')
    logging.debug("server_id: %s", server_id)

    if server_id is None:
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"<@{user}>: I couldn't process your request. Try again?",
                },
            },
        ]

        respond(web_client, message["data"], blocks=blocks)
        return

    # get server entry
    server = request_server(server_id, user)
    logging.debug("server: %s", server)

    # construct response
    server_blocks = _build_server_status(server)

    # respond
    web_client = message["web_client"]
    respond(web_client, message["data"], blocks=server_blocks)


def handle_list(message: dict, action: dict, user: str):
    logging.debug("message: %s, action: %s, user: %s", message, action, user)

    data = request_list(user)
    logging.debug("data: %s", data)

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"<@{user}>: Here is the *list of servers* you requested:",
            },
        },
        {"type": "divider"},
    ]

    # build server list as blocks
    for server in data.get('servers', []):
        server_blocks = _build_server_status(server)
        blocks.extend(server_blocks)
        blocks.append({"type": "divider"})

    web_client = message["web_client"]
    respond(web_client, message["data"], blocks=blocks)
