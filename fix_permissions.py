import re

# Read the file
with open('social/views.py', 'r') as f:
    content = f.read()

# Views that should be public (no authentication required)
public_views = [
    'UserPostsView',
    'PostDetailView', 
    'PostCommentsView',
    'CommentRepliesView',
    'FollowersListView',
    'FollowingListView',
    'PostLikesListView',
    'UserProfileView',
    'SearchPostsView',
    'SearchUsersView'
]

# Add permission_classes = [AllowAny] to public views
for view in public_views:
    pattern = f'(class {view}\\([^)]+\\):.*?)(    def|    @)'
    replacement = r'\1    permission_classes = [AllowAny]\n\n\2'
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Write back to file
with open('social/views.py', 'w') as f:
    f.write(content)

print("Fixed permissions for public views")
