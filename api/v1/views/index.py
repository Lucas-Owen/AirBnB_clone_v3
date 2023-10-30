#!/usr/bin/python3
"""This module defines status route of the app"""
from ..views import app_views
from flask import jsonify
from models.engine.db_storage import classes
from models import storage


@app_views.route("/status", methods=["GET"])
def status():
    """Returns an OK status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"])
def stats():
    summary = {name: storage.count(cls) for name, cls in classes.items()}
    return jsonify(summary)
