#!/usr/bin/python3
"""Docs"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_all_cities(state_id):
    """Docs"""
    try:
        cities = []
        state_list = storage.all('City')
        for key, val in state_list.items():
            cities_dict = val.to_dict()
            if cities_dict.get('state_id') == state_id:
                cities.append(cities_dict)
        return jsonify(cities)
    except Exception as e:
        abort(404)


@app_views.route('/cities/<city_id>',
                 methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Docs"""
    try:
        return jsonify(storage.get('City', city_id).to_dict())
    except Exception as e:
        abort(404)


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Docs"""
    try:
        city = storage.get('City', city_id)
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    except Exception as e:
        abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Docs"""
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    city = City(**request.get_json())
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Docs"""
    city = storage.get('City', city_id)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if city is None:
        abort(404)
    for key, val in request.get_json().items():
        if key not in ['id', 'state_id', 'updated_at', 'created_at']:
            setattr(city, key, val)
    city.save()
    return jsonify(city.to_dict())
