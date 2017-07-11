#!/usr/bin/python

from threading import Thread, Lock
import time

class BroadcastThread(Thread):
    def __init__(self, threadId, topic, subs_lock):
        Thread.__init__(self)
        self.threadId = threadId
        self.topic = topic
        self.subs_lock = subs_lock
    def run(self):
        self.topic.incr_counter()
        while self.topic.has_message():
            subscribers = self.topic.get_subscribers()
            if len(subscribers) > 0:
                message = self.topic.get_message()
                self.subs_lock.acquire()
                for subs_name in subscribers:
                    subs = subscribers[subs_name]
                    subs.read_handler(message)
                    time.sleep(0.1)
                self.subs_lock.release()


class Topic:
    '''Topic class
    '''
    def __init__(self, topic_name='Topic', queue_size=100):
        self.queue_size = queue_size
        self.queue = []
        self.subscribers = {}
        self.name = topic_name
        self.counter = 0
        self.queue_lock = Lock()
        self.subs_lock = Lock()
        self.broadcast_thread = BroadcastThread('broadcast-thread', self, self.subs_lock)
        self.broadcast_thread.start()   

    def publish(self, message):
        self.queue.append(message)
        self.broadcast()

    def get_message(self):
        return self.queue.pop(0)

    def broadcast(self):
        if self.broadcast_thread.isAlive():
            return
        else:
            self.broadcast_thread = BroadcastThread('broadcast-thread', self, self.subs_lock)
            self.broadcast_thread.start()

    def subscribe(self, subscriber):
        self.subs_lock.acquire()
        self.subscribers[subscriber.get_name()] = subscriber
        self.subs_lock.release()

    def get_subscribers(self):
        return self.subscribers

    def has_message(self):
        if len(self.queue) > 0:
            return True
        else:
            return False

    def get_counter(self):
        return self.counter

    def incr_counter(self):
        self.counter += 1



