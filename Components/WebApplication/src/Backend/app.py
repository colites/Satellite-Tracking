import requests
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS

main = Blueprint('main', __name__)

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    CORS(app) 
    return app

@main.route('/send-coordinates', methods=['POST'])
def SendCoordinatesToCollector():
    data = request.get_json()

    latitude = data.get("latitude", "")
    longitude = data.get("longitude", "")
    if latitude == "" or longitude == "":
        return jsonify({"message": "Missing a Required Piece of Information"}), 400

    coordinates = (latitude, longitude)
    response = requests.post('https://0.0.0.0:5003/get-satellites', json=coordinates)
    if response.status_code != 200:
        return jsonify({"message": "Could not send to Data Collector"}), response.status_code
    
    return jsonify({"message": "Coordinates sent to satellite data collector"}), 200

if __name__ == '__main__':
    app = create_app()
    app.run(debug=False,host='0.0.0.0')
