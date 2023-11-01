from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(name)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected!')

if name == 'main':
    socketio.run(app, debug=True)
