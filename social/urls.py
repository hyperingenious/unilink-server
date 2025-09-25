from django.urls import path
from .views import (
    PostListCreateView, CommentCreateView, FollowerView, PostReactionView,
    UserPostsView, FeedView, PostDetailView, PostCommentsView, CommentRepliesView,
    FollowersListView, FollowingListView, PostLikesListView, UserProfileView,
    SearchPostsView, SearchUsersView
)

"""
API Endpoints Documentation for Social Features

This module defines all the social media endpoints for the Unilink platform.
All endpoints require JWT authentication unless otherwise specified.

AUTHENTICATION:
- All endpoints require JWT token in Authorization header: "Bearer <token>"
- Token can be obtained from /api/auth/login/ endpoint

PAGINATION:
- Most list endpoints support pagination with 20 items per page
- Use ?page=N query parameter to navigate pages

RESPONSE FORMATS:
- Success responses typically return JSON with data
- Error responses return JSON with 'error' field
- All timestamps are in ISO format

"""

urlpatterns = [
    # ==================== BASIC CRUD OPERATIONS ====================
    
    # POSTS ENDPOINTS
    # GET /posts/ - List all posts (paginated, newest first)
    # POST /posts/ - Create a new post
    # Authentication: Required
    # Request Body (POST): {"text": "string", "image_url": "string (optional)"}
    # Response: List of posts or created post object
    path("posts/", PostListCreateView.as_view(), name="posts"),
    
    # COMMENTS ENDPOINTS  
    # POST /comments/ - Create a new comment
    # Authentication: Required
    # Request Body: {"post_id": "uuid", "text": "string", "parent": "uuid (optional for replies)"}
    # Response: Created comment object
    path("comments/", CommentCreateView.as_view(), name="comments"),
    
    # FOLLOW/UNFOLLOW ENDPOINTS
    # POST /follow/ - Follow a user
    # DELETE /follow/ - Unfollow a user  
    # Authentication: Required
    # Request Body: {"user_id": "uuid"}
    # Response: Success/error message
    path("follow/", FollowerView.as_view(), name="follow"),
    
    # REACTIONS ENDPOINTS
    # POST /react/ - Add reaction to post (like/comment)
    # DELETE /react/ - Remove reaction from post
    # Authentication: Required
    # Request Body: {"post_id": "uuid", "reaction_type": "like|comment"}
    # Response: Success/error message
    path("react/", PostReactionView.as_view(), name="react"),

    # ==================== EXTENDED SOCIAL FEATURES ====================
    
    # USER POSTS
    # GET /users/{user_id}/posts/ - Get all posts by a specific user
    # Authentication: Not required
    # Parameters: user_id (UUID) in URL path
    # Response: Paginated list of posts by the user
    path("users/<uuid:user_id>/posts/", UserPostsView.as_view()),
    
    # FEED
    # GET /feed/ - Get personalized feed (posts from followed users + own posts)
    # Authentication: Required
    # Response: Paginated list of posts from followed users and self
    path("feed/", FeedView.as_view()),
    
    # POST DETAILS
    # GET /posts/{id}/ - Get details of a specific post
    # Authentication: Not required
    # Parameters: id (UUID) in URL path
    # Response: Single post object with full details
    path("posts/<uuid:id>/", PostDetailView.as_view()),
    
    # POST COMMENTS
    # GET /posts/{post_id}/comments/ - Get all top-level comments for a post
    # Authentication: Not required
    # Parameters: post_id (UUID) in URL path
    # Response: Paginated list of comments (excludes replies)
    path("posts/<uuid:post_id>/comments/", PostCommentsView.as_view()),
    
    # COMMENT REPLIES
    # GET /comments/{comment_id}/replies/ - Get all replies to a specific comment
    # Authentication: Not required
    # Parameters: comment_id (UUID) in URL path
    # Response: Paginated list of comment replies
    path("comments/<uuid:comment_id>/replies/", CommentRepliesView.as_view()),

    # ==================== FOLLOWERS & FOLLOWING ====================
    
    # FOLLOWERS LIST
    # GET /users/{user_id}/followers/ - Get list of users following a specific user
    # Authentication: Not required
    # Parameters: user_id (UUID) in URL path
    # Response: Paginated list of user profiles who follow the specified user
    path("users/<uuid:user_id>/followers/", FollowersListView.as_view()),
    
    # FOLLOWING LIST
    # GET /users/{user_id}/following/ - Get list of users that a specific user follows
    # Authentication: Not required
    # Parameters: user_id (UUID) in URL path
    # Response: Paginated list of user profiles that the specified user follows
    path("users/<uuid:user_id>/following/", FollowingListView.as_view()),
    
    # POST LIKES
    # GET /posts/{post_id}/likes/ - Get list of users who liked a specific post
    # Authentication: Not required
    # Parameters: post_id (UUID) in URL path
    # Response: Paginated list of user profiles who liked the post
    path("posts/<uuid:post_id>/likes/", PostLikesListView.as_view()),
    
    # USER PROFILE
    # GET /users/{id}/profile/ - Get detailed profile information for a user
    # Authentication: Not required
    # Parameters: id (UUID) in URL path
    # Response: User profile object with detailed information
    path("users/<uuid:id>/profile/", UserProfileView.as_view()),

    # ==================== SEARCH FUNCTIONALITY ====================
    
    # SEARCH POSTS
    # GET /search/posts/ - Search for posts by text content
    # Authentication: Not required
    # Query Parameters: ?q=search_term
    # Response: Paginated list of posts matching search term (max 20 results)
    path("search/posts/", SearchPostsView.as_view()),
    
    # SEARCH USERS
    # GET /search/users/ - Search for users by username or full name
    # Authentication: Not required
    # Query Parameters: ?q=search_term
    # Response: Paginated list of user profiles matching search term
    path("search/users/", SearchUsersView.as_view()),
]