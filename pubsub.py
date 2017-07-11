#!/usr/bin/env python

class Publisher:
    '''Publisher Class
    '''
    def __init__(self, topic, name='Publisher'):
        self.topic = topic
        self.name = name

    def publish(self, message):
        self.topic.publish(message) 
    
    def get_name(self):
        return self.name

class Subscriber:
    '''Subscriber Class
    '''
    def __init__(self, topic, name='Subscriber'):
        self.topic = topic
        self.name = name
        self.topic.subscribe(self)  

    def read_handler(self, message):
        print '%s: %s' % (self.name, message)

    def get_name(self):
        return self.name