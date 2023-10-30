#!/usr/bin/python3
"""This module defies a view for the states path"""
from ..views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, make_response, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieves the list of all State objects
    """
    all_states = storage.all(State).values()
    list_states = []
    for state in all_states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieves a specific State """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


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
    abort(404)
