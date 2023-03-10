from flask import request
from app import flask_app
from schema import extract_arguments, GetFlatsSchema
from response import SuccessResponse


@flask_app.route("/api/flats/page", methods=["GET"])
def api_get_paginated_flats():
    """
    Get paginated entries of the flats.
    :return: list of dicts
    """
    # TODO add a possibility to check only new offers
    get_flats_schema = GetFlatsSchema()
    args = extract_arguments(get_flats_schema, request=request)
    print(args[get_flats_schema.currency])
    return SuccessResponse(response_payload={**args}).generate_response()


@flask_app.route("/api/group/add", methods=["POST"])
def api_post_new_group_name():
    pass


@flask_app.route("/api/group/remove", methods=['DELETE'])
def api_post_delete_group_name():
    pass
