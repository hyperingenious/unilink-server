from rest_framework.permissions import AllowAny
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Count
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from datetime import datetime
from django.utils import timezone
import random


from .models import Post, Comment, Follower, PostReaction
from .serializers import (
    PostSerializer, CommentSerializer, FollowerSerializer, 
    PostReactionSerializer, UserProfileSerializer
)
from users.models import User
from .pagination import StandardResultsSetPagination, TimestampBasedPagination

# ------------------- Posts -------------------
class PostListCreateView(generics.ListCreateAPIView):
    """
    List all posts or create a new post.
    
    GET: Retrieve a paginated list of all posts, ordered by creation date (newest first)
    POST: Create a new post (requires authentication)
    """
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserPostsView(generics.ListAPIView):
    """
    Get all posts by a specific user.
    
    GET: Retrieve a paginated list of posts created by the specified user
    """
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination

    permission_classes = [AllowAny]
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Post.objects.filter(user_id=self.kwargs["user_id"]).order_by('-created_at')

class FeedView(generics.ListAPIView):
    """
    Get personalized feed for authenticated user with timestamp-based pagination and gender distribution.
    
    GET: Retrieve a paginated list of posts from users you follow plus your own posts
    Query Parameters:
    - timestamp: ISO timestamp for pagination
    - type: 'new' (posts newer than timestamp) or 'old' (posts older than timestamp)
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = TimestampBasedPagination

    def get_queryset(self):
        user = self.request.user
        following_ids = user.following.values_list("user_id", flat=True)
        
        # Base queryset: posts from followed users + own posts
        base_queryset = Post.objects.filter(Q(user__in=following_ids) | Q(user=user))
        
        # Get timestamp and type parameters
        timestamp = self.request.query_params.get('timestamp')
        pagination_type = self.request.query_params.get('type', 'old')  # Default to 'old'
        
        if timestamp:
            try:
                # Parse timestamp
                ts = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                
                if pagination_type == 'new':
                    # Get posts newer than timestamp
                    queryset = base_queryset.filter(created_at__gt=ts).order_by('created_at')
                else:  # 'old'
                    # Get posts older than timestamp
                    queryset = base_queryset.filter(created_at__lt=ts).order_by('-created_at')
            except ValueError:
                # Invalid timestamp, return latest posts
                queryset = base_queryset.order_by('-created_at')
        else:
            # No timestamp, return latest posts
            queryset = base_queryset.order_by('-created_at')
        
        # Apply gender-based distribution for male users
        if user.gender == 'male':
            queryset = self._apply_gender_distribution(queryset)
        
        return queryset

    def _apply_gender_distribution(self, queryset):
        """
        For male users, ensure 70% of posts are from female users.
        """
        # Get all posts
        all_posts = list(queryset)
        
        if not all_posts:
            return queryset
        
        # Separate posts by gender
        female_posts = []
        male_posts = []
        other_posts = []
        
        for post in all_posts:
            if post.user.gender == 'female':
                female_posts.append(post)
            elif post.user.gender == 'male':
                male_posts.append(post)
            else:
                other_posts.append(post)
        
        # Calculate target distribution
        total_posts = len(all_posts)
        target_female_count = int(total_posts * 0.7)  # 70% female posts
        target_male_count = total_posts - target_female_count  # Remaining for male/other
        
        # If we have enough female posts, prioritize them
        if len(female_posts) >= target_female_count:
            # Take 70% female posts
            selected_female = random.sample(female_posts, target_female_count)
            # Take remaining from male/other posts
            remaining_posts = male_posts + other_posts
            if len(remaining_posts) >= target_male_count:
                selected_others = random.sample(remaining_posts, target_male_count)
            else:
                selected_others = remaining_posts
            
            # Combine and maintain chronological order
            selected_posts = selected_female + selected_others
            selected_posts.sort(key=lambda x: x.created_at, reverse=True)
            
            return selected_posts
        else:
            # Not enough female posts, return all available posts
            return all_posts

class PostDetailView(generics.RetrieveAPIView):
    """
    Get details of a specific post.
    
    GET: Retrieve detailed information about a single post
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [AllowAny]
    lookup_field = "id"

# ------------------- Comments -------------------
class CommentCreateView(generics.CreateAPIView):
    """
    Create a new comment on a post.
    
    POST: Create a new comment or reply to an existing comment
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostCommentsView(generics.ListAPIView):
    """
    Get all top-level comments for a specific post.
    
    GET: Retrieve a paginated list of comments for a post (excludes replies)
    """
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination

    permission_classes = [AllowAny]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs["post_id"], parent__isnull=True).order_by("created_at")

class CommentRepliesView(generics.ListAPIView):
    """
    Get all replies to a specific comment.
    
    GET: Retrieve a paginated list of replies to a comment
    """
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination

    permission_classes = [AllowAny]

    def get_queryset(self):
        return Comment.objects.filter(parent_id=self.kwargs["comment_id"]).order_by("created_at")

# ------------------- Followers -------------------
class FollowerView(APIView):
    """
    Follow or unfollow a user.
    
    POST: Follow a user
    DELETE: Unfollow a user
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Follow a user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID, description='ID of user to follow')
            },
            required=['user_id']
        ),
        responses={
            200: openapi.Response('Success', examples={'application/json': {'status': 'Now following username'}}),
            400: openapi.Response('Bad Request', examples={'application/json': {'error': 'Cannot follow yourself'}}),
            404: openapi.Response('Not Found', examples={'application/json': {'error': 'User not found'}})
        }
    )
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

    @swagger_auto_schema(
        operation_description="Unfollow a user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID, description='ID of user to unfollow')
            },
            required=['user_id']
        ),
        responses={
            200: openapi.Response('Success', examples={'application/json': {'status': 'Unfollowed username'}}),
            404: openapi.Response('Not Found', examples={'application/json': {'error': 'User not found'}})
        }
    )
    def delete(self, request):
        user_id = request.data.get("user_id")
        try:
            user_to_unfollow = User.objects.get(id=user_id)
            Follower.objects.filter(user=user_to_unfollow, follower=request.user).delete()
            return Response({"status": f"Unfollowed {user_to_unfollow.username}"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)


class FollowStatusView(APIView):
    """
    Check if the current user is following a specific user.
    
    GET: Check follow status
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Check if current user is following a specific user",
        manual_parameters=[
            openapi.Parameter(
                'user_id',
                openapi.IN_QUERY,
                description="ID of user to check follow status for",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID,
                required=True
            )
        ],
        responses={
            200: openapi.Response('Follow Status', examples={
                'application/json': {
                    'is_following': True,
                    'user_id': '123e4567-e89b-12d3-a456-426614174000',
                    'username': 'johndoe'
                }
            }),
            400: openapi.Response('Bad Request', examples={
                'application/json': {'error': 'user_id parameter is required'}
            }),
            404: openapi.Response('Not Found', examples={
                'application/json': {'error': 'User not found'}
            }),
            401: openapi.Response('Unauthorized', examples={
                'application/json': {'detail': 'Authentication credentials were not provided.'}
            })
        }
    )
    def get(self, request):
        user_id = request.GET.get('user_id')
        
        if not user_id:
            return Response({"error": "user_id parameter is required"}, status=400)
        
        try:
            target_user = User.objects.get(id=user_id)
            
            # Check if current user is following the target user
            is_following = Follower.objects.filter(
                user=target_user,
                follower=request.user
            ).exists()
            
            return Response({
                "is_following": is_following,
                "user_id": str(target_user.id),
                "username": target_user.username,
                "full_name": target_user.full_name
            })
            
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)


class FollowersListView(generics.ListAPIView):
    """
    Get list of users following a specific user.
    
    GET: Retrieve a paginated list of users who follow the specified user
    """
    serializer_class = UserProfileSerializer
    pagination_class = StandardResultsSetPagination

    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.filter(following__user_id=self.kwargs["user_id"])

class FollowingListView(generics.ListAPIView):
    """
    Get list of users that a specific user follows.
    
    GET: Retrieve a paginated list of users that the specified user follows
    """
    serializer_class = UserProfileSerializer
    pagination_class = StandardResultsSetPagination

    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.filter(followers__follower_id=self.kwargs["user_id"])

# ------------------- Post Reactions -------------------
class PostReactionView(APIView):
    """
    Add or remove reactions to a post.
    
    POST: Add a reaction (like/comment) to a post
    DELETE: Remove a reaction from a post
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add a reaction to a post",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'post_id': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID, description='ID of the post'),
                'reaction_type': openapi.Schema(type=openapi.TYPE_STRING, enum=['like', 'comment'], description='Type of reaction')
            },
            required=['post_id', 'reaction_type']
        ),
        responses={
            200: openapi.Response('Success', examples={'application/json': {'status': 'like added'}}),
            404: openapi.Response('Not Found', examples={'application/json': {'error': 'Post not found'}})
        }
    )
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

    @swagger_auto_schema(
        operation_description="Remove a reaction from a post",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'post_id': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID, description='ID of the post'),
                'reaction_type': openapi.Schema(type=openapi.TYPE_STRING, enum=['like', 'comment'], description='Type of reaction')
            },
            required=['post_id', 'reaction_type']
        ),
        responses={
            200: openapi.Response('Success', examples={'application/json': {'status': 'like removed'}})
        }
    )
    def delete(self, request):
        post_id = request.data.get("post_id")
        reaction_type = request.data.get("reaction_type")
        PostReaction.objects.filter(user=request.user, post_id=post_id, reaction_type=reaction_type).delete()
        return Response({"status": f"{reaction_type} removed"})

class PostLikesListView(generics.ListAPIView):
    """
    Get list of users who liked a specific post.
    
    GET: Retrieve a paginated list of users who liked the specified post
    """
    serializer_class = UserProfileSerializer
    pagination_class = StandardResultsSetPagination

    permission_classes = [AllowAny]

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        user_ids = PostReaction.objects.filter(post_id=post_id, reaction_type='like').values_list("user_id", flat=True)
        return User.objects.filter(id__in=user_ids)

# ------------------- Profiles -------------------
class UserProfileView(generics.RetrieveAPIView):
    """
    Get detailed profile information for a user.
    
    GET: Retrieve detailed profile information for the specified user
    """
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    lookup_field = "id"

# ------------------- Search -------------------
class SearchPostsView(generics.ListAPIView):
    """
    Search for posts by text content.
    
    GET: Search for posts containing the specified text (case-insensitive)
    Query Parameters: ?q=search_term
    """
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination

    permission_classes = [AllowAny]

    permission_classes = [AllowAny]

    def get_queryset(self):
        q = self.request.query_params.get("q", "")
        return Post.objects.filter(text__icontains=q).order_by('-created_at')[:20]

class SearchUsersView(generics.ListAPIView):
    """
    Search for users by username or full name.
    
    GET: Search for users by username or full name (case-insensitive)
    Query Parameters: ?q=search_term
    """
    serializer_class = UserProfileSerializer
    pagination_class = StandardResultsSetPagination

    permission_classes = [AllowAny]

    def get_queryset(self):
        q = self.request.query_params.get("q", "")
        return User.objects.filter(Q(username__icontains=q) | Q(full_name__icontains=q))
