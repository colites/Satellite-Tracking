from sklearn.svm import LinearSVC
from flask import Flask, Blueprint, request
from flask_cors import CORS

import schemas_queries as queries

main = Blueprint('main', __name__)

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    CORS(app) 
    return app

@main.route('/analyze', methods=['POST'])
def analyze_text():
    reviews = request.get_json()
    analyzer = Analyzer(train_features, train_labels)

    analyzed_reviews = []
    for review in reviews:
        date, name, text, stars = review[0], review[1], review[2], review[3]

        sentiment = analyzer.predict_model(text)
        analyzed_review = (date, name, text, sentiment, stars)
        analyzed_reviews.append(analyzed_review)
    
    queries.commitreviews(analyzed_reviews)

    return "Successfully committed reviews", 200

if __name__ == '__main__':
    app = create_app()
    app.run(debug=False)