from flask import Flask, send_from_directory

app = Flask(__name)

# Serve your React app from the 'build' directory
@app.route('/')
def serve_react_app():
    return send_from_directory('react_app/build', 'index.html')

# Serve static assets (CSS, JS, etc.) from the 'build/static' directory
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('react_app/build/static', filename)

if __name__ == '__main__':
    app.run(debug=True)
