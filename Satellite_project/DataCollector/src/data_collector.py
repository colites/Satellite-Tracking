import requests
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
import json
import pika

main = Blueprint('main', __name__)

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    CORS(app) 
    return app

@main.route('/get-satellites', methods=['POST'])
def getData():
    data = request.get_json()
    
    credentials = pika.PlainCredentials('guest', 'guest')

    connection_parameters = pika.ConnectionParameters(
        host='rabbitmq-server-kgaz.onrender.com',
        credentials=credentials
    )
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    channel.queue_declare(queue='database_queue')

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
    
    ## data needs to be made into Json-encoded bytes for the message queue producer.
    try: 
        message = json.dumps({'data': data, 'latitude': latitude, 'longitude': longitude}).encode()
        channel.basic_publish(exchange='',
                        routing_key='database_queue',
                        body=message)

        channel.close()
        connection.close()

    except Exception as e:
        return jsonify({"message": "could not send to message queue"}), 500

    return jsonify({"message": "sent information to message queue"}), 201
    

if __name__ == '__main__':
    app = create_app()
    app.run(debug=False)