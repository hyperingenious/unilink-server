
from flask import request, jsonify
from models import db, User, Follower
from helpers import verify_firebase_token
from . import api

@api.route("/follow/<int:followee_id>", methods=["POST"])
def follow_user(followee_id):
    id_token = request.headers.get("Authorization")
    decoded_token = verify_firebase_token(id_token)
    if not decoded_token:
        return jsonify({"error": "Invalid token"}), 401

    follower = User.query.filter_by(firebase_uid=decoded_token["uid"]).first()
    if not follower:
        return jsonify({"error": "User not found"}), 404

    if follower.user_id == followee_id:
        return jsonify({"error": "Cannot follow yourself"}), 400

    if Follower.query.filter_by(follower_id=follower.user_id, following_id=followee_id).first():
        return jsonify({"error": "Already following"}), 400

    new_follow = Follower(follower_id=follower.user_id, following_id=followee_id)
    db.session.add(new_follow)
    db.session.commit()
    return jsonify({"message": "Now following user"})

@api.route("/unfollow/<int:followee_id>", methods=["POST"])
def unfollow_user(followee_id):
    id_token = request.headers.get("Authorization")
    decoded_token = verify_firebase_token(id_token)
    if not decoded_token:
        return jsonify({"error": "Invalid token"}), 401

    follower = User.query.filter_by(firebase_uid=decoded_token["uid"]).first()
    if not follower:
        return jsonify({"error": "User not found"}), 404

    follow = Follower.query.filter_by(follower_id=follower.user_id, following_id=followee_id).first()
    if not follow:
        return jsonify({"error": "Not following"}), 400

    db.session.delete(follow)
    db.session.commit()
    return jsonify({"message": "Unfollowed user"})
