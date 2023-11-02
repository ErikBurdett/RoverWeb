from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Add your login logic here (e.g., checking credentials)

    return 'Logged in as ' + username

if __name__ == '__main__':
    app.run(ssl_context='adhoc', debug=True)
