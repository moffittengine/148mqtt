import paho.mqtt.client as mqtt
import argparse
import time

from MqttClient import MqttClient
from constants import *

_LOOP = True

def parse_args():
    parser = argparse.ArgumentParser(description="MQTT Timer")
    parser.add_argument("-n", "--number", required=True, type=int, help="Number of trials")
    parser.add_argument("--hostname", required=True, help="Hostname")
    return parser.parse_args()

def on_message(client, userdata, message):
    global _LOOP
    _LOOP = False

def time_message(client):
    global _LOOP
    _LOOP = True
    client.connect()
    client.subscribe()
    start = time.time()
    client.publish("hello")
    while _LOOP:
        client.loop()
    end = time.time()
    client.disconnect()
    return end - start

def main(cmds):
    host = cmds.hostname if cmds.hostname != None else LOCALHOST
    client = MqttClient(None, host, SUBSCRIBE_TOPIC, on_message)
    avg = 0
    for i in xrange(cmds.number):
        avg += time_message(client)
    print("%.7f ms average for %d trials on host \'%s'" % 
        ((avg/cmds.number)*1000, cmds.number, host))

if __name__ == "__main__":
    cmds = parse_args()
    main(cmds)
