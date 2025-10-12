from django.db import models
from django.conf import settings
import uuid

User = settings.AUTH_USER_MODEL

# ------------------- Post -------------------
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    text = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user}"

# ------------------- Comment -------------------
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="subcomments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on Post {self.post.id}"

# ------------------- Follower -------------------
class Follower(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")  # being followed
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")  # who follows

    class Meta:
        unique_together = ('user', 'follower')

    def __str__(self):
        return f"{self.follower} follows {self.user}"

# ------------------- Post Reaction -------------------
class PostReaction(models.Model):
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('comment', 'Comment')  # optional
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_reactions")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reactions")
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)

    class Meta:
        unique_together = ('user', 'post', 'reaction_type')

    def __str__(self):
        return f"{self.user} reacted {self.reaction_type} on {self.post.id}"
