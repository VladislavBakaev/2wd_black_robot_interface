from flask import Flask
from flask_sockets import Sockets
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
import gevent

app = Flask(__name__)
sockets = Sockets(app)

from web_socket_control_app.utils import update_vel, action_feedback_manager

geventOpt = {'GATEWAY_INTERFACE': 'CGI/1.1',
                'SCRIPT_NAME': '',
                'wsgi.version': (1, 0),
                'wsgi.multithread': True, # XXX: Aren't we really, though?
                'wsgi.multiprocess': True,
                'wsgi.run_once': False}

@sockets.route('/ws/joy', websocket=True)
def echo_socket(ws):
    while not ws.closed:
        message = ws.receive()
        gevent.sleep(0)
        if message:          
            update_vel(message)
        if(ws.closed):
            print('close connect')

@sockets.route('/ws/action_feedback', websocket=True)
def action_feedback(ws):
    while not ws.closed:
        ws.send(action_feedback_manager.get_feedback())
        gevent.sleep(1/action_feedback_manager.rate)


def create_app():
    http_server = WSGIServer(('',5000), app, handler_class=WebSocketHandler, environ=geventOpt)
    return http_server
