import os
import time
import traceback

import joblib
import pandas as pd
from flask import Flask, request, jsonify, Response
from pydantic import ValidationError
from app.validation import PredictionRequest, FEATURE_ORDER
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'random_forest_model.joblib')
MODEL_PATH = os.path.abspath(MODEL_PATH)

try:
    model = joblib.load(MODEL_PATH)
except Exception:
    app.logger.exception('Failed to load model at %s', MODEL_PATH)
    model = None

PREDICTION_COUNT = Counter('prediction_requests_total', 'Total number of prediction requests')
PREDICTION_LATENCY = Histogram('prediction_duration_seconds', 'Prediction latency in seconds')
PREDICTION_ERRORS = Counter('prediction_errors_total', 'Total number of prediction errors')


@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        PREDICTION_ERRORS.inc()
        return jsonify({'error': 'Model not available'}), 500

    try:
        PREDICTION_COUNT.inc()
        payload = request.get_json(force=True)

        if isinstance(payload, list):
            if len(payload) != getattr(model, 'n_features_in_', None):
                return jsonify({
                    'error': 'invalid input',
                    'details': f'expected {getattr(model, "n_features_in_", "?")} features'
                }), 400
            input_df = pd.DataFrame([payload], columns=FEATURE_ORDER)

        elif isinstance(payload, dict):
            try:
                validated = PredictionRequest.model_validate(payload)
            except ValidationError as e:
                return jsonify({'error': 'invalid input', 'details': e.errors()}), 400

            feature_dict = validated.as_feature_dict(by_alias=True)
            try:
                input_df = pd.DataFrame([feature_dict])[FEATURE_ORDER]
            except KeyError as e:
                return jsonify({'error': 'invalid input', 'details': f'missing feature: {e}'}), 400

        else:
            return jsonify({'error': 'invalid payload format (expected object or array)'}), 400

        pred_start = time.time()
        prediction = model.predict(input_df)
        pred_duration = time.time() - pred_start
        PREDICTION_LATENCY.observe(pred_duration)

        return jsonify({'prediction': prediction.tolist()}), 200

    except Exception as exc:
        PREDICTION_ERRORS.inc()
        app.logger.error('Prediction error: %s', exc)
        app.logger.debug(traceback.format_exc())
        return jsonify({'error': str(exc)}), 500


@app.route('/metrics')
def metrics():
    data = generate_latest(REGISTRY)
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