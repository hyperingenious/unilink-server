from flask import request, jsonify
from models import db, Comment, User
from helpers import verify_firebase_token
from . import api

@api.route("/posts/<int:post_id>/comments", methods=["POST"])
def create_comment(post_id):
    id_token = request.headers.get("Authorization")
    decoded_token = verify_firebase_token(id_token)
    if not decoded_token:
        return jsonify({"error": "Invalid token"}), 401

    user = User.query.filter_by(firebase_uid=decoded_token["uid"]).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    new_comment = Comment(
        post_id=post_id,
        user_id=user.user_id,
        parent_id=data.get("parent_id"),
        content=data.get("content")
    )
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({"message": "Comment created", "comment_id": new_comment.comment_id})

@api.route("/posts/<int:post_id>/comments", methods=["GET"])
def get_comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id).all()
    return jsonify([{
        "comment_id": c.comment_id,
        "user_id": c.user_id,
        "parent_id": c.parent_id,
        "content": c.content,
        "created_at": c.created_at.isoformat()
    } for c in comments])
