from flask import Flask, render_template

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
		print(movement)
