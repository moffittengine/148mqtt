import paho.mqtt.client as mqtt
import argparse
import time
import uuid
import hashlib
import Queue
import threading
from constants import *

class SetQueue:
    def __init__(self):
        self.q = Queue.Queue()
        self.lookup = set()
        self.lock = threading.Lock()

    def enqueue(self, item):
        self.lock.acquire()
        ret = False
        if item not in self.lookup:
            self.q.put(item)
            self.lookup.add(item)
            ret = True
        self.lock.release()
        return ret 

    def dequeue(self):
        item = None
        self.lock.acquire()
        if not self.q.empty():
            item = self.q.get()
            self.lookup.remove(item)
        self.lock.release()
        return item

    def size(self):
        return len(self.lookup)

class Master:
    
    def __init__(self, host, timeout=1):
        self.client = mqtt.Client()
        self.client.connect(host)
        self.client.on_message = self.on_message
        self.master_id = '0x{0:012x}'.format(uuid.getnode())
        #self.master_id = str(hex(uuid.getnode()))

        self.status_lock = threading.Lock()
        self.slave_statuses = {}
        self.slave_job = {}
        self.ready_slaves = SetQueue()

        self.aggregate_running = {} # slaves running
        self.aggregate_lock = {}    # locks for each work id
        self.aggregate = {}         # aggregate return value

        self.client.subscribe([
            (MASTER_TOPIC, 0),
        ])
        self.client.loop_start()
        self.broadcast("%s%s" % (self.master_id, GET_ACTIVE_CLIENTS))
        time.sleep(2*timeout) # fixed time to wait for messages to come back

    def broadcast(self, message):
        self.client.publish(BROADCAST_TOPIC, message)

    # low, high inclusive
    def range_sum(self, low, high):
        op = OPERATIONS_MAP["SUM"]
        work_id = uuid.uuid4()
        self.aggregate_running[work_id] = 0
        self.aggregate[work_id] = 0
        self.aggregate_lock[work_id] = threading.Lock()
        r = range(low, high + 1)
        tasks = Queue.Queue()
        if high - low > self.ready_slaves.size():
            i = 0
            inc = (high - low + 2)/self.ready_slaves.size()
            while (i < high - low + 1):
                r2 = r[i:i+inc]
                i += inc
                msg = "%s%s" % (op, ",".join(map(str,r2)))
                tasks.put(msg)

        while not tasks.empty():
            worker_id = self.ready_slaves.dequeue()
            if worker_id is not None:
                msg = tasks.get()
                self.status_lock.acquire()
                self.slave_statuses[worker_id] = PENDING_STATUS
                self.slave_job[worker_id] = work_id
                self.aggregate_running[work_id] += 1
                self.status_lock.release()
                self.distribute(worker_id, "%s%s" % (self.master_id, msg))

        while (True):
            self.aggregate_lock[work_id].acquire()
            if (self.aggregate_running[work_id] == 0):
                break
            self.aggregate_lock[work_id].release()

        print "Finished sum of integers from %d to %d inclusive" % (low, high)
        print "Output after distributing work: %d" % self.aggregate[work_id]
        print "Expected output: " + str(sum(r))


    def distribute(self, worker_id, message):
        self.client.publish("/".join([SLAVE_TOPIC, worker_id]), message)

    def on_message(self, client, userdata, message):
        payload = str(message.payload.decode("utf-8"))
        worker_id = payload[0:CLIENT_ID_LENGTH]
        operation = payload[CLIENT_ID_LENGTH:PAYLOAD_START]
        message = payload[PAYLOAD_START:]

        if operation == GET_ACTIVE_CLIENTS:
            self.ready_slaves.enqueue(worker_id)
        elif operation == ACCEPT_MESSAGE_RESPONSE:
            self.status_lock.acquire()
            self.slave_statuses[worker_id] = BUSY_STATUS
            self.status_lock.release()
        else:
            self.status_lock.acquire()
            if worker_id in self.slave_statuses:
                job = self.slave_job[worker_id]
                print "Message recieved from worker"
                print "Worker id: " + worker_id
                print "Worker operation: " + operation
                print "Worker message: " + message
                print "\n"
                self.aggregate_lock[job].acquire()
                self.aggregate_running[job] -= 1
                if operation == OPERATIONS_MAP["SUM"]:
                    self.aggregate[job] += int(message)
                self.aggregate_lock[job].release()
                del self.slave_statuses[worker_id]
                del self.slave_job[worker_id]
            self.status_lock.release()
            self.ready_slaves.enqueue(worker_id)


def parse_args():
    parser = argparse.ArgumentParser(description="Distributed Calculator Master")
    parser.add_argument("--hostname", required=True, help="Hostname")
    return parser.parse_args()


def main(cmds):
    host = cmds.hostname if cmds.hostname != None else LOCALHOST
    m = Master(host)
    m.range_sum(10, 1000)


if __name__ == "__main__":
    cmds = parse_args()
    main(cmds)
