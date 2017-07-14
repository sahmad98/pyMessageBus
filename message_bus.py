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
        try:
            return self.message_queue[topic_name]
        except KeyError:
            return None

    def bind(self, topic_name, pubsub):
        topic = self.get_topic(topic_name)
        pubsub.bind_topic(topic)

    def get_available_topics(self):
        topics = []
        for key in self.message_queue:
            topics.append(key)
        return topics

    def remove_topic(self, name):
        result = {}
        for key in self.message_queue:
            if key != name:
                result[key] = self.message_queue[key]

