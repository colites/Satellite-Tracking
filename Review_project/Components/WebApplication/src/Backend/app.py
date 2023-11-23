import requests
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from datetime import date

import Backend.schemas_queries as queries

main = Blueprint('main', __name__)

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    CORS(app) 
    return app

@main.route('/submit-review', methods=['POST'])
def SendReviewToAnalyze():
    data = request.get_json()

    tdate = date.today() 
    product_name = data.get("ProductName", "")
    review_text = data.get("ReviewText", "")
    stars = data.get("stars", 0)

    review_data = [(tdate, product_name, review_text, stars)]

    response = requests.post('/analyze', json=review_data)

    return jsonify({"message": "Review submitted for analysis"}), response.status_code


@main.route('/query-data-frontend', methods=['GET'])
def SendToFrontend():
    product_name = request.args.get("productName", "")
    if (product_name == None or product_name == ""):
        return jsonify({"message": "No Product Name Given"}), 400
    
    product_reviews = queries.getProductReviewsQuery(product_name)
    return jsonify(product_reviews)


if __name__ == '__main__':
    app = create_app()
    app.run(debug=False)
