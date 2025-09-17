
from flask import request, jsonify
from models import db, User, ChatRoom, ChatParticipant, Message
from helpers import verify_firebase_token
from . import api

@api.route("/chats", methods=["POST"])
def create_chat():
    id_token = request.headers.get("Authorization")
    decoded_token = verify_firebase_token(id_token)
    if not decoded_token:
        return jsonify({"error": "Invalid token"}), 401

    user = User.query.filter_by(firebase_uid=decoded_token["uid"]).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    new_room = ChatRoom()
    db.session.add(new_room)
    db.session.commit()

    participant = ChatParticipant(room_id=new_room.room_id, user_id=user.user_id)
    db.session.add(participant)
    db.session.commit()
    return jsonify({"room_id": new_room.room_id})

@api.route("/chats/<int:room_id>/join", methods=["POST"])
def join_chat(room_id):
    id_token = request.headers.get("Authorization")
    decoded_token = verify_firebase_token(id_token)
    if not decoded_token:
        return jsonify({"error": "Invalid token"}), 401

    user = User.query.filter_by(firebase_uid=decoded_token["uid"]).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    if ChatParticipant.query.filter_by(room_id=room_id, user_id=user.user_id).first():
        return jsonify({"error": "Already joined"}), 400

    participant = ChatParticipant(room_id=room_id, user_id=user.user_id)
    db.session.add(participant)
    db.session.commit()
    return jsonify({"message": "Joined chat"})

@api.route("/chats/<int:room_id>/messages", methods=["POST"])
def send_message(room_id):
    id_token = request.headers.get("Authorization")
    decoded_token = verify_firebase_token(id_token)
    if not decoded_token:
        return jsonify({"error": "Invalid token"}), 401

    user = User.query.filter_by(firebase_uid=decoded_token["uid"]).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    new_message = Message(room_id=room_id, sender_id=user.user_id, content=data.get("content"))
    db.session.add(new_message)
    db.session.commit()
    return jsonify({"message": "Message sent", "message_id": new_message.message_id})

@api.route("/chats/<int:room_id>/messages", methods=["GET"])
def get_messages(room_id):
    messages = Message.query.filter_by(room_id=room_id).all()
    return jsonify([{
        "message_id": m.message_id,
        "sender_id": m.sender_id,
        "content": m.content,
        "created_at": m.created_at.isoformat()
    } for m in messages])
