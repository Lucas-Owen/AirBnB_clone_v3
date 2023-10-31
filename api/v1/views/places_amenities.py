#!/usr/bin/python3
"""This module defies a view for the places path"""
from ..views import app_views
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity
from flask import jsonify, abort, make_response


@app_views.route("/places/<place_id>/amenities", methods=["GET"])
def get_places(place_id):
    """Retrieves a list of all Amenities objects in Place"""
    place = storage.get(Place, place_id)
    if place:
        amenities = []
        if storage_t == 'db':
            amenities = [amenity.to_dict() for amenity in place.amenities]
        else:
            for amenity in storage.all(Amenity):
                if amenity.place_id == place_id:
                    amenities.append(amenity.to_dict())
        return jsonify(amenities)
    abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"])
def delete_place(place_id, amenity_id):
    """Delete amenity in place with specified place id"""
    place = storage.get(Place, place_id)
    if place:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            if storage_t == 'db':
                if amenity in place.amenities:
                    place.amenities.remove(amenity)
                    storage.save()
                    return make_response(jsonify(dict()), 200)
            else:
                if amenity_id in place.amenities:
                    amenity.place_id = None
                    storage.save()
                    return make_response(jsonify(dict()), 200)
    abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"])
def post_place(place_id, amenity_id):
    """Link an Amenity to a place"""
    place = storage.get(Place, place_id)
    if place:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            if storage_t == 'db':
                if amenity not in place.amenities:
                    place.amenities.append(amenity)
                    storage.save()
                    return make_response(jsonify(amenity.to_dict()), 201)
            else:
                if amenity_id not in place.amenities:
                    amenity.place_id = place_id
                    storage.save()
                    return make_response(jsonify(amenity.to_dict()), 201)
            return make_response(jsonify(amenity.to_dict()), 200)
    abort(404)
