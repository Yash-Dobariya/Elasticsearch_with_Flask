from src.database import es
from datetime import datetime


def current_datetime():
    """current date and time"""
    return str(datetime.utcnow())


def set_default_values(data, user_id):
    """Set default values for indexes"""

    data.setdefault("is_activate", True)
    data.setdefault("is_delete", False)
    data.setdefault("created_at", current_datetime())
    data.setdefault("created_by", user_id)
    data.setdefault("updated_at", current_datetime())
    data.setdefault("updated_by", user_id)
    return data


def get_data_from_es(id, index):
    """Get data from Elasticsearch"""

    data = es.get(index=index, id=id)
    user_data = data["_source"]

    default_values = [
        "is_activate",
        "is_delete",
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
    ]

    for key in default_values:
        user_data.pop(key, None)

    response_data = {**user_data}
    response_data["id"] = id

    return response_data
