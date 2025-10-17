import joblib
import pandas as pd 
from flask import Flask, request, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CollectorRegistry
import time

app = Flask(__name__)
registry = CollectorRegistry()

model = joblib.load('random_forest_model.joblib')
