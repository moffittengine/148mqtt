import paho.mqtt.client as paho
import time


class mqtt:
    def __init__(self, name, host, topic, pubSub, callback):
        self.host  = host
        self.topic = topic
        if callback == None : self.callback = self.on_message
        else: self.callback = callback
        self.client = paho.Client(name)#self.topic)
        if(pubSub): self.setSubscriber()

    def on_message(self, client, userdata, message):
        print("message received " ,str(message.payload.decode("utf-8")))
        print("message topic=",message.topic)

    def connect(self):
        self.client.connect(self.host)
    def disconnect(self):
        self.client.disconnect()

    def setSubscriber(self):
        self.client.on_message=self.callback        #attach function to callback
        self.connect()
        self.client.loop_start()    #start the loop
        self.client.subscribe(self.topic)

    def publish(self, message):
        self.connect()
        self.client.publish(self.topic, message)
        self.client.disconnect()



if __name__ == "__main__":
    host   = 'localhost'
    topic  = 'test148'

    # Subscriber Setup
    listen = mqtt('a', host, topic, 1, None)
    time.sleep(1)

    # Publisher Setup
    send = mqtt('b', host, topic, 0, None)

    # Send and disconnect
    send.publish("\n\nTEST MESSAGE HAS BEEN SENT\n\n")
    print("Message Sent")
    time.sleep(4)
    send.disconnect()
