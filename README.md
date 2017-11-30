# 148mqtt

This program is for the CMPE148 Raspberry Pi project. 

The goal of this project is to bring up a Raspberry Pi and implement a networking function.
For this project, the MQTT protocol was selected. This uses publish and subscribe methods to pass messages over the network. 


There are four (4) main files:


mqttTimer.py

This program will subscribe and publish to the same server/topic. After the connection is established and the subscriber is setup, the publisher sends a message and saves a timestamp. When the message is received by the subscriber after the broker relays it, another timestamp is taken. The difference in time denotes the round trip time. This is averaged over N itterations and output to the console. This program's primary use is for testing network connectivity.


master.py

This program communicates with the slaves to partition tasks and give the tasks to the slaves, then recombines them into aggregated data. Currently, the master only sends an summation request to the slaves.


slave.py

This program allows communication with the master on a client so that the master can assign tasks to it.


subAll.py

This program will subscribe to all topics on a broker, and display every message being passed through it over MQTT.

