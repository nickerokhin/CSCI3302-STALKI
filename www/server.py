from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, emit
from threading import Lock


# initialize Flask


def run_server(q):

	app = Flask(__name__)
	socketio = SocketIO(app, async_mode='threading')
	@app.route('/')
	def index():
		"""Serve the index HTML"""
		return render_template('index.html')


	@socketio.on('direction')
	def receive_connections(res):
		print("BEFORE LOOP")
		while True:
			movement = q.get()
			print(movement)
			
			emit('move', {'move': movement})
			
	socketio.run(app, debug=True)
	
