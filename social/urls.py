from django.urls import path
from .views import (
    PostListCreateView, CommentCreateView, FollowerView, PostReactionView,
    UserPostsView, FeedView, PostDetailView, PostCommentsView, CommentRepliesView,
    FollowersListView, FollowingListView, PostLikesListView, UserProfileView,
    SearchPostsView, SearchUsersView
)

urlpatterns = [
    # Basic CRUD
    path("posts/", PostListCreateView.as_view(), name="posts"),
    path("comments/", CommentCreateView.as_view(), name="comments"),
    path("follow/", FollowerView.as_view(), name="follow"),
    path("react/", PostReactionView.as_view(), name="react"),

    # Extended social features
    path("users/<uuid:user_id>/posts/", UserPostsView.as_view()),
    path("feed/", FeedView.as_view()),
    path("posts/<uuid:id>/", PostDetailView.as_view()),
    path("posts/<uuid:post_id>/comments/", PostCommentsView.as_view()),
    path("comments/<uuid:comment_id>/replies/", CommentRepliesView.as_view()),

    path("users/<uuid:user_id>/followers/", FollowersListView.as_view()),
    path("users/<uuid:user_id>/following/", FollowingListView.as_view()),
    path("posts/<uuid:post_id>/likes/", PostLikesListView.as_view()),
    path("users/<uuid:id>/profile/", UserProfileView.as_view()),

    path("search/posts/", SearchPostsView.as_view()),
    path("search/users/", SearchUsersView.as_view()),
]
