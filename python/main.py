from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdef123456'
socketio = SocketIO(app)

@socketio.on('my event')
def handle_message(message):
    print('received message: ' + str(message))

if __name__ == '__main__':
    socketio.run(app)
