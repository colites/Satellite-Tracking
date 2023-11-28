from flask import Flask, render_template, Blueprint
from flask_cors import CORS

main = Blueprint('main', __name__)

def create_app():
    front_app = Flask(__name__)
    front_app.register_blueprint(main)
    CORS(front_app) 
    return front_app

@main.route("/")
def frontPage():
    return render_template('search_input.html')

if __name__ == '__main__':
    front_app = create_app()
    front_app.run(debug=False)
