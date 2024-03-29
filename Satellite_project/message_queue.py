import pika
import logging
import json

import schemas_queries as queries

logging.basicConfig(level=logging.INFO)

def callback(ch, method, properties, body):
    data = json.loads(body.decode())

    satellite_data = data['data']
    latitude = data['latitude']
    longitude = data['longitude']

    status = queries.commitSatellites(satellite_data, latitude, longitude)
    if status == "fail":
        logging.error("Database commit failed")

credentials = pika.PlainCredentials('qdnreuvr', 'cLLZvcWfbND3eRC8d8-watMm3rKQB26W')

connection_parameters = pika.ConnectionParameters(
    host='hawk-01.rmq.cloudamqp.com',
    port=5672,  
    virtual_host='qdnreuvr',
    credentials=credentials
)

connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()
channel.queue_declare(queue='database_queue')
channel.basic_consume(queue='database_queue', on_message_callback=callback, auto_ack=True)

channel.start_consuming()