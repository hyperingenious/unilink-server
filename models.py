
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.BigInteger, primary_key=True)
    firebase_uid = db.Column(db.String(128), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100))
    dob = db.Column(db.Date)
    gender = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Post(db.Model):
    __tablename__ = "posts"
    post_id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.user_id"), nullable=False)
    content = db.Column(db.Text)
    image_url = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Comment(db.Model):
    __tablename__ = "comments"
    comment_id = db.Column(db.BigInteger, primary_key=True)
    post_id = db.Column(db.BigInteger, db.ForeignKey("posts.post_id"), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.user_id"), nullable=False)
    parent_id = db.Column(db.BigInteger, db.ForeignKey("comments.comment_id"))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Follower(db.Model):
    __tablename__ = "followers"
    follower_id = db.Column(db.BigInteger, db.ForeignKey("users.user_id"), primary_key=True)
    following_id = db.Column(db.BigInteger, db.ForeignKey("users.user_id"), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PostReaction(db.Model):
    __tablename__ = "post_reactions"
    reaction_id = db.Column(db.BigInteger, primary_key=True)
    post_id = db.Column(db.BigInteger, db.ForeignKey("posts.post_id"), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.user_id"), nullable=False)
    reaction = db.Column(db.String(10), nullable=False)  # like / dislike
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ChatRoom(db.Model):
    __tablename__ = "chat_rooms"
    room_id = db.Column(db.BigInteger, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ChatParticipant(db.Model):
    __tablename__ = "chat_participants"
    room_id = db.Column(db.BigInteger, db.ForeignKey("chat_rooms.room_id"), primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.user_id"), primary_key=True)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

class Message(db.Model):
    __tablename__ = "messages"
    message_id = db.Column(db.BigInteger, primary_key=True)
    room_id = db.Column(db.BigInteger, db.ForeignKey("chat_rooms.room_id"), nullable=False)
    sender_id = db.Column(db.BigInteger, db.ForeignKey("users.user_id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
