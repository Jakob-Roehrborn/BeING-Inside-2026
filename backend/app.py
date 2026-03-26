from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from dataclasses import dataclass, asdict
from data_class import input_data
from main import main_backend

app = Flask(__name__)
CORS(app)

@app.route('/api/calculate', methods=['POST'])
def calculate():
    json_data = request.get_json() 
    
    if not json_data:
        return make_response("Unable to parse json", 400)

    data = input_data(**json_data)
    
    output = main_backend(data)
    # print(output)
    return make_response(jsonify(asdict(output)), 200)
    return make_response("toll", 200)

@app.route("/api/module_change", methods=["POST"])
def module_change():
    data_json = request.get_json()
    print(data_json)
    return make_response("Ok", 200)

@app.route("/")
def index():
    return make_response("<h1>You've reached the server</h1>")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000) 