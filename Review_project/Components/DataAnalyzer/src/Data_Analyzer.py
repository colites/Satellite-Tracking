import requests
import psycopg2
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/analyze', methods=['POST'])
def analyze_text():
    ## analyzer = Analyzer(train_features, train_labels)
    ## sentiment = analyzer.predict_model(text)
    ## return sentiment
    ## then store it to a database
    pass


class Analyzer():
    def __init__(self, train_features, train_labels):
        self.model = self.train_model(train_features, train_labels)

    def train_model(self, train_features, train_labels):
        model = LinearSVC(C=1,
                        class_weight='balanced',
                        dual=True,
                        loss='squared_hinge',
                        penalty='l2')

        model.fit(train_features, train_labels)
        return model

    def predict_model(self, text):
        sentiment_SVM = self.model.predict(text)
        return sentiment_SVM

if __name__ == '__main__':
    app.run(debug=False)