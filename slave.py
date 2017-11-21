import paho.mqtt.client as mqtt
import argparse
import time
import uuid
import hashlib
from constants import *

_WORKING = False

class Slave:
    
    def __init__(self, host):
        self.client = mqtt.Client()
        self.client.connect(host)
        self.worker_id = str(uuid.uuid4())
        self.client.on_message = self.on_message
        self.topic = "/".join([SLAVE_TOPIC, self.worker_id])
        print "got here1"
        self.client.subscribe([
            (self.topic, 0), # slave topic
            (BROADCAST_TOPIC, 0)
        ])
        print "got here2"
        while(True):
            self.client.loop()
        #self.client.loop_start()
    
    #def send_heartbeat(self, uuid):
    #    self.client.publish(HEARTBEAT_TOPIC, "%s,%s" %
    #        (uuid, BUSY_STATUS if _WORKING else READY_STATUS))

    def on_message(self, client, userdata, message):
        print "got message"
        payload = message.payload.decode("utf-8")
        if (message.topic == self.topic):
            self.accept_message()
            self.work(payload)
        elif (message.topic == BROADCAST_TOPIC):
            self.broadcast_handler(payload)

    def send_master(self, msg):
        self.client.publish(MASTER_TOPIC, "%s%s" % (self.worker_id, msg))

    def broadcast_handler(self, message):
        # currently just tell master you're alive
        self.send_master(GET_ACTIVE_CLIENTS)

    """ Tell the master that the slave has recieved the message """
    def accept_message(self):
        self.send_master(ACCEPT_MESSAGE_RESPONSE)

    def work(self, message, sleeptime=0):
        print "recieved work item: \n%s\n\n" % message
        start_time = time.time()
        key = message[0:UUID_LENGTH]
        ret = ""
        if key in OPERATIONS_MAP:
            func = OPERATIONS_MAP[key]
            msg = message[UUID_LENGTH:]
            if func == "SUM":
                s = self.func_sum(msg)
                ret = "%s%s" % (key, str(s))
                print "s: " + str(s)
            elif func == "PRODUCT":
                ret = "%s%s" % (key, str(self.func_product(msg)))

        while (time.time() - start_time < sleeptime):
            time.sleep(0.1) # don't kill all cpu cycles

        self.send_master(ret)

    def func_sum(self, message):
        return sum(map(int, message.split(",")))

    def func_product(self, message):
        arr = map(int, message.split(","))
        prod = 1
        for i in arr:
            prod *= i
        return prod


def parse_args():
    parser = argparse.ArgumentParser(description="Distributed Calculator Worker")
    parser.add_argument("--hostname", required=True, help="Hostname")
    return parser.parse_args()


def main(cmds):
    host = cmds.hostname if cmds.hostname != None else LOCALHOST
    s = Slave(host)


if __name__ == "__main__":
    cmds = parse_args()
    main(cmds)
