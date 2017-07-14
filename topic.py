#!/usr/bin/python

from threading import Thread, Lock
import time

class BroadcastThread(Thread):
    '''BroadcastThread represents a broadcaster for
    messages in topic queue. It is a derived class 
    of Thread.
    run() method is executed till the messeage queue
    becomes empty and each messge in queue us sent 
    to each subscriber.
    '''
    def __init__(self, threadId, topic, subs_lock):
        '''Constructor
        @Arguments
        threadId  - Name of the broadcast thread
        topic     - Topic form which this broadcast thread
                     will take message
        subs_lock - A lock for subscribers map. Number of
                    subscribers can increase during iterat-
                    ion over map
        '''
        Thread.__init__(self)
        self.threadId = threadId
        self.topic = topic
        self.subs_lock = subs_lock

    def run(self):
        '''@Overridden run() method
        Checks the topic for any queued message, If it finds
        one, send it to all subscribers till the message
        queue becomes empty. A new thread should be launched
        if the previous thread is terminated.
        '''
        self.topic.incr_counter()
        while self.topic.has_message() and len(self.topic.subscribers) > 0:
            self.subs_lock.acquire()
            subscribers = self.topic.get_subscribers()
            message = self.topic.read()
            for subs_name in subscribers:
                subs = subscribers[subs_name]
                subs.read_handler(message)
            self.subs_lock.release()
            time.sleep(0.1)

class Topic:
    '''Topic class represents a topic in message bus. Publishers
    can write on this topic and subscribers can read from this
    topic. There can be multiple publishers/subscribers to the
    same topic.
    '''
    def __init__(self, topic_name='Topic', queue_size=100):
        '''Constructor
        @Arguments
        topic_name - Name of the topic
        queue_size - Max number of messages in queue [default=100]
        '''
        self.queue_size = queue_size
        self.queue = []
        # Map of subsribers name and Subscriber object
        self.subscribers = {}
        self.name = topic_name
        # TODO: Remove this counter
        self.counter = 0
        # Lock for queue and subscribers map sync
        self.queue_lock = Lock()
        self.subs_lock = Lock()
        self.broadcast_thread = None

    def write(self, message):
        '''@Arguments
        message - string message to store in message queue
        write method is used to put message in the message
        queue.
        '''
        self.queue.append(message)
        self.broadcast()
        return True

    def read(self):
        '''@Returns - message from message queue
        read method returns one message from message queue
        if available. Queue might be empty so always use 
        has_message() before calling read.
        '''
        if len(self.queue) > 0:
            return self.queue.pop(0)
        else:
            return None

    def broadcast(self):
        '''broadcast method starts new thread broadcaster to
        start sending messages to subscribers. If there is any
        active broadcast thread available then it uses that
        other wise creats a new broadcast thread.
        '''
        if self.broadcast_thread != None and self.broadcast_thread.isAlive():
            return
        else:
            self.broadcast_thread = BroadcastThread('broadcast-thread', self, self.subs_lock)
            self.broadcast_thread.start()

    def subscribe(self, subscriber):
        '''@Argument
        subscriber - A Subscriber object which will listen to
                     this topic
        subscribe method is used to register subscribers to this
        topic
        '''
        self.subs_lock.acquire()
        self.subscribers[subscriber.get_name()] = subscriber
        self.subs_lock.release()
        self.broadcast()

    def unsubscribe(self, subscriber):
        # TODO: Implement unsubscribe
        pass

    def get_subscribers(self):
        '''@Returns - A map of subscribers currently registered
        get_subscribers method is used to get a map of currently
        registered subscribers to this topic. A name to object
        mapping is stored in map
        '''
        return self.subscribers

    def has_message(self):
        '''@Returns - boolean 
        Returns true if a message is availabe in message queue
        '''
        if len(self.queue) > 0:
            return True
        else:
            return False

    def get_counter(self):
        return self.counter

    def incr_counter(self):
        self.counter += 1


