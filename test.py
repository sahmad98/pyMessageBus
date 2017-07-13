#!/usr/bin/python

from message_bus import MessageBus
from pubsub import Publisher, Subscriber
from flask import Flask
import time

bus = MessageBus()
bus.add_topic('saleem')

publisher = Publisher('Pub1')
bus.bind('saleem', publisher)

sub1 = Subscriber('Sub1')
sub2 = Subscriber('Sub2')
bus.bind('saleem', sub1)
bus.bind('saleem', sub2)

publisher.publish('Hello Saleem')

for x in xrange(20):
    publisher.publish('Pub1 : %s: Counter ' % (x))

time.sleep(1)
sub3 = Subscriber('Sub3')
bus.bind('saleem', sub3)