from flask import Flask, Blueprint, request, jsonify
from flask_cors import CORS

import Components.schemas_queries as queries

main = Blueprint('main', __name__)

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    CORS(app) 
    return app

@main.route('/make-map', methods=['POST'])
def makeMap():
    
    data = request.get_json()

    satlongitude = data.get("satlongitude", "all")
    satlatitude = data.get("satlatitude", "all")
    sataltitude = data.get("sataltitude", "all")
    satname = data.get("satname", "all")
    includes = data.get("includes")
    
    if includes == "all":
        satellite_data = queries.getAllSatellites()
        return jsonify(satellite_data), 200
    
    if includes == "filtered":
        satellite_data = queries.getSatellitesFiltered(satname, satlongitude, satlatitude, sataltitude)   
        return jsonify(satellite_data), 200
    
    return jsonify({"message": "data could not be analyzed"}), 500


@main.route('/orbit-calculations', methods=['POST'])
def orbitCalculations():
    satellite_data = queries.getAllSatellites()
    orbits_data = {"LEO": [], "MEO": [], "HEO": [], "GEO": []}
    for satellite in satellite_data:
        satellite_altitude = satellite["sataltitude"]
        if satellite_altitude <= 2000:
            orbits_data["LEO"].append(satellite)
        elif satellite_altitude < 35785:
            orbits_data["MEO"].append(satellite)
        elif satellite_altitude > 35787:
            orbits_data["HEO"].append(satellite)
        elif 35785 <= satellite_altitude <= 35787:
            orbits_data["GEO"].append(satellite)
    
    data = {
        'labels':["LEO","MEO","HEO","GEO"],
        'datasets' : [{
            'label': "Satellites in orbit categories",
            'data': [len(orbits_data["LEO"]), len(orbits_data["MEO"]), len(orbits_data["HEO"]), len(orbits_data["GEO"])]            
        }]
    }

    return jsonify(data), 200


if __name__ == '__main__':
    app = create_app()
    app.run(debug=False)