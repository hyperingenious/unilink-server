from rest_framework import serializers
from .models import Post, Comment, Follower, PostReaction
from users.serializers import UserSerializer
from users.models import User

# Recursive Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    subcomments = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "post", "parent", "text", "created_at", "subcomments"]

    def get_subcomments(self, obj):
        serializer = CommentSerializer(obj.subcomments.all(), many=True)
        return serializer.data

# Post Serializer
class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    reactions_count = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "user", "text", "image_url", "created_at", "comments", "reactions_count"]

    def get_reactions_count(self, obj):
        return obj.reactions.count()

# Follower Serializer
class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ["id", "user", "follower"]

# Post Reaction Serializer
class PostReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReaction
        fields = ["id", "user", "post", "reaction_type"]

# User Profile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "full_name", "bio", "profile_photo",
                  "followers_count", "following_count", "posts_count"]

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_posts_count(self, obj):
        return obj.posts.count()
