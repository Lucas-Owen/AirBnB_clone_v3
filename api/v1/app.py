#!/usr/bin/python3
"""This module defines the flask app"""
from .views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
import os

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={'/*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def teardown(exc):
    """Tears down the app context"""
    storage.close()


@app.errorhandler(404)
def not_found_handler(error):
    """Handler when a 404 is raised"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST')
    if host is None:
        host = '0.0.0.0'
    port = os.getenv('HBNB_API_PORT')
    if port is None:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
