import paho.mqtt.client as paho
import datetime as dt
import time
from mqtt import mqtt

############ Setup ###############
hostLocal = 'localhost'
hostWeb   = 'test.mosquitto.org'

loopCount = 5
topic     = '/test148/tripTime'

totals  = 0
counter = 0

def callback(client, userdata, message): 
    elapsed(dt.datetime.now().microsecond);

def elapsed(end):
    global start, totals, trip, counter
    trip = (end-start)/1000
    if(trip<0) : trip = trip + 1000
    totals = totals + trip
    counter +=1

def outTime():
    global trip, counter
    print("Time average for %d message(s)" %counter)
    print("Round Trip: %3.2f ms" %(totals/counter)   )
    print("One way   : %3.2f ms" %(totals/(2*counter)))
############ END Setup ###############



############ Broker Test ###############
def testLocal(host, topic, loopCount):
    global totals, counter, start
    totals  = 0
    counter = 0
    # Setup Subscriber
    listen = mqtt('a', host, topic, 1, callback)
    time.sleep(1)

    # Setup Publisher
    send = mqtt('b', host, topic, 0, None)

    # Send N messages and get the Average
    for i in range(0, loopCount):
        time.sleep(2)
        start = dt.datetime.now().microsecond   
        send.publish("SendMessage: %d" %i)

    time.sleep(1)
    outTime()
    listen.disconnect()
############ END Broker Test ###############



if __name__ == '__main__':
    print("\n*** Test Local Server Trip Time ***")
    testLocal(hostLocal, topic, loopCount)
    print("\n**** Test Web Server Trip Time ****")
    testLocal(hostWeb  , topic, loopCount)

