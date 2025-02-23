from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Lock
import json

app = Flask(__name__)
socketio = SocketIO(app)
lock = Lock()
drawings = []

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('draw')
def handle_draw(data):
    with lock:
        drawings.append(data)
    socketio.emit('sync', json.dumps(drawings), include_self=False)

@socketio.on('connect')
def handle_connect():
    # Send the current drawing to the new client
    socketio.emit('sync', json.dumps(drawings))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)