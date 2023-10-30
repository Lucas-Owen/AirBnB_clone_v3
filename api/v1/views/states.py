#!/usr/bin/python3
"""This module defies a view for the states path"""
from ..views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, make_response, request


@app_views.route("/states", methods=["GET"])
@app_views.route("/states/<state_id>", methods=["GET"])
def get_states(state_id=None):
    """Retrieves a list of all State objects"""
    if state_id is not None:
        state = storage.get(State, state_id)
        if state:
            return jsonify(state.to_dict())
        abort(404)
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """Delete state with specified state id"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return make_response(jsonify(dict()), 200)
    abort(404)


@app_views.route("/states", methods=["POST"])
def post_state():
    """Create a state"""
    data = request.get_json(silent=True)
    if not data:
        return make_response("Not a JSON", 400)
    if "name" not in data:
        return make_response("Missing name", 400)
    if type(data) is not dict:
        return make_response("Not an object", 400)
    state = State(**data)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"])
def put_state(state_id):
    """Updates a state in the storage"""
    data = request.get_json(silent=True)
    if not data:
        return make_response("Not a JSON", 400)
    if type(data) is not dict:
        return make_response("Not an object", 400)
    state = storage.get(State, state_id)
    if state:
        for key in data:
            if key not in ['id', 'created_at', 'updated_at', '__class__']:
                setattr(state, key, data[key])
        storage.save()
        return make_response(jsonify(state.to_dict()), 200)
