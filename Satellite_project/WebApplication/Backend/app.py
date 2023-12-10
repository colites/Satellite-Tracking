import sys
import os
import requests
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from prometheus_client import CollectorRegistry, push_to_gateway, Counter

#need to include root imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import schemas_queries as queries

main = Blueprint('main', __name__)

# Metrics
registry = CollectorRegistry()
requests_counter = Counter('requests_total', 'Successful requests made by user in backend server', registry=registry)

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    CORS(app) 
    return app

def push_metrics():
    try:
        push_to_gateway('https://pushgateway-ln1p.onrender.com:9091', job='flask_app', registry=registry)
    except Exception as e:
        print("Metrics push failed:", e)

@main.route('/send-coordinates', methods=['POST'])
def SendCoordinatesToCollector():
    ## Send data to the collector
    requests_counter.inc()
    data = request.get_json()

    latitude = data.get("latitude", "")
    longitude = data.get("longitude", "")
    if latitude == "" or longitude == "":
        return jsonify({"message": "Missing a Required Piece of Information"}), 400
    
    coordinates = {'latitude':latitude, 'longitude':longitude}
    response = requests.post('https://data-collector-r7r1.onrender.com/get-satellites', json=coordinates)
    if response.status_code != 201:
        return jsonify({"message": "Could not send to Data Collector Successfully"}), 502
    
    ## send requested data to frontend if data was successfully put inside the database
    try:
        query_results = requests.get(f'https://backend-q6r6.onrender.com/Observable-satellites?latitude={latitude}&longitude={longitude}')
        push_metrics()
        return jsonify(query_results.json()), 200

    except Exception as e:
        print("error:", e)
        return jsonify({"message": "Coordinates could not be sent"}), 500


@main.route('/Observable-satellites', methods=['GET'])
def displayObservableSatellites():
    #query parameters in web requests are treated as strings, unless converted
    latitude = float(request.args.get("latitude"))
    longitude = float(request.args.get("longitude"))
    satellites = queries.getSatellites(latitude=latitude, longitude=longitude)

    return jsonify(satellites), 200


@main.route('/send-to-analyzer', methods=['POST'])
def sendData():
    requests_counter.inc()
    data = request.get_json()
    if len(data) == 0:
        return jsonify({"message": "No data to be analyzed"}), 400
    
    data_type = data["type"]
    
    if data_type == "orbits":
        calculations = requests.get('https://data-analyzer.onrender.com/orbit-calculations')
    if data_type == "map":
        calculations = requests.post('https://data-analyzer.onrender.com/make-map', json=data)
        
    if calculations.status_code != 200:
        return jsonify({"message": "Could not analyze the data"}), 502

    try:
        push_metrics()
        return jsonify(calculations.json()), 200
    
    except Exception as e:
        print("error:", e)
        return jsonify({"message": "Coordinates could not be sent"}), 500
    

if __name__ == '__main__':
    app = create_app()
    app.run(debug=False)
