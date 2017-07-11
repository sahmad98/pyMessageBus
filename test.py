#!/usr/bin/python

from message_bus import MessageBus
from pubsub import Publisher, Subscriber
from flask import Flask
import time

bus = MessageBus()
topic = bus.add_topic('saleem')

publisher = Publisher(topic, 'Pub1')
sub1 = Subscriber(topic, 'Sub1')
sub2 = Subscriber(topic, 'Sub2')

publisher.publish('Hello Saleem')
publisher2 = Publisher(topic, 'Pub2')

for x in xrange(10):
    publisher.publish('Pub1 : %s: Counter %s' % (x, topic.get_counter()))
    publisher2.publish('Pub2')

time.sleep(1)
sub3 = Subscriber(topic, 'Sub3')