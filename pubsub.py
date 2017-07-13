#!/usr/bin/env python

class Publisher:
    '''Publisher Class
    '''
    def __init__(self, name='Publisher'):
        self.topic = None
        self.name = name

    def publish(self, message):
        if self.topic != None:
            self.topic.publish(message) 
    
    def get_name(self):
        return self.name

    def bind_topic(self, topic):
        self.topic = topic
    
    def unbind_topic(self, topic):
        self.topic = None

class Subscriber:
    '''Subscriber Class
    '''
    def __init__(self, name='Subscriber'):
        self.topic = None
        self.name = name
    
    def read_handler(self, message):
        print '%s: %s' % (self.name, message)

    def get_name(self):
        return self.name

    def bind_topic(self, topic):
        self.topic = topic
        self.topic.subscribe(self)

    def unbind_topic(self):
        # TODO: First unsubscribe
        self.topic = None