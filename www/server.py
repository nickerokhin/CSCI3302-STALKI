from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, emit
socketio = SocketIO(app)

# initialize Flask
app = Flask(__name__)
@app.route('/')
def index():
    """Serve the index HTML"""
    return render_template('index.html')


def run_server(q):
	app.run()
	while True:
		movement = q.get()
		emit('move', {'move': movement})
