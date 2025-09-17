
from flask import request, jsonify
from models import db, User, PostReaction
from helpers import verify_firebase_token
from . import api

@api.route("/posts/<int:post_id>/react", methods=["POST"])
def react_post(post_id):
    id_token = request.headers.get("Authorization")
    decoded_token = verify_firebase_token(id_token)
    if not decoded_token:
        return jsonify({"error": "Invalid token"}), 401

    user = User.query.filter_by(firebase_uid=decoded_token["uid"]).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    reaction_type = data.get("reaction")
    if reaction_type not in ["like", "dislike"]:
        return jsonify({"error": "Invalid reaction"}), 400

    # overwrite existing reaction
    existing = PostReaction.query.filter_by(post_id=post_id, user_id=user.user_id).first()
    if existing:
        existing.reaction = reaction_type
    else:
        new_reaction = PostReaction(post_id=post_id, user_id=user.user_id, reaction=reaction_type)
        db.session.add(new_reaction)

    db.session.commit()
    return jsonify({"message": f"Post {reaction_type}d"})
