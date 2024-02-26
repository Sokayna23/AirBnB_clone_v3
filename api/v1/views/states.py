#!/usr/bin/python3
"""State view"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Docs"""
    states = []
    for state in storage.all('State').values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Docs"""
    try:
        state = storage.get('State', state_id)
        return jsonify(storage.get('State', state_id).to_dict())
    except Exception:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Docs"""
    try:
        storage.delete(storage.get('State', state_id))
        storage.save()
        return jsonify({}), 200
    except Exception as e:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Docs"""
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400

    new_state = State(**request.get_json())
    new_state.save()
    return jsonify(new_state.to_dict()), 201
