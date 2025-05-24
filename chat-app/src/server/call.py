from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

active_calls = {}

@app.route('/call/start', methods=['POST'])
def start_call():
    data = request.json
    caller = data.get('caller')
    receiver = data.get('receiver')

    if caller and receiver:
        call_id = f"{caller}-{receiver}"
        active_calls[call_id] = {'caller': caller, 'receiver': receiver, 'status': 'active'}
        return jsonify({'message': 'Call started', 'call_id': call_id}), 200
    return jsonify({'error': 'Caller and receiver must be specified'}), 400

@app.route('/call/end', methods=['POST'])
def end_call():
    data = request.json
    call_id = data.get('call_id')

    if call_id in active_calls:
        del active_calls[call_id]
        return jsonify({'message': 'Call ended'}), 200
    return jsonify({'error': 'Call not found'}), 404

@app.route('/call/status', methods=['GET'])
def call_status():
    return jsonify(active_calls), 200

def run_server():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    server_thread = threading.Thread(target=run_server)
    server_thread.start()