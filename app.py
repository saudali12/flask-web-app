# app.py
from flask import Flask, request, jsonify
import time
import random
import threading

app = Flask(__name__)

def mock_model_predict(input: str) -> dict:
    time.sleep(random.randint(8, 15))  # Simulate processing delay
    result = str(random.randint(100, 10000))
    output = {"input": input, "result": result}
    return output

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if 'Async-Mode' in request.headers:
        prediction_id = str(random.randint(100000, 999999))
        # Simulate asynchronous processing
        threading.Thread(target=background_prediction, args=(data['input'], prediction_id)).start()
        return jsonify({"message": "Request received. Processing asynchronously.", "prediction_id": prediction_id}), 202
    else:
        result = mock_model_predict(data['input'])
        return jsonify(result), 200

def background_prediction(input, prediction_id):
    result = mock_model_predict(input)
    # Store result in a persistent storage or in-memory data structure

if __name__ == '__main__':
    app.run(port=8080)
