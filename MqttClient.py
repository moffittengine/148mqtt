import paho.mqtt.client as mqtt
import time

class MqttClient:

    def __init__(self, name, host, topic, callback):
        self.host  = host
        self.topic = topic
        self.blocking_run = True
        self.callback = self.on_message if callback == None else callback
        self.client = mqtt.Client() if name == None else mqtt.Client(name)
        self.client.on_message = self.callback

    def on_message(self, client, userdata, message):
        print("Topic: %s" % message.topic)
        print("Message: \n%s\n" % str(message.payload.decode("utf-8")))

    def connect(self):
        self.client.connect(self.host)

    def disconnect(self):
        self.client.disconnect()

    def subscribe(self):
        self.client.subscribe(self.topic)

    def subscribe_unblocking(self):
        self.client.subscribe(self.topic)
        self.client.loop_start()    #start the loop

    def subscribe_blocking(self):
        self.client.subscribe(self.topic)
        self.blocking_run = True
        while(self.blocking_run):
            self.client.loop()

    def subscribe_unblock(self):
        self.blocking_run = False

    def publish(self, message):
        self.client.publish(self.topic, message)

    def publish_topic(self, topic, message):
        self.client.publish(topic, message)

    def loop(self):
        self.client.loop()

    def get_id():
        return self.client_id
