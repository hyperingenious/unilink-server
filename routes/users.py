
from flask import request, jsonify
from models import db, User
from helpers import verify_firebase_token
from . import api

@api.route("/users", methods=["POST"])
def create_user():
    data = request.json
    new_user = User(
        firebase_uid=data["firebase_uid"],
        username=data["username"],
        name=data.get("name"),
        dob=data.get("dob"),
        gender=data.get("gender"),
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created", "user_id": new_user.user_id})

@api.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "user_id": user.user_id,
        "username": user.username,
        "name": user.name,
        "dob": str(user.dob),
        "gender": user.gender
    })
