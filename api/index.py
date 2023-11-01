from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# A simple dictionary to store username-password pairs (for demonstration purposes)
users = {
    'user1': 'password1',
    'user2': 'password2',
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username] == password:
            # You can add session management or set a cookie to keep the user logged in
            return "Login successful. Welcome, " + username
        else:
            return "Login failed. Please try again."

    return '''
        <form method="post">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required><br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required><br>
            <input type="submit" value="Login">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
