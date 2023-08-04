from flask import Blueprint, request, jsonify
from src.database import es
import uuid
from flask_api import status
from src.utils.same_function import (
    get_data_from_es,
    set_default_values,
    current_datetime,
)


user = Blueprint("user", __name__)

INDEX = "user"


@user.route("/create_user", methods=["POST"])
def create_user():
    """Create user"""

    data = request.json
    user_id = str(uuid.uuid4())
    data = set_default_values(data, user_id)

    es.index(index=INDEX, id=user_id, document=data)

    user_data = get_data_from_es(id=user_id, index=INDEX)

    return jsonify(user_data), status.HTTP_201_CREATED


@user.route("/get_user/<user_id>", methods=["GET"])
def get_particular_user(user_id):
    """get particular user"""
    
    user_data = get_data_from_es(id=user_id, index=INDEX)

    return jsonify(user_data), status.HTTP_200_OK


@user.route("/all_users", methods=["GET"])
def get_all_users():
    """Get all users"""

    es_response = es.search(index=INDEX, body={"query": {"match_all": {}}})

    users_data = [
        {"id": hit["_id"], **hit["_source"]} for hit in es_response["hits"]["hits"]
    ]

    return jsonify(users_data), status.HTTP_200_OK


@user.route("/update_user/<user_id>", methods=["PUT"])
def update_data(user_id):
    """update_data"""

    data = request.json
    data["updated_at"] = current_datetime()
    data["updated_by"] = user_id
    es.update(index=INDEX, id=user_id, doc=data)

    return jsonify({"message": "successfully updated {user_id}"}), status.HTTP_200_OK


@user.route("/delete_user/<user_id>", methods=["DELETE"])
def delete_data(user_id):
    """delete_data"""

    es.delete(index=INDEX, id=user_id)
    return jsonify({"message": "successfully deleted {user_id}"}), status.HTTP_200_OK
