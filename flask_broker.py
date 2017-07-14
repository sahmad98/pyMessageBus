#!/usr/bin/env python

from flask import Flask, request, jsonify
from message_bus import MessageBus

__bus = MessageBus()
app = Flask(__name__)

@app.route('/')
def ping():
    response = {}
    response['status'] = 'success'
    response['type'] = 'ping'
    return jsonify(response)

@app.route('/create_topic', methods=['GET'])
def create_broker():
    response = {}
    response['status'] = 'unknown'
    if request.method == 'GET':
        try:
            name = request.args.get('name')
            if name is None:
                raise KeyError('name query parameter not found')
            __bus.add_topic(name)
            response['status'] = 'success'
        except KeyError as error:
            response['status'] = 'error'
            response['message'] = str(error)
    return jsonify(response)

@app.route('/get_topics', methods=['GET'])
def get_topics():
    response = {}
    response['status'] = 'unknown'
    if request.method == 'GET':
        response['topics'] = __bus.get_available_topics()
        response['status'] = 'success'
    return jsonify(response)

@app.route('/publish', methods=['POST'])
def publish():
    response = {}
    response['status'] = 'unknown'
    if request.method == 'POST':
        json = request.json
        topic_name = json['topic']
        message = json['message']
        topic = __bus.get_topic(topic_name)
        if topic is None:
            response['status'] = 'error'
            response['message'] = 'topic: %s missing' % topic_name
        else:
            topic.write(message)
            response['status'] = 'success'
    return jsonify(response)

@app.route('/read', methods=['GET'])
def read():
    response = {}
    response['status'] = 'unknown'
    topic_name = request.args.get('topic')
    if topic_name is None:
        response['status'] = 'error'
        response['message'] = 'topic query paramter missing'
        return jsonify(response)
    topic = __bus.get_topic(topic_name)
    if topic is None:
        response['status'] = 'error'
        response['message'] = 'invalid topic name, missing on bus'
        return jsonify(response)
    message = topic.read()
    response['status'] = 'success'
    response['message'] = message
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)