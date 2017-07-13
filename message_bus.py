#!/usr/bin/env python

from topic import Topic

class MessageBus:
    '''MessageBus class
    '''
    def __init__(self):
        self.message_queue = {}
    
    def add_topic(self, topic_name, queue_size=100):
        self.message_queue[topic_name] = Topic(queue_size)
        return self.message_queue[topic_name]

    def get_topic(self, topic_name):
        return self.message_queue[topic_name]

    def bind(self, topic_name, pubsub):
        topic = self.get_topic(topic_name)
        pubsub.bind_topic(topic)

