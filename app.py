from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/login')
def handle_connect():
    print('Client connected')

@socketio.on('login', namespace='/login')
def handle_login(data):
    username = data['username']
    password = data['password']
    # Add your authentication logic here
    # For security, you should hash and salt the passwords and verify against a database

    if username == 'your_username' and password == 'your_password':
        socketio.emit('login_result', {'success': True}, namespace='/login')
    else:
        socketio.emit('login_result', {'success': False}, namespace='/login')

if __name__ == '__main__':
    socketio.run(app)

