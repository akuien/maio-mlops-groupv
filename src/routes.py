from flask import Blueprint, render_template, jsonify, request
from .model import predict

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template("index.html", message="Hello, Flask!")

@main.route('/health')
def health():
    return jsonify({"status": "ok", "model_version": "v0.1"})

@main.route('/predict', methods=['POST'])
def predictData():
    # TODO: Validate input
    result = predict(request.json)
    return {"prediction": result.tolist()}
