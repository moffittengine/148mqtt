# 148mqtt

This program is for the CMPE148 Raspberry Pi project. 

The goal of this project is to bring up a Raspberry Pi and implement a networking function.
For this project, the MQTT protocol was selected. This uses publish and subscribe methods to pass messages over the network. 

This program will subscribe and publish to the same server/topic. After the connection is established and the subscriber is setup, the publisher sends a message and saves a timestamp. When the message is received by the subscriber after the broker relays it, another timestamp is taken. The difference in time denotes the round trip time. This is averaged over N itterations and output to the console.

This process is repeated for both the local mosquitto broker and the test server online. Any additional servers could be tested by changing the host at the top of mqttTest.py


There are two (2) main files 
-mqtt.py 
	-This file holds the main calls and processes
	-If ran alone, local broker must be running
		A single message will be sent and received

-mqttTest.py
	-This file uses the mqtt.py mqtt class
	-Unchanged, running this file will test both local broker and the 
		test.mosquitto.org web broker server
	-N calls will be made and timed to each server
	-The average of those round trips will be output to console






