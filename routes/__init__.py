
from flask import Blueprint

# Create a blueprint to register all routes
api = Blueprint('api', __name__)

# Import individual route modules to attach routes
from . import users, posts, comments, followers, reactions, chats
