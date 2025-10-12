# Unilink API Documentation

A comprehensive social media platform API built with Django REST Framework, designed for university students to connect, share content, and build communities.

## 🚀 Platform Overview

Unilink is a feature-rich social media platform specifically designed for university students. The platform enables users to:

- **📱 Share Content**: Create posts with text, images, and videos
- **💬 Engage**: Comment on posts with unlimited threaded replies
- **👥 Connect**: Follow other students and build networks
- **📊 Interact**: React to posts and show appreciation
- **🔍 Discover**: Find new content and connect with peers
- **📈 Track**: Monitor engagement and community metrics

## 🏗️ Architecture & Features

### **Core Technologies**
- **Backend**: Django REST Framework
- **Authentication**: JWT (JSON Web Tokens)
- **File Storage**: Appwrite Cloud Storage
- **Database**: PostgreSQL (recommended) / SQLite (development)
- **API Style**: RESTful API with comprehensive documentation

### **Key Features**
- ✅ **User Registration & Authentication** with email verification
- ✅ **Rich Media Posts** supporting text, images, and videos
- ✅ **Threaded Comments** with unlimited nesting depth
- ✅ **Follow System** for building user networks
- ✅ **Personalized Feeds** with smart content distribution
- ✅ **Reaction System** for post engagement
- ✅ **Search Functionality** for posts and users
- ✅ **File Upload** for media content
- ✅ **Pagination** for optimal performance
- ✅ **Gender-Balanced Feeds** for enhanced user experience

### **API Characteristics**
- **Authentication**: JWT-based authentication for secure access
- **Pagination**: Standard and timestamp-based pagination
- **Error Handling**: Comprehensive error responses with detailed messages
- **Validation**: Robust input validation and sanitization
- **Performance**: Optimized queries and efficient data structures

## 📚 Table of Contents
- [Authentication](#authentication) - User registration, login, and token management
- [User Management](#user-management) - Profile management and user operations
- [Social Features](#social-features) - Posts, comments, follows, and reactions
- [Error Codes](#error-codes) - Comprehensive error handling guide
- [Data Models](#data-models) - Complete data structure documentation

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
  "password": "secure_password123",
  "institute_name": "University of Technology",
  "dob": "1995-06-15",
  "dept_course": "Computer Science",
  "gender": "male",
  "register_number": "CS2024001",
  "profile_photo": "https://example.com/profile.jpg"
}
```

**Note:** `profile_photo` is optional. If not provided, it will be `null`.

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
    "password": "secure_password123",
    "institute_name": "University of Technology",
    "dob": "1995-06-15",
    "dept_course": "Computer Science",
    "gender": "male",
    "register_number": "CS2024001"
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
    "profile_photo": null,
    "institute_name": "University of Technology",
    "dob": "1995-06-15",
    "dept_course": "Computer Science",
    "gender": "male",
    "register_number": "CS2024001"
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

### 5. Edit User Profile
**PATCH** `/api/auth/profile/edit/`

Update user profile information. **Authentication required.**

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "full_name": "Updated Full Name",
  "bio": "Updated bio text",
  "profile_photo": "https://example.com/new-profile.jpg",
  "institute_name": "Updated University",
  "dept_course": "Updated Department/Course"
}
```

**Note:** All fields are optional. Only include the fields you want to update.

**Response (200 OK):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "Updated Full Name",
  "bio": "Updated bio text",
  "profile_photo": "https://example.com/new-profile.jpg",
  "institute_name": "Updated University",
  "dob": "1995-06-15",
  "dept_course": "Updated Department/Course",
  "gender": "male",
  "register_number": "CS2024001"
}
```

**cURL Example:**
```bash
curl -X PATCH http://127.0.0.1:8000/api/auth/profile/edit/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Updated Full Name",
    "bio": "Updated bio text",
    "profile_photo": "https://example.com/new-profile.jpg"
  }'
```

---

### 6. Upload File
**POST** `/api/auth/upload/`

Upload a file to Appwrite storage and get its URL. **No authentication required.**

**Headers:**
```
Content-Type: multipart/form-data
```

**Request Body:**
```
file: [file upload]
```

**Response (200 OK):**
```json
{
  "file_id": "unique_file_id",
  "file_url": "https://cloud.appwrite.io/v1/storage/buckets/68dd64ea00069ab481c3/files/unique_file_id/view?project=68dd64330036984d70ce",
  "message": "File uploaded successfully"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "No file provided"
}
```

**Response (500 Internal Server Error):**
```json
{
  "error": "Upload failed",
  "details": "Error details"
}
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/upload/ \
  -F "file=@path/to/your/file.jpg"
```

---

### 6. Get Users List
**GET** `/api/auth/users/`

Get a paginated list of users excluding current user and already followed users.

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
  "next": "http://127.0.0.1:8000/api/auth/users/?page=2",
  "previous": null,
  "results": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "username": "johndoe",
      "full_name": "John Doe"
    },
    {
      "id": "456e7890-e89b-12d3-a456-426614174000",
      "username": "janedoe",
      "full_name": "Jane Smith"
    }
  ]
}
```

**Response (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**cURL Example:**
```bash
curl -X GET http://127.0.0.1:8000/api/auth/users/ \
  -H "Authorization: Bearer <access_token>"
```

---

## Social Features

The social features section provides comprehensive functionality for creating and managing posts, comments, user relationships, and interactions within the Unilink platform.

### Posts

Posts are the core content units in the social platform. Users can create text posts, attach images, or include videos. All posts support comments and reactions from other users.

#### 1. List All Posts (Global Timeline)
**GET** `/api/social/posts/`

Retrieve a paginated list of ALL posts from ALL users in the platform, ordered by creation date (newest first). This endpoint serves as the main discovery feed where users can explore content from across the entire platform.

**Purpose:**
- 🌐 **Global Discovery**: Browse content from all users on the platform
- 📱 **Main Timeline**: Primary feed for exploring new content
- 🔍 **Content Discovery**: Find new users and interesting posts
- 🔄 **Real-time Updates**: Get the latest posts when refreshing the app

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page` (optional): Page number for pagination (default: 1)
- `page_size` (optional): Number of posts per page (default: 20, max: 100)

**Response (200 OK):**
```json
{
  "count": 150,
  "next": "http://127.0.0.1:8000/api/social/posts/?page=2",
  "previous": null,
  "results": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "user": {
        "id": "456e7890-e89b-12d3-a456-426614174000",
        "email": "author@example.com",
        "username": "johndoe",
        "full_name": "John Doe",
        "bio": "Software Developer | Tech Enthusiast",
        "profile_photo": "https://cloud.appwrite.io/v1/storage/buckets/profile-photos/files/user123/view?project=project_id",
        "institute_name": "University of Technology",
        "dob": "1995-06-15",
        "dept_course": "Computer Science",
        "gender": "male",
        "register_number": "CS2024001"
      },
      "text": "Just finished building an amazing mobile app! 🚀 The development process was challenging but incredibly rewarding. Can't wait to share it with everyone!",
      "image_url": "https://cloud.appwrite.io/v1/storage/buckets/media/files/app-screenshot.jpg/view?project=project_id",
      "video_url": "https://cloud.appwrite.io/v1/storage/buckets/media/files/app-demo.mp4/view?project=project_id",
      "created_at": "2024-01-15T10:30:00Z",
      "comments": [
        {
          "id": "comment-uuid-1",
          "user": {
            "username": "alice_dev",
            "full_name": "Alice Developer"
          },
          "text": "This looks amazing! What tech stack did you use?",
          "created_at": "2024-01-15T10:35:00Z",
          "subcomments": []
        }
      ],
      "reactions_count": 15
    },
    {
      "id": "789e0123-e89b-12d3-a456-426614174001",
      "user": {
        "id": "321e0987-e89b-12d3-a456-426614174001",
        "username": "sarah_writer",
        "full_name": "Sarah Writer",
        "bio": "Content Creator | University Student",
        "profile_photo": "https://cloud.appwrite.io/v1/storage/buckets/profile-photos/files/user456/view?project=project_id",
        "institute_name": "Creative Arts University",
        "dob": "1998-03-22",
        "dept_course": "Journalism",
        "gender": "female",
        "register_number": "JA2024005"
      },
      "text": "Beautiful sunset from campus today! 📸 Sometimes the best moments are the simple ones.",
      "image_url": "https://cloud.appwrite.io/v1/storage/buckets/media/files/sunset.jpg/view?project=project_id",
      "video_url": null,
      "created_at": "2024-01-15T09:15:00Z",
      "comments": [],
      "reactions_count": 8
    }
  ]
}
```

**Error Responses:**
- **401 Unauthorized**: Invalid or missing authentication token
- **500 Internal Server Error**: Server-side error

**Use Cases:**
- **Mobile App Feed**: Load the main timeline in your mobile application
- **Web Dashboard**: Display global posts in a web interface
- **Content Discovery**: Allow users to discover new content and users
- **Analytics**: Track popular content across the platform

**cURL Example:**
```bash
curl -X GET http://127.0.0.1:8000/api/social/posts/ \
  -H "Authorization: Bearer <access_token>"
```

---

#### 2. Create Post
**POST** `/api/social/posts/`

Create a new post with optional media attachments (images and/or videos). This endpoint allows users to share content with the community, supporting rich media content alongside text.

**Purpose:**
- 📝 **Content Creation**: Share thoughts, updates, and experiences
- 🖼️ **Media Sharing**: Attach images or videos to posts
- 🎥 **Video Content**: Share video content (newly supported feature)
- 💬 **Community Engagement**: Start conversations with other users

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
All fields are optional, but at least one should be provided:
```json
{
  "text": "Just finished my final project! 🎉 The past few months have been challenging but incredibly rewarding. Can't wait to present it tomorrow!",
  "image_url": "https://cloud.appwrite.io/v1/storage/buckets/media/files/project-screenshot.jpg/view?project=project_id",
  "video_url": "https://cloud.appwrite.io/v1/storage/buckets/media/files/project-demo.mp4/view?project=project_id"
}
```

**Field Descriptions:**
- `text` (optional): The main content of the post. Supports Unicode characters, emojis, and line breaks
- `image_url` (optional): URL to an image file. Must be a valid URL pointing to an image
- `video_url` (optional): URL to a video file. Must be a valid URL pointing to a video

**Response (201 Created):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user": {
    "id": "456e7890-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "bio": "Computer Science Student | Aspiring Developer",
    "profile_photo": "https://cloud.appwrite.io/v1/storage/buckets/profile-photos/files/user123/view?project=project_id",
    "institute_name": "University of Technology",
    "dob": "1995-06-15",
    "dept_course": "Computer Science",
    "gender": "male",
    "register_number": "CS2024001"
  },
  "text": "Just finished my final project! 🎉 The past few months have been challenging but incredibly rewarding. Can't wait to present it tomorrow!",
  "image_url": "https://cloud.appwrite.io/v1/storage/buckets/media/files/project-screenshot.jpg/view?project=project_id",
  "video_url": "https://cloud.appwrite.io/v1/storage/buckets/media/files/project-demo.mp4/view?project=project_id",
  "created_at": "2024-01-15T10:30:00Z",
  "comments": [],
  "reactions_count": 0
}
```

**Error Responses:**
- **400 Bad Request**: Invalid request data or validation errors
- **401 Unauthorized**: Invalid or missing authentication token
- **500 Internal Server Error**: Server-side error

**Validation Rules:**
- At least one of `text`, `image_url`, or `video_url` must be provided
- URLs must be valid and accessible
- Text content should be reasonable in length (no hard limit, but extremely long posts may affect performance)

**Use Cases:**
- **Text Posts**: Share thoughts, announcements, or updates
- **Image Posts**: Share photos, screenshots, or visual content
- **Video Posts**: Share video demonstrations, tutorials, or vlogs
- **Mixed Media**: Combine text with images and/or videos for rich content

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

Get all posts by a specific user. **No authentication required.**

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
        "email": "johndoe@example.com",
        "username": "johndoe",
        "full_name": "John Doe",
        "bio": "Bio text",
        "profile_photo": "https://example.com/photo.jpg",
        "institute_name": "University of Technology",
        "dob": "1995-06-15",
        "dept_course": "Computer Science",
        "gender": "male",
        "register_number": "CS2024001"
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

#### 4. Delete Post
**DELETE** `/api/social/posts/{id}/delete/`

Delete a specific post. **Authentication required.** Only the post owner can delete their own posts.

**Path Parameters:**
- `id` (required): UUID of the post to delete

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (204 No Content):**
```
No content returned on successful deletion
```

**Response (404 Not Found):**
```json
{
  "detail": "Not found."
}
```

**cURL Example:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/social/posts/123e4567-e89b-12d3-a456-426614174000/delete/ \
  -H "Authorization: Bearer <access_token>"
```

---

#### 5. Get Personalized Feed
**GET** `/api/social/feed/`

Get a personalized feed showing posts from users you follow plus your own posts. This endpoint uses advanced timestamp-based pagination and includes gender distribution algorithms for enhanced user experience.

**Purpose:**
- 🏠 **Personalized Timeline**: See content from users you care about
- 📊 **Smart Distribution**: Gender-balanced content distribution
- ⚡ **Efficient Pagination**: Timestamp-based pagination for smooth scrolling
- 🔄 **Real-time Updates**: Get latest posts from your network

**Algorithm Details:**
- Shows posts from users you follow + your own posts
- For male users: 70% of posts are from female users (gender balance)
- For female users: Standard chronological feed from followed users
- Posts are ordered by creation time (newest first)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `timestamp` (optional): ISO 8601 timestamp for pagination (e.g., "2024-01-15T10:30:00Z")
- `type` (optional): Pagination direction
  - `"old"` (default): Get posts older than the timestamp
  - `"new"`: Get posts newer than the timestamp (for refresh functionality)

**Response (200 OK):**
```json
{
  "count": 15,
  "next": "http://127.0.0.1:8000/api/social/feed/?timestamp=2024-01-15T10:30:00Z&type=old",
  "previous": "http://127.0.0.1:8000/api/social/feed/?timestamp=2024-01-15T09:15:00Z&type=new",
  "results": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "user": {
        "id": "456e7890-e89b-12d3-a456-426614174000",
        "email": "friend@example.com",
        "username": "alice_dev",
        "full_name": "Alice Developer",
        "bio": "Software Engineer | Coffee Enthusiast",
        "profile_photo": "https://example.com/photo.jpg",
        "institute_name": "University of Technology",
        "dob": "1995-06-15",
        "dept_course": "Computer Science",
        "gender": "female",
        "register_number": "CS2024002"
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

**Usage Examples:**

**Get latest posts:**
```bash
curl -X GET http://127.0.0.1:8000/api/social/feed/ \
  -H "Authorization: Bearer <access_token>"
```

**Get older posts (pagination):**
```bash
curl -X GET "http://127.0.0.1:8000/api/social/feed/?timestamp=2024-01-15T10:30:00Z&type=old" \
  -H "Authorization: Bearer <access_token>"
```


**Get newer posts (refresh):**
```bash
curl -X GET "http://127.0.0.1:8000/api/social/feed/?timestamp=2024-01-15T10:30:00Z&type=new" \
  -H "Authorization: Bearer <access_token>"
```

**Notes:**
- For male users, the feed automatically shows 70% posts from female users
- `type=new` returns posts newer than the timestamp
- `type=old` returns posts older than the timestamp
- If no timestamp is provided, returns latest posts
- Posts are ordered chronologically (newest first for 'old', oldest first for 'new')

---

#### 5. Get Post Details
**GET** `/api/social/posts/{id}/`

Get details of a specific post. **No authentication required.**

**Path Parameters:**
- `id` (required): UUID of the post

**Response (200 OK):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user": {
    "id": "456e7890-e89b-12d3-a456-426614174000",
    "email": "johndoe@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "bio": "Bio text",
    "profile_photo": "https://example.com/photo.jpg",
    "institute_name": "University of Technology",
    "dob": "1995-06-15",
    "dept_course": "Computer Science",
    "gender": "male",
    "register_number": "CS2024001"
  },
  "text": "Detailed post content",
  "image_url": "https://example.com/image.jpg",
  "created_at": "2024-01-15T10:30:00Z",
  "comments": [
    {
      "id": "789e0123-e89b-12d3-a456-426614174000",
      "user": {
        "id": "012e3456-e89b-12d3-a456-426614174000",
        "email": "commenter@example.com",
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

Comments enable users to engage with posts through threaded conversations. The system supports unlimited nested replies, allowing for rich discussions and community interaction.

#### 1. Create Comment
**POST** `/api/social/comments/`

Create a new comment on a post or reply to an existing comment. This endpoint supports both direct post comments and nested reply threads with unlimited depth.

**Purpose:**
- 💬 **Post Engagement**: Comment on posts to start conversations
- 🔗 **Threaded Replies**: Reply to existing comments for discussions
- 🌐 **Community Building**: Foster interactions between users
- 📝 **Content Discussion**: Share thoughts and opinions on posts

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "post": "123e4567-e89b-12d3-a456-426614174000",
  "text": "Great post! I totally agree with your perspective. The examples you provided really help illustrate the concept. Looking forward to more insights! 👍",
  "parent": "789e0123-e89b-12d3-a456-426614174000"
}
```

**Field Descriptions:**
- `post` (required): UUID of the post you want to comment on
- `text` (required): The comment content. Supports Unicode, emojis, and line breaks
- `parent` (optional): UUID of a parent comment if replying to an existing comment

**Important Notes:**
- Use `post` field (not `post_id`) for the post UUID
- Comments support unlimited nesting depth
- All comments are associated with the authenticated user

**Response (201 Created):**
```json
{
  "id": "789e0123-e89b-12d3-a456-426614174000",
  "user": {
    "id": "456e7890-e89b-12d3-a456-426614174000",
    "email": "johndoe@example.com",
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
    "post": "123e4567-e89b-12d3-a456-426614174000",
    "text": "This is a comment"
  }'
```

---

#### 2. Get Post Comments
**GET** `/api/social/posts/{post_id}/comments/`

Get all top-level comments for a specific post. **No authentication required.**

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
        "email": "commenter@example.com",
        "username": "commenter",
        "full_name": "Comment Author",
        "bio": "",
        "profile_photo": null,
        "institute_name": "University of Technology",
        "dob": "1995-06-15",
        "dept_course": "Computer Science",
        "gender": "male",
        "register_number": "CS2024001"
      },
      "post": "123e4567-e89b-12d3-a456-426614174000",
      "parent": null,
      "text": "This is a top-level comment",
      "created_at": "2024-01-15T11:00:00Z",
      "subcomments": []
    },
    {
      "id": "345e6789-e89b-12d3-a456-426614174000",
      "user": {
        "id": "678e9012-e89b-12d3-a456-426614174000",
        "email": "commenter2@example.com",
        "username": "commenter2",
        "full_name": "Another Commenter",
        "bio": "Bio text",
        "profile_photo": "https://example.com/photo.jpg",
        "institute_name": "University of Technology",
        "dob": "1995-06-15",
        "dept_course": "Computer Science",
        "gender": "female",
        "register_number": "CS2024002"
      },
      "post": "123e4567-e89b-12d3-a456-426614174000",
      "parent": null,
      "text": "Another top-level comment",
      "created_at": "2024-01-15T11:30:00Z",
      "subcomments": []
    }
  ]
}
```

**Note:** This endpoint returns only top-level comments (no replies). To get replies to a specific comment, use the `/api/social/comments/{comment_id}/replies/` endpoint.

**cURL Example:**
```bash
curl -X GET http://127.0.0.1:8000/api/social/posts/123e4567-e89b-12d3-a456-426614174000/comments/
```

---

#### 3. Get Comment Replies
**GET** `/api/social/comments/{comment_id}/replies/`

Get all replies to a specific comment. **No authentication required.**

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
        "email": "replier@example.com",
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

Follow a user to see their posts in your personalized feed. Following a user creates a relationship that allows you to stay updated with their content and activities.

**Purpose:**
- 👥 **Build Connections**: Create relationships with other users
- 📱 **Personalized Feed**: See posts from followed users in your feed
- 🔔 **Stay Updated**: Get notified about new content from users you follow
- 🌐 **Community Building**: Expand your network on the platform

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

**Field Descriptions:**
- `user_id` (required): UUID of the user you want to follow

**Response (200 OK):**
```json
{
  "status": "Now following johndoe"
}
```

**Error Responses:**
- **400 Bad Request**: Invalid user ID or trying to follow yourself
- **404 Not Found**: User with the specified ID doesn't exist
- **409 Conflict**: Already following this user
- **401 Unauthorized**: Invalid or missing authentication token

**Important Notes:**
- You cannot follow yourself
- Following is a one-way relationship (doesn't automatically make them follow you back)
- Once you follow a user, their posts will appear in your personalized feed

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

Stop following a user to remove their posts from your personalized feed. This action removes the follow relationship but doesn't delete any previous interactions.

**Purpose:**
- 🚫 **Manage Feed**: Remove users from your personalized timeline
- 🎯 **Curate Content**: Control what content appears in your feed
- 🔄 **Relationship Management**: Manage your following list
- 📱 **Feed Optimization**: Keep your feed relevant to your interests

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

**Field Descriptions:**
- `user_id` (required): UUID of the user you want to unfollow

**Response (200 OK):**
```json
{
  "status": "Unfollowed johndoe"
}
```

**Error Responses:**
- **400 Bad Request**: Invalid user ID or trying to unfollow yourself
- **404 Not Found**: User with the specified ID doesn't exist or you're not following them
- **401 Unauthorized**: Invalid or missing authentication token

**Important Notes:**
- Unfollowing a user removes their posts from your personalized feed
- Previous comments and interactions remain intact
- You can re-follow the user later if desired
- This action is reversible

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

#### 3. Check Follow Status
**GET** `/api/social/follow-status/`

Check if the current user is following a specific user.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `user_id` (required): UUID of the user to check follow status for

**Response (200 OK):**
```json
{
  "is_following": true,
  "user_id": "456e7890-e89b-12d3-a456-426614174000",
  "username": "johndoe",
  "full_name": "John Doe"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "user_id parameter is required"
}
```

**Response (404 Not Found):**
```json
{
  "error": "User not found"
}
```

**cURL Example:**
```bash
curl -X GET "http://127.0.0.1:8000/api/social/follow-status/?user_id=456e7890-e89b-12d3-a456-426614174000" \
  -H "Authorization: Bearer <access_token>"
```

---

#### 4. Get User Followers
**GET** `/api/social/users/{user_id}/followers/`

Get list of users following a specific user. **No authentication required.**

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

#### 5. Get User Following
**GET** `/api/social/users/{user_id}/following/`

Get list of users that a specific user follows. **No authentication required.**

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

Reactions allow users to express their feelings and engagement with posts. The system supports various reaction types, with likes being the primary form of positive feedback.

#### 1. Add Reaction
**POST** `/api/social/react/`

Add a reaction to a post to show your appreciation or engagement. This creates a positive interaction between you and the post author.

**Purpose:**
- 👍 **Show Appreciation**: Express positive feedback on posts
- 💬 **Engage with Content**: Participate in community interactions
- 📊 **Content Metrics**: Help authors understand post popularity
- 🔗 **Social Connection**: Build relationships through interactions

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

**Field Descriptions:**
- `post_id` (required): UUID of the post you want to react to
- `reaction_type` (required): Type of reaction. Currently supports:
  - `"like"`: Positive reaction to show appreciation

**Response (200 OK):**
```json
{
  "status": "like added"
}
```

**Error Responses:**
- **400 Bad Request**: Invalid post ID or reaction type
- **404 Not Found**: Post with the specified ID doesn't exist
- **409 Conflict**: You've already reacted to this post
- **401 Unauthorized**: Invalid or missing authentication token

**Important Notes:**
- You can only react once per post
- Reactions are counted in the post's `reactions_count` field
- Reactions help determine post popularity and engagement

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

Get list of users who liked a specific post. **No authentication required.**

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

Get detailed profile information for a user. **No authentication required.**

**Path Parameters:**
- `id` (required): UUID of the user

**Response Fields:**
- `id`: Unique identifier for the user
- `email`: User's email address
- `username`: User's unique username
- `full_name`: User's full name
- `bio`: User's biography/description
- `profile_photo`: URL to user's profile photo
- `institute_name`: Name of the educational institution
- `dob`: Date of birth (YYYY-MM-DD format)
- `dept_course`: Department or course of study
- `gender`: User's gender (male/female/others)
- `register_number`: Unique registration number
- `date_joined`: When the user joined the platform (ISO format)
- `followers_count`: Number of users following this user
- `following_count`: Number of users this user follows
- `posts_count`: Number of posts created by this user
- `age`: Calculated age based on date of birth

**Response (200 OK):**
```json
{
  "id": "456e7890-e89b-12d3-a456-426614174000",
  "email": "johndoe@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "bio": "Software developer and tech enthusiast",
  "profile_photo": "https://example.com/profile.jpg",
  "institute_name": "University of Technology",
  "dob": "1995-03-15",
  "dept_course": "Computer Science Engineering",
  "gender": "male",
  "register_number": "REG123456",
  "date_joined": "2024-01-15T10:30:00Z",
  "followers_count": 150,
  "following_count": 75,
  "posts_count": 200,
  "age": 29
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

Search for posts by text content. **No authentication required.**

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
        "email": "johndoe@example.com",
        "username": "johndoe",
        "full_name": "John Doe",
        "bio": "",
        "profile_photo": null,
        "institute_name": "University of Technology",
        "dob": "1995-06-15",
        "dept_course": "Computer Science",
        "gender": "male",
        "register_number": "CS2024001"
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

Search for users by username or full name. **No authentication required.**

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

#### 6. Get Current User Following List
**GET** `/api/social/following/`

Get list of users that the current authenticated user is following. **Authentication required.**

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
  "next": "http://127.0.0.1:8000/api/social/following/?page=2",
  "previous": null,
  "results": [
    {
      "id": "456e7890-e89b-12d3-a456-426614174000",
      "username": "johndoe",
      "full_name": "John Doe",
      "bio": "Software Developer",
      "profile_photo": "https://example.com/photo.jpg",
      "followers_count": 150,
      "following_count": 75,
      "posts_count": 200
    },
    {
      "id": "789e0123-e89b-12d3-a456-426614174001",
      "username": "janedoe",
      "full_name": "Jane Doe",
      "bio": "Designer",
      "profile_photo": "https://example.com/jane.jpg",
      "followers_count": 300,
      "following_count": 120,
      "posts_count": 150
    }
  ]
}
```

**cURL Example:**
```bash
curl -X GET http://127.0.0.1:8000/api/social/following/ \
  -H "Authorization: Bearer <access_token>"
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
  "institute_name": "string (max 200 chars, required)",
  "dob": "date (required)",
  "dept_course": "string (max 200 chars, required)",
  "gender": "string (choices: 'male', 'female', 'others', required)",
  "register_number": "string (unique, max 50 chars, required)",
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
  "video_url": "URL (optional)",
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
  "reaction_type": "string (choices: 'like')"
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

## Public vs Protected Endpoints

### Public Endpoints (No Authentication Required)
- User Posts: `GET /api/social/users/{user_id}/posts/`
- Post Details: `GET /api/social/posts/{id}/`
- User Profile: `GET /api/social/users/{id}/profile/`

- Post Comments: `GET /api/social/posts/{post_id}/comments/`
- Comment Replies: `GET /api/social/comments/{comment_id}/replies/`
- User Followers: `GET /api/social/users/{user_id}/followers/`
- User Following: `GET /api/social/users/{user_id}/following/`
- Post Likes: `GET /api/social/posts/{post_id}/likes/`
- Search Posts: `GET /api/social/search/posts/`
- Search Users: `GET /api/social/search/users/`
- File Upload: `POST /api/auth/upload/`

### Protected Endpoints (Authentication Required)
- All authentication endpoints (signup, login, verify-email, delete, users list)
- Create Post: `POST /api/social/posts/`
- List Posts: `GET /api/social/posts/`
- Feed: `GET /api/social/feed/`
- Create Comment: `POST /api/social/comments/`
- Follow/Unfollow: `POST/DELETE /api/social/follow/`
- Check Follow Status: `GET /api/social/follow-status/`
- Add/Remove Reaction: `POST/DELETE /api/social/react/`

---

## Notes

- All timestamps are in ISO 8601 format (UTC)
- UUIDs are used for all primary keys
- Email verification is required before account activation
- Users cannot follow themselves
- Comments support nested replies (unlimited depth)
- Search is case-insensitive
- Image and video URLs should be valid URLs
- All text fields support Unicode characters
- **Important**: Use `post` field (not `post_id`) when creating comments
- Feed shows posts from users you follow plus your own posts
- All public endpoints work without authentication for better user experience