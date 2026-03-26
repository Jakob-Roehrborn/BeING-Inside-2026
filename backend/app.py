from flask import Flask, jsonify, request, make_response, Response
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from dataclasses import asdict
from data_class import input_data
from main import main_backend
import user_json_new as js

app = Flask(__name__)
app.config['SECRET_KEY'] = 'WS-key'
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    print("WS CON")

@socketio.on('disconnect')
def handle_disconnect():
    print("WS DISCON")

# @socketio.on('client_message')
# def handle_client_message(payload):
#     print('Received message from frontend:', payload)
    
#     response = f"Server heard you say: {payload}"
#     emit('server_message', {'data': response})

@app.route('/api/calculate', methods=['POST'])
def calculate():
    json_data = request.get_json() 
    
    if not json_data:
        return make_response("Unable to parse json", 400)

    data = input_data(**json_data)
    js.update_config_from_api(data) # setzt die Koordinaten basierend auf der plz
    js.save_user_data(data, 'user.json') # speichert die Änderung
     
    output = main_backend(data)

    return make_response(output.model_dump_json(), 200)
    return make_response("toll", 200)

@app.route("/api/module_change", methods=["POST"])
def module_change():
    data_json = request.get_json()
    print("MODULE CHANGE: ", data_json)
    socketio.emit('module_change', data_json)

    return make_response("Ok", 200)

@app.route("/api/hit", methods=["GET"])
def hit():
    socketio.emit('module_change', {"module": 1, "state": 1})

    return Response("<p>You've hit me </p>", status=200)
    

@app.route("/")
def index():
    return make_response("<h1>You've reached the server</h1>")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000) 