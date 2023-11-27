from flask import Flask, Blueprint, request
from flask_cors import CORS

main = Blueprint('main', __name__)

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    CORS(app) 
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=False)