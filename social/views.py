
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Count

from .models import Post, Comment, Follower, PostReaction
from .serializers import (
    PostSerializer, CommentSerializer, FollowerSerializer, 
    PostReactionSerializer, UserProfileSerializer
)
from users.models import User
from .pagination import StandardResultsSetPagination

# ------------------- Posts -------------------
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Post.objects.filter(user_id=self.kwargs["user_id"]).order_by('-created_at')

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        following_ids = user.following.values_list("following_id", flat=True)
        return Post.objects.filter(Q(user__in=following_ids) | Q(user=user)).order_by('-created_at')

class PostDetailView(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = "id"

# ------------------- Comments -------------------
class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostCommentsView(generics.ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs["post_id"], parent__isnull=True).order_by("created_at")

class CommentRepliesView(generics.ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Comment.objects.filter(parent_id=self.kwargs["comment_id"]).order_by("created_at")

# ------------------- Followers -------------------
class FollowerView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user_id = request.data.get("user_id")
        try:
            user_to_follow = User.objects.get(id=user_id)
            if user_to_follow == request.user:
                return Response({"error": "Cannot follow yourself"}, status=400)
            Follower.objects.get_or_create(user=user_to_follow, follower=request.user)
            return Response({"status": f"Now following {user_to_follow.username}"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

    def delete(self, request):
        user_id = request.data.get("user_id")
        try:
            user_to_unfollow = User.objects.get(id=user_id)
            Follower.objects.filter(user=user_to_unfollow, follower=request.user).delete()
            return Response({"status": f"Unfollowed {user_to_unfollow.username}"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

class FollowersListView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return User.objects.filter(following__following_id=self.kwargs["user_id"])

class FollowingListView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return User.objects.filter(followers__follower_id=self.kwargs["user_id"])

# ------------------- Post Reactions -------------------
class PostReactionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        post_id = request.data.get("post_id")
        reaction_type = request.data.get("reaction_type")
        try:
            post = Post.objects.get(id=post_id)
            reaction, created = PostReaction.objects.get_or_create(
                user=request.user, post=post, reaction_type=reaction_type
            )
            return Response({"status": f"{reaction_type} added" if created else f"{reaction_type} already exists"})
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=404)

    def delete(self, request):
        post_id = request.data.get("post_id")
        reaction_type = request.data.get("reaction_type")
        PostReaction.objects.filter(user=request.user, post_id=post_id, reaction_type=reaction_type).delete()
        return Response({"status": f"{reaction_type} removed"})

class PostLikesListView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        user_ids = PostReaction.objects.filter(post_id=post_id, reaction_type=PostReaction.LIKE).values_list("user_id", flat=True)
        return User.objects.filter(id__in=user_ids)

# ------------------- Profiles -------------------
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    lookup_field = "id"

# ------------------- Search -------------------
class SearchPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        q = self.request.query_params.get("q", "")
        return Post.objects.filter(text__icontains=q).order_by('-created_at')[:20]

class SearchUsersView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        q = self.request.query_params.get("q", "")
        return User.objects.filter(Q(username__icontains=q) | Q(full_name__icontains=q))
