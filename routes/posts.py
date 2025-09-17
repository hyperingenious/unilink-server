
from flask import request, jsonify
from models import db, User, Post
from helpers import verify_firebase_token
from . import api

@api.route("/posts", methods=["POST"])
def create_post():
    id_token = request.headers.get("Authorization")
    decoded_token = verify_firebase_token(id_token)
    if not decoded_token:
        return jsonify({"error": "Invalid token"}), 401

    user = User.query.filter_by(firebase_uid=decoded_token["uid"]).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    new_post = Post(
        user_id=user.user_id,
        content=data.get("content"),
        image_url=data.get("image_url")
    )
    db.session.add(new_post)
    db.session.commit()
    return jsonify({"message": "Post created", "post_id": new_post.post_id})

@api.route("/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    return jsonify({
        "post_id": post.post_id,
        "user_id": post.user_id,
        "content": post.content,
        "image_url": post.image_url,
        "created_at": post.created_at.isoformat()
    })
