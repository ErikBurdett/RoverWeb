from flask import Flask

app = Flask(__name__)

correct_username = "rover"
correct_password = "rover"

@app.route('/')
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == correct_username and password == correct_password:
            return redirect(url_for('control_panel'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

@app.route('/control-panel')
def control_panel():
    return render_template('control_panel.html')
