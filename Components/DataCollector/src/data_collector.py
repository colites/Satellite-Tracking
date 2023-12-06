import requests
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS

import Components.schemas_queries as queries

main = Blueprint('main', __name__)
#license key = 777RKY-662TWA-KAK8Z7-55Y1
def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    CORS(app) 
    return app


@main.route('/get-satellites', methods=['POST'])
def getData():
    data = request.get_json()
    
    api_key = '777RKY-662TWA-KAK8Z7-55Y1'
    latitude = data['latitude']
    longitude = data['longitude']
    altitude = 0
    search_radius = 30
    category = 0

    url = f"https://api.n2yo.com/rest/v1/satellite/above/{latitude}/{longitude}/{altitude}/{search_radius}/{category}/&apiKey={api_key}"
    response = requests.get(url)    
    if response.status_code != 200:
       return jsonify({"message": "Unable to get API satellite data"}), response.status_code
    
    data = response.json()
    status = queries.commitSatellites(data, latitude, longitude)
    if status == "fail":
        return jsonify({"message": "Database Commit Failed"}), 500
    
    return jsonify({"message": "Successfully added satellite information"}), 201
    

if __name__ == '__main__':
    app = create_app()
    app.run(debug=False)