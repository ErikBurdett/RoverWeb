from flask import Flask, request, jsonify

app = Flask(__name)

rover_message = ""

@app.route('/')
def home():
    return """
    <main class="font-mono">
      <h1 class="text-3xl text-center p-4 font-bold">Rover App</h1>
      <div class='flex justify-center flex-col items-center'>
        <button class='active:bg-neutral-500 border p-2 border-black rounded' onclick="fetchRover()">Call Rover</button>
        <p class='text-blue-700 pt-4' id="rover-message"></p>
        <div class="pt-4">
          <input type="text" value="" id="new-message" placeholder="New message to Rover" class="border p-2 border-black rounded" />
          <button class="active:bg-neutral-500 border p-2 border-black rounded ml-2" onclick="updateRoverMessage()">Send to Rover</button>
        </div>
      </div>
    </main>
    <script>
      function fetchRover() {
        fetch('/api/data')
          .then(response => response.json())
          .then(data => {
            document.getElementById("rover-message").textContent = "Message from Rover: " + data.message;
          });
      }

      function updateRoverMessage() {
        const newMessage = document.getElementById("new-message").value;
        fetch('/api/data', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ text: newMessage }),
        });
      }
    </script>
    """

@app.route('/api/data', methods=['GET', 'POST'])
def api_data():
    global rover_message

    if request.method == 'GET':
        return jsonify({'message': rover_message})
    elif request.method == 'POST':
        data = request.get_json()
        rover_message = data['text']
        return jsonify({'message': 'Message updated successfully'})

if __name__ == '__main__':
    app.run(debug=True)
