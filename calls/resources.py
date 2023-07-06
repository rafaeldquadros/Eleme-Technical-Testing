from flask import jsonify
from flask_restful import Resource, reqparse
from .services import CallsServices
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


class Calls(Resource):
    __service__ = CallsServices()

    parser = reqparse.RequestParser()
    parser.add_argument(
        "priority_level",
        type=str,
        required=True,
        help="Enter the priority level 'HIGH/MEDIUM/LOW",
    )
    parser.add_argument(
        "status",
        type=str,
        required=False,
    )
    parser.add_argument(
        "setor",
        type=str,
        required=True,
        help="Inform the sector you want to send the call",
    )
    parser.add_argument(
        "description",
        type=str,
        required=True,
        help="Please provide a description of your problem!",
    )

    @jwt_required()
    def get(self):
        user_adds = get_jwt()
        if "is_admin" in user_adds and user_adds["is_admin"]:
            return self.__service__.find_all()
        else:
            return {"message": "Your account is not an administrator"}, 401

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()

        data = Calls.parser.parse_args()
        data["user_id"] = user_id

        return self.__service__.create(**data)


class CallsById(Resource):
    __service__ = CallsServices()

    parser = reqparse.RequestParser()
    parser.add_argument(
        "priority_level",
        type=str,
        required=False,
    )
    parser.add_argument(
        "status",
        type=str,
        required=False,
    )
    parser.add_argument(
        "setor",
        type=str,
        required=False,
    )
    parser.add_argument(
        "description",
        type=str,
        required=False,
    )

    @jwt_required()
    def get(self, id):
        user_adds = get_jwt()
        success = self.__service__.find_by_id(id)
        if success:
            if user_adds["sub"] == success.user_id or "is_admin" in user_adds:
                return success.as_dict()
            else:
                return {
                    "message": "You need to be a ticket owner or administrator to do this."
                }, 401
        else:
            return {"message": "Call not found"}, 404

    @jwt_required()
    def delete(self, id):
        user_adds = get_jwt()
        call = self.__service__.find_by_id(id)
        if call:
            if user_adds["sub"] == call.user_id or "is_admin" in user_adds:
                success = self.__service__.delete(id)
                if success:
                    return jsonify({"message": "Call deleted successfully"})
            else:
                return {
                    "message": "You need to be a ticket owner or administrator to do this."
                }, 401
        return {"message": "Call not found"}, 404

    @jwt_required()
    def patch(self, id):
        user_adds = get_jwt()
        call = self.__service__.find_by_id(id)
        if call:
            if user_adds["sub"] == call.user_id or "is_admin" in user_adds:
                data = CallsById.parser.parse_args()
                success = self.__service__.update(id, **data)
                return success
            else:
                return {
                    "message": "You need to be a ticket owner or administrator to do this."
                }, 401
        return {"message": "Call not found"}, 404
