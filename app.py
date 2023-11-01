from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In a real-world application, you should store user data securely, e.g., in a database.
# For this example, we'll use a simple dictionary to store user information.
users = {
    'user1': 'password1',
    'user2': 'password2',
}

@app.route('/')
def home():
    return render_template('Templates/login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username] == password:
        # In a real application, you should set up proper user sessions.
        return 'Login successful!'
    else:
        return 'Login failed. Please check your username and password.'

if __name__ == '__main__':
    app.run(debug=True)

