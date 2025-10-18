import os
import time
import traceback

import joblib
import pandas as pd
from flask import Flask, request, jsonify, Response
from prometheus_client import Counter, Histogram, generate_latest, CollectorRegistry

app = Flask(__name__)
registry = CollectorRegistry()

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'random_forest_model.joblib')
MODEL_PATH = os.path.abspath(MODEL_PATH)

try:
    model = joblib.load(MODEL_PATH)
except Exception:
    app.logger.exception('Failed to load model at %s', MODEL_PATH)
    model = None

REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status_code'],
    registry=registry,
)
REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency in seconds',
    ['method', 'endpoint'],
    registry=registry,
)
PREDICTION_COUNT = Counter('prediction_requests_total', 'Total number of prediction requests', registry=registry)
PREDICTION_LATENCY = Histogram('prediction_duration_seconds', 'Prediction latency in seconds', registry=registry)
PREDICTION_ERRORS = Counter('prediction_errors_total', 'Total number of prediction errors', registry=registry)


@app.route('/predict', methods=['POST'])
def predict():
    method = request.method
    endpoint = '/predict'
    status_code = 500
    request_start = time.time()

    if model is None:
        PREDICTION_ERRORS.inc()
        status_code = 500
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status_code=str(status_code)).inc()
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(time.time() - request_start)
        return jsonify({'error': 'Model not available'}), 500

    try:
        PREDICTION_COUNT.inc()
        payload = request.get_json(force=True)

        if not isinstance(payload, dict):
            raise ValueError('Payload must be a JSON object with feature keys.')
        input_df = pd.DataFrame([payload])

        pred_start = time.time()
        prediction = model.predict(input_df)
        pred_duration = time.time() - pred_start
        PREDICTION_LATENCY.observe(pred_duration)

        status_code = 200
        return jsonify({'prediction': prediction.tolist()}), 200

    except Exception as exc:
        PREDICTION_ERRORS.inc()
        app.logger.error('Prediction error: %s', exc)
        app.logger.debug(traceback.format_exc())
        status_code = 500
        return jsonify({'error': str(exc)}), 500

    finally:
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(time.time() - request_start)
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status_code=str(status_code)).inc()


@app.route('/metrics')
def metrics():
    data = generate_latest(registry)
    return Response(data, mimetype='text/plain; version=0.0.4; charset=utf-8')


@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


@app.route('/ready')
def ready():
    if model is None:
        return jsonify({'ready': False}), 503
    return jsonify({'ready': True})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)