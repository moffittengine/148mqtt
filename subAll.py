import paho.mqtt.client as mqtt
import argparse
import time
import uuid
import hashlib
import Queue
import threading
from constants import *


def parse_args():
    parser = argparse.ArgumentParser(description="Distributed Calculator Master")
    parser.add_argument("--hostname", required=True, help="Hostname")
    return parser.parse_args()


def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    client_id = payload[0:UUID_LENGTH]
    operation = payload[UUID_LENGTH:PAYLOAD_START]
    msg = payload[PAYLOAD_START:]
    print(
        "--------------------------------\n" \
        "Topic: %s\n" \
        "Client Id: %s\n" \
        "Operation: %s\n" \
        "Message: %s\n" \
        "--------------------------------\n" \
    % (message.topic, client_id, operation, msg))

def main(cmds):
    host = cmds.hostname if cmds.hostname != None else LOCALHOST
    
    client = mqtt.Client()
    client.connect(host)
    client.on_message = on_message
    client.subscribe('#')
    while True:
        client.loop()


if __name__ == "__main__":
    cmds = parse_args()
    main(cmds)
