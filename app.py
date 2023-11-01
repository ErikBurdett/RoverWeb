from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong, unique secret key
socketio = SocketIO(app)

# A simple dictionary to store user information for this example.
users = {'username': 'password'}  # Replace with your user database.

@app.route('/')
def home():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@socketio.on('message')
def handle_message(message):
    if 'username' in session:
        emit('message', {'username': session['username'], 'message': message})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80)
