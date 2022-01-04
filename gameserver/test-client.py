#!/usr/bin/env python3
import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.on("stuff")
def _stuff(data):
    print('message received with')
    print(locals())

# @sio.event
# def stuff(data):
#     print('message received with')
#     print(locals())
#     #sio.emit('my response', {'response': 'my response'})

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://localhost:8000')
sio.emit("test event", {"lol": "cat"})
sio.wait()