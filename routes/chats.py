from flask import request, jsonify
from models import db, User, Message
from helpers import verify_firebase_token
from . import api

# Send a message to another user
@api.route("/messages", methods=["POST"])
def send_message():
    id_token = request.headers.get("Authorization")
    decoded_token = verify_firebase_token(id_token)
    if not decoded_token:
        return jsonify({"error": "Invalid token"}), 401

    sender = User.query.filter_by(firebase_uid=decoded_token["uid"]).first()
    if not sender:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    receiver_id = data.get("receiver_id")
    receiver = User.query.get(receiver_id)
    if not receiver:
        return jsonify({"error": "Receiver not found"}), 404

    new_message = Message(sender_id=sender.user_id, receiver_id=receiver_id, content=data.get("content"))
    db.session.add(new_message)
    db.session.commit()
    return jsonify({"message": "Message sent", "message_id": new_message.message_id})

# Get messages between current user and another user
@api.route("/messages/<int:user_id>", methods=["GET"])
def get_messages(user_id):
    id_token = request.headers.get("Authorization")
    decoded_token = verify_firebase_token(id_token)
    if not decoded_token:
        return jsonify({"error": "Invalid token"}), 401

    current_user = User.query.filter_by(firebase_uid=decoded_token["uid"]).first()
    if not current_user:
        return jsonify({"error": "User not found"}), 404

    messages = Message.query.filter(
        ((Message.sender_id == current_user.user_id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user.user_id))
    ).order_by(Message.created_at.asc()).all()

    return jsonify([{
        "message_id": m.message_id,
        "sender_id": m.sender_id,
        "receiver_id": m.receiver_id,
        "content": m.content,
        "created_at": m.created_at.isoformat()
    } for m in messages])
