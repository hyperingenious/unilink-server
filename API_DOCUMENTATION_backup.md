# Unilink API Documentation

A comprehensive social media platform API built with Django REST Framework.

## Table of Contents
- [Authentication](#authentication)
- [User Management](#user-management)
- [Social Features](#social-features)
- [Error Codes](#error-codes)
- [Data Models](#data-models)

---

## Authentication

All protected endpoints require JWT authentication via the `Authorization` header:
```
Authorization: Bearer <access_token>
```

### Getting Access Token
1. Register a new account
2. Verify your email
3. Login to get access and refresh tokens

---

## User Management

### 1. Register User
**POST** `/api/auth/signup/`

Create a new user account. Account will be inactive until email verification.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "password": "secure_password123"
}
```

**Response (201 Created):**
```json
{
  "message": "User created. Check email for verification link."
}
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "password": "secure_password123"
  }'
```

---

### 2. Login User
**POST** `/api/auth/login/`

Authenticate user and return JWT tokens.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password123"
}
```

**Response (200 OK):**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "bio": "",
    "profile_photo": null
  }
}
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secure_password123"
  }'
```

---

### 3. Verify Email
**GET** `/api/auth/verify-email/?token=<verification_token>`

Verify user email using token sent via email.

**Query Parameters:**
- `token` (required): Email verification token

**Response (200 OK):**
```json
{
  "status": "Email verified"
}
```

**cURL Example:**
```bash
curl -X GET "http://127.0.0.1:8000/api/auth/verify-email/?token=your_verification_token"
```

---

### 4. Delete Account
**DELETE** `/api/auth/delete/`

Permanently delete the authenticated user's account.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "status": "account deleted"
}
```

**cURL Example:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/auth/delete/ \
  -H "Authorization: Bearer <access_token>"
```

---

## Social Features

### Posts

#### 1. List All Posts
**GET** `/api/social/posts/`

Get paginated list of all posts (newest first).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page` (optional): Page number for pagination

**Response (200 OK):**
```json
{
  "count": 25,
  "next": "http://127.0.0.1:8000/api/social/posts/?page=2",
  "previous": null,
  "results": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "user": {
        "id": "456e7890-e89b-12d3-a456-426614174000",
        "email": "author@example.com",
        "username": "author",
        "full_name": "Author Name",
        "bio": "Bio text",
        "profile_photo": "https://example.com/photo.jpg"
      },
      "text": "This is a post content",
      "image_url": "https://example.com/image.jpg",
      "created_at": "2024-01-15T10:30:00Z",
      "comments": [],
      "reactions_count": 5
    }
  ]
}
```

**cURL Example:**
```bash
curl -X GET http://127.0.0.1:8000/api/social/posts/ \
  -H "Authorization: Bearer <access_token>"
```

---

#### 2. Create Post
**POST** `/api/social/posts/`

Create a new post.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "text": "This is my new post!",
  "image_url": "https://example.com/image.jpg"
}
```

**Response (201 Created):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user": {
    "id": "456e7890-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "bio": "",
    "profile_photo": null
  },
  "text": "This is my new post!",
  "image_url": "https://example.com/image.jpg",
  "created_at": "2024-01-15T10:30:00Z",
  "comments": [],
  "reactions_count": 0
}
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/social/posts/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This is my new post!",
    "image_url": "https://example.com/image.jpg"
  }'
```

---

#### 3. Get User Posts
**GET** `/api/social/users/{user_id}/posts/`

Get all posts by a specific user.

**Path Parameters:**
- `user_id` (required): UUID of the user

**Query Parameters:**
- `page` (optional): Page number for pagination

**Response (200 OK):**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "user": {
        "id": "456e7890-e89b-12d3-a456-426614174000",
        "username": "johndoe",
        "full_name": "John Doe",
        "bio": "Bio text",
        "profile_photo": "https://example.com/photo.jpg"
      },
      "text": "User's post content",
      "image_url": "https://example.com/image.jpg",
      "created_at": "2024-01-15T10:30:00Z",
      "comments": [],
      "reactions_count": 3
    }
  ]
}
```

**cURL Example:**
```bash
curl -X GET http://127.0.0.1:8000/api/social/users/456e7890-e89b-12d3-a456-426614174000/posts/
```

---

#### 4. Get Personalized Feed
**GET** `/api/social/feed/`

Get personalized feed (posts from followed users + own posts).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page` (optional): Page number for pagination

**Response (200 OK):**
```json
{
  "count": 15,
  "next": "http://127.0.0.1:8000/api/social/feed/?page=2",
  "previous": null,
  "results": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "user": {
        "id": "456e7890-e89b-12d3-a456-426614174000",
        "username": "followed_user",
        "full_name": "Followed User",
        "bio": "Bio text",
        "profile_photo": "https://example.com/photo.jpg"
      },
      "text": "Post from someone you follow",
      "image_url": null,
      "created_at": "2024-01-15T10:30:00Z",
      "comments": [],
      "reactions_count": 8
    }
  ]
}
```

**cURL Example:**
```bash
curl -X GET http://127.0.0.1:8000/api/social/feed/ \
  -H "Authorization: Bearer <access_token>"
```

---

#### 5. Get Post Details
**GET** `/api/social/posts/{id}/`

Get details of a specific post.

**Path Parameters:**
- `id` (required): UUID of the post

**Response (200 OK):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user": {
    "id": "456e7890-e89b-12d3-a456-426614174000",
    "username": "johndoe",
    "full_name": "John Doe",
    "bio": "Bio text",
    "profile_photo": "https://example.com/photo.jpg"
  },
  "text": "Detailed post content",
  "image_url": "https://example.com/image.jpg",
  "created_at": "2024-01-15T10:30:00Z",
  "comments": [
    {
      "id": "789e0123-e89b-12d3-a456-426614174000",
      "user": {
        "id": "012e3456-e89b-12d3-a456-426614174000",
        "username": "commenter",
        "full_name": "Comment Author",
        "bio": "",
        "profile_photo": null
      },
      "post": "123e4567-e89b-12d3-a456-426614174000",
      "parent": null,
      "text": "This is a comment",
      "created_at": "2024-01-15T11:00:00Z",
      "subcomments": []
    }
  ],
  "reactions_count": 12
}
```

**cURL Example:**
```bash
curl -X GET http://127.0.0.1:8000/api/social/posts/123e4567-e89b-12d3-a456-426614174000/
```

---

### Comments

#### 1. Create Comment
**POST** `/api/social/comments/`

Create a new comment on a post or reply to an existing comment.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "post_id": "123e4567-e89b-12d3-a456-426614174000",
  "text": "This is a comment",
  "parent": "789e0123-e89b-12d3-a456-426614174000"
}
```

**Response (201 Created):**
```json
{
  "id": "789e0123-e89b-12d3-a456-426614174000",
  "user": {
    "id": "456e7890-e89b-12d3-a456-426614174000",
    "username": "johndoe",
    "full_name": "John Doe",
    "bio": "",
    "profile_photo": null
  },
  "post": "123e4567-e89b-12d3-a456-426614174000",
  "parent": null,
  "text": "This is a comment",
  "created_at": "2024-01-15T11:00:00Z",
  "subcomments": []
}
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/social/comments/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "post_id": "123e4567-e89b-12d3-a456-426614174000",
    "text": "This is a comment"
  }'
```

---

#### 2. Get Post Comments
**GET** `/api/social/posts/{post_id}/comments/`

Get all top-level comments for a specific post.

**Path Parameters:**
- `post_id` (required): UUID of the post

**Query Parameters:**
- `page` (optional): Page number for pagination

**Response (200 OK):**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "789e0123-e89b-12d3-a456-426614174000",
      "user": {
        "id": "456e7890-e89b-12d3-a456-426614174000",
        "username": "commenter",
        "full_name": "Comment Author",
        "bio": "",
        "profile_photo": null
      },
      "post": "123e4567-e89b-12d3-a456-426614174000",
      "parent": null,
      "text": "This is a top-level comment",
      "created_at": "2024-01-15T11:00:00Z",
      "subcomments": [
        {
          "id": "345e6789-e89b-12d3-a456-426614174000",
          "user": {
            "id": "678e9012-e89b-12d3-a456-426614174000",
            "username": "replier",
            "full_name": "Reply Author",
            "bio": "",
            "profile_photo": null
          },
          "post": "123e4567-e89b-12d3-a456-426614174000",
          "parent": "789e0123-e89b-12d3-a456-426614174000",
          "text": "This is a reply",
          "created_at": "2024-01-15T11:15:00Z",
          "subcomments": []
        }
      ]
    }
  ]
}
```

**cURL Example:**
```bash
curl -X GET http://127.0.0.1:8000/api/social/posts/123e4567-e89b-12d3-a456-426614174000/comments/
```

---

#### 3. Get Comment Replies
**GET** `/api/social/comments/{comment_id}/replies/`

Get all replies to a specific comment.

**Path Parameters:**
- `comment_id` (required): UUID of the comment

**Query Parameters:**
- `page` (optional): Page number for pagination

**Response (200 OK):**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "345e6789-e89b-12d3-a456-426614174000",
      "user": {
        "id": "678e9012-e89b-12d3-a456-426614174000",
        "username": "replier",
        "full_name": "Reply Author",
        "bio": "",
        "profile_photo": null
      },
      "post": "123e4567-e89b-12d3-a456-426614174000",
      "parent": "789e0123-e89b-12d3-a456-426614174000",
      "text": "This is a reply",
      "created_at": "2024-01-15T11:15:00Z",
      "subcomments": []
    }
  ]
}
```

**cURL Example:**
```bash
curl -X GET http://127.0.0.1:8000/api/social/comments/789e0123-e89b-12d3-a456-426614174000/replies/
```

---

### Followers & Following

#### 1. Follow User
**POST** `/api/social/follow/`

Follow a user.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "user_id": "456e7890-e89b-12d3-a456-426614174000"
}
```

**Response (200 OK):**
```json
{
  "status": "Now following johndoe"
}
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/social/follow/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "456e7890-e89b-12d3-a456-426614174000"
  }'
```

---

#### 2. Unfollow User
**DELETE** `/api/social/follow/`

Unfollow a user.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "user_id": "456e7890-e89b-12d3-a456-426614174000"
}
```

**Response (200 OK):**
```json
{
  "status": "Unfollowed johndoe"
}
```

**cURL Example:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/social/follow/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "456e7890-e89b-12d3-a456-426614174000"
  }'
```

---

#### 3. Get User Followers
**GET** `/api/social/users/{user_id}/followers/`

Get list of users following a specific user.

**Path Parameters:**
- `user_id` (required): UUID of the user

**Query Parameters:**
- `page` (optional): Page number for pagination

**Response (200 OK):**
```json
{
  "count": 25,
  "next": "http://127.0.0.1:8000/api/social/users/456e7890-e89b-12d3-a456-426614174000/followers/?page=2",
  "previous": null,
  "results": [
    {
      "id": "789e0123-e89b-12d3-a456-426614174000",
      "username": "follower1",
      "full_name": "Follower One",
      "bio": "Bio text",
      "profile_photo": "https://example.com/photo.jpg",
      "followers_count": 10,
      "following_count": 5,
      "posts_count": 20
    }
  ]
}
```

**cURL Example:**
```bash
curl -X GET http://127.0.0.1:8000/api/social/users/456e7890-e89b-12d3-a456-426614174000/followers/
```

---

#### 4. Get User Following
**GET** `/api/social/users/{user_id}/following/`

Get list of users that a specific user follows.

**Path Parameters:**
- `user_id` (required): UUID of the user

**Query Parameters:**
- `page` (optional): Page number for pagination

**Response (200 OK):**
```json
{
  "count": 15,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "345e6789-e89b-12d3-a456-426614174000",
      "username": "following1",
      "full_name": "Following One",
      "bio": "Bio text",
      "profile_photo": "https://example.com/photo.jpg",
      "followers_count": 50,
      "following_count": 30,
      "posts_count": 100
    }
  ]
}
```

**cURL Example:**
```bash
curl -X GET http://127.0.0.1:8000/api/social/users/456e7890-e89b-12d3-a456-426614174000/following/
```

---

### Reactions

#### 1. Add Reaction
**POST** `/api/social/react/`

Add a reaction (like/comment) to a post.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "post_id": "123e4567-e89b-12d3-a456-426614174000",
  "reaction_type": "like"
}
```

**Response (200 OK):**
```json
{
  "status": "like added"
}
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/social/react/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "post_id": "123e4567-e89b-12d3-a456-426614174000",
    "reaction_type": "like"
  }'
```

---

#### 2. Remove Reaction
**DELETE** `/api/social/react/`

Remove a reaction from a post.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "post_id": "123e4567-e89b-12d3-a456-426614174000",
  "reaction_type": "like"
}
```

**Response (200 OK):**
```json
{
  "status": "like removed"
}
```

**cURL Example:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/social/react/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "post_id": "123e4567-e89b-12d3-a456-426614174000",
    "reaction_type": "like"
  }'
```

---

#### 3. Get Post Likes
**GET** `/api/social/posts/{post_id}/likes/`

Get list of users who liked a specific post.

**Path Parameters:**
- `post_id` (required): UUID of the post

**Query Parameters:**
- `page` (optional): Page number for pagination

**Response (200 OK):**
```json
{
  "count": 8,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "789e0123-e89b-12d3-a456-426614174000",
      "username": "liker1",
      "full_name": "Liker One",
      "bio": "Bio text",
      "profile_photo": "https://example.com/photo.jpg",
      "followers_count": 15,
      "following_count": 8,
      "posts_count": 25
    }
  ]
}
```

**cURL Example:**
```bash
curl -X GET http://127.0.0.1:8000/api/social/posts/123e4567-e89b-12d3-a456-426614174000/likes/
```

---

### User Profiles

#### 1. Get User Profile
**GET** `/api/social/users/{id}/profile/`

Get detailed profile information for a user.

**Path Parameters:**
- `id` (required): UUID of the user

**Response (200 OK):**
```json
{
  "id": "456e7890-e89b-12d3-a456-426614174000",
  "username": "johndoe",
  "full_name": "John Doe",
  "bio": "Software developer and tech enthusiast",
  "profile_photo": "https://example.com/profile.jpg",
  "followers_count": 150,
  "following_count": 75,
  "posts_count": 200
}
```

**cURL Example:**
```bash
curl -X GET http://127.0.0.1:8000/api/social/users/456e7890-e89b-12d3-a456-426614174000/profile/
```

---

### Search

#### 1. Search Posts
**GET** `/api/social/search/posts/`

Search for posts by text content.

**Query Parameters:**
- `q` (required): Search term
- `page` (optional): Page number for pagination

**Response (200 OK):**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "user": {
        "id": "456e7890-e89b-12d3-a456-426614174000",
        "username": "johndoe",
        "full_name": "John Doe",
        "bio": "",
        "profile_photo": null
      },
      "text": "This post contains the search term",
      "image_url": null,
      "created_at": "2024-01-15T10:30:00Z",
      "comments": [],
      "reactions_count": 3
    }
  ]
}
```

**cURL Example:**
```bash
curl -X GET "http://127.0.0.1:8000/api/social/search/posts/?q=django"
```

---

#### 2. Search Users
**GET** `/api/social/search/users/`

Search for users by username or full name.

**Query Parameters:**
- `q` (required): Search term
- `page` (optional): Page number for pagination

**Response (200 OK):**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "456e7890-e89b-12d3-a456-426614174000",
      "username": "johndoe",
      "full_name": "John Doe",
      "bio": "Software developer",
      "profile_photo": "https://example.com/profile.jpg",
      "followers_count": 150,
      "following_count": 75,
      "posts_count": 200
    }
  ]
}
```

**cURL Example:**
```bash
curl -X GET "http://127.0.0.1:8000/api/social/search/users/?q=john"
```

---

## Error Codes

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid request data |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Access denied |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error - Server error |

### Common Error Responses

**400 Bad Request:**
```json
{
  "error": "Validation errors",
  "field_errors": {
    "email": ["This field is required."],
    "username": ["This field is required."]
  }
}
```

**401 Unauthorized:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**403 Forbidden:**
```json
{
  "error": "Email not verified"
}
```

**404 Not Found:**
```json
{
  "error": "User not found"
}
```

---

## Data Models

### User Model
```json
{
  "id": "UUID (Primary Key)",
  "email": "string (unique, required)",
  "username": "string (unique, max 50 chars, required)",
  "full_name": "string (max 150 chars, required)",
  "bio": "string (optional, default: '')",
  "profile_photo": "URL (optional)",
  "is_active": "boolean (default: false)",
  "is_staff": "boolean (default: false)",
  "date_joined": "datetime (auto-generated)"
}
```

### Post Model
```json
{
  "id": "UUID (Primary Key)",
  "user": "User (Foreign Key)",
  "text": "string (optional)",
  "image_url": "URL (optional)",
  "created_at": "datetime (auto-generated)"
}
```

### Comment Model
```json
{
  "id": "UUID (Primary Key)",
  "user": "User (Foreign Key)",
  "post": "Post (Foreign Key)",
  "parent": "Comment (Self-referencing, optional for replies)",
  "text": "string (required)",
  "created_at": "datetime (auto-generated)"
}
```

### Follower Model
```json
{
  "id": "UUID (Primary Key)",
  "user": "User (Foreign Key - being followed)",
  "follower": "User (Foreign Key - who follows)"
}
```

### PostReaction Model
```json
{
  "id": "UUID (Primary Key)",
  "user": "User (Foreign Key)",
  "post": "Post (Foreign Key)",
  "reaction_type": "string (choices: 'like', 'comment')"
}
```

---

## Pagination

Most list endpoints support pagination with 20 items per page by default.

**Pagination Response Format:**
```json
{
  "count": 100,
  "next": "http://127.0.0.1:8000/api/endpoint/?page=2",
  "previous": null,
  "results": [...]
}
```

**Query Parameters:**
- `page`: Page number (starts from 1)

---

## Rate Limiting

Currently no rate limiting is implemented. Consider implementing rate limiting for production use.

---

## Base URL

All API endpoints are prefixed with:
```
http://127.0.0.1:8000/api/
```

For production, replace with your domain:
```
https://yourdomain.com/api/
```

---

## Authentication Flow

1. **Register**: `POST /api/auth/signup/`
2. **Verify Email**: Click link in email or `GET /api/auth/verify-email/?token=...`
3. **Login**: `POST /api/auth/login/` to get JWT tokens
4. **Use Access Token**: Include in `Authorization: Bearer <token>` header for protected endpoints
5. **Refresh Token**: Use refresh token to get new access token when expired

---

## JWT Token Details

- **Access Token**: Valid for 7 days
- **Refresh Token**: Valid for 30 days
- **Algorithm**: HS256
- **Header Format**: `Authorization: Bearer <access_token>`

---

## Notes

- All timestamps are in ISO 8601 format (UTC)
- UUIDs are used for all primary keys
- Email verification is required before account activation
- Users cannot follow themselves
- Comments support nested replies (unlimited depth)
- Search is case-insensitive
- Image URLs should be valid URLs
- All text fields support Unicode characters
