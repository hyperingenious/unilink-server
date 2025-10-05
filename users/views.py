from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
import jwt
from datetime import datetime, timedelta
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from appwrite.client import Client
from appwrite.services.storage import Storage
from appwrite.id import ID
from appwrite.input_file import InputFile
import uuid
import io

from .models import User
from .serializers import UserSerializer, RegisterSerializer, UserListSerializer
from social.models import Follower
from social.pagination import StandardResultsSetPagination

# ------------------- Register -------------------
class RegisterView(generics.CreateAPIView):
    """
    Register a new user account.
    
    POST: Create a new user account (requires email verification)
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        operation_description="Register a new user account",
        request_body=RegisterSerializer,
        responses={
            201: openapi.Response('User Created', examples={
                'application/json': {'message': 'User created. Check email for verification link.'}
            }),
            400: openapi.Response('Bad Request', examples={
                'application/json': {'error': 'Validation errors'}
            })
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(is_active=True)  # Active for testing

        # Generate email verification token
        token_data = {
            "user_id": str(user.id),
            "exp": datetime.utcnow() + timedelta(hours=24)  # 24-hour expiry
        }
        verification_token = jwt.encode(token_data, settings.SECRET_KEY, algorithm="HS256")

        # Send verification email
        verification_path = "/api/auth/verify-email"
        verification_link = f"http://127.0.0.1:8000{verification_path}?token={verification_token}"

        send_mail(
            subject="Verify your Unilink email",
            message=f"Click the link to verify: {verification_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return Response({"message": "User created. Check email for verification link."}, status=status.HTTP_201_CREATED)


# ------------------- Login -------------------

class LoginView(APIView):
    """
    Authenticate user and return JWT tokens.
    
    POST: Login with email and password to get access and refresh tokens
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Login with email and password",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='User email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password')
            },
            required=['email', 'password']
        ),
        responses={
            200: openapi.Response('Login Success', examples={
                'application/json': {
                    'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                    'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                    'user': {
                        'id': '123e4567-e89b-12d3-a456-426614174000',
                        'email': 'user@example.com',
                        'username': 'johndoe',
                        'full_name': 'John Doe'
                    }
                }
            }),
            400: openapi.Response('Bad Request', examples={
                'application/json': {'error': 'Invalid credentials'}
            }),
            403: openapi.Response('Forbidden', examples={
                'application/json': {'error': 'Email not verified'}
            })
        }
    )
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)

        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_active:
            return Response({"error": "Email not verified"}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(user).data
        })

# ------------------- Delete Account -------------------
class DeleteAccountView(APIView):
    """
    Delete the authenticated user's account.
    
    DELETE: Permanently delete the user account (requires authentication)
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Delete the authenticated user's account",
        responses={
            200: openapi.Response('Account Deleted', examples={
                'application/json': {'status': 'account deleted'}
            }),
            401: openapi.Response('Unauthorized', examples={
                'application/json': {'detail': 'Authentication credentials were not provided.'}
            })
        }
    )
    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"status": "account deleted"})


# ------------------- Verify Email -------------------
class VerifyEmailView(APIView):
    """
    Verify user email with token.
    
    GET: Verify user email using the token sent via email
    """
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_description="Verify user email with token",
        manual_parameters=[
            openapi.Parameter(
                'token',
                openapi.IN_QUERY,
                description="Email verification token",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response('Email Verified', examples={
                'application/json': {'status': 'Email verified'}
            }),
            400: openapi.Response('Bad Request', examples={
                'application/json': {'error': 'Missing token'}
            }),
            400: openapi.Response('Bad Request', examples={
                'application/json': {'error': 'Invalid or expired token'}
            })
        }
    )
    def get(self, request):
        token = request.GET.get("token")
        if not token:
            return Response({"error": "Missing token"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()
            return Response({"status": "Email verified"})
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)


# ------------------- File Upload -------------------
class FileUploadView(APIView):
    """
    Upload a file to Appwrite storage and return the file URL.
    
    POST: Upload a file and get its URL
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Upload a file to Appwrite storage (No authentication required)",
        manual_parameters=[
            openapi.Parameter(
                'file',
                openapi.IN_FORM,
                description="File to upload",
                type=openapi.TYPE_FILE,
                required=True
            )
        ],
        responses={
            200: openapi.Response('File Uploaded', examples={
                'application/json': {
                    'file_id': 'unique_file_id',
                    'file_url': 'https://cloud.appwrite.io/v1/storage/buckets/68dd64ea00069ab481c3/files/unique_file_id/view?project=68dd64330036984d70ce',
                    'message': 'File uploaded successfully'
                }
            }),
            400: openapi.Response('Bad Request', examples={
                'application/json': {'error': 'No file provided'}
            }),
            500: openapi.Response('Server Error', examples={
                'application/json': {'error': 'Upload failed', 'details': 'Error details'}
            })
        }
    )
    def post(self, request):
        if 'file' not in request.FILES:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        uploaded_file = request.FILES['file']
        
        try:
            # Initialize Appwrite client
            client = Client()
            client.set_endpoint(settings.APPWRITE_ENDPOINT)
            client.set_project(settings.APPWRITE_PROJECT_ID)
            client.set_key(settings.APPWRITE_API_KEY)
            
            # Initialize Storage service
            storage = Storage(client)
            
            # Generate unique file ID
            file_id = ID.unique()
            
            # Create InputFile for Appwrite
            input_file = InputFile.from_bytes(
                uploaded_file.read(),
                uploaded_file.name
            )
            
            # Upload file to Appwrite
            result = storage.create_file(
                bucket_id=settings.APPWRITE_BUCKET_ID,
                file_id=file_id,
                file=input_file
            )
            
            # Construct file URL
            file_url = f"{settings.APPWRITE_ENDPOINT}/storage/buckets/{settings.APPWRITE_BUCKET_ID}/files/{file_id}/view?project={settings.APPWRITE_PROJECT_ID}"
            
            return Response({
                "file_id": file_id,
                "file_url": file_url,
                "message": "File uploaded successfully"
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "error": "Upload failed",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ------------------- User List -------------------
class UserListView(generics.ListAPIView):
    """
    Get a paginated list of users excluding current user and already followed users.
    
    GET: Get list of users to potentially follow
    """
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    @swagger_auto_schema(
        operation_description="Get paginated list of users (excluding current user and already followed users)",
        responses={
            200: openapi.Response('Users List', examples={
                'application/json': {
                    'count': 25,
                    'next': 'http://127.0.0.1:8000/api/auth/users/?page=2',
                    'previous': None,
                    'results': [
                        {
                            'id': '123e4567-e89b-12d3-a456-426614174000',
                            'username': 'johndoe',
                            'full_name': 'John Doe'
                        },
                        {
                            'id': '456e7890-e89b-12d3-a456-426614174000',
                            'username': 'janedoe',
                            'full_name': 'Jane Smith'
                        }
                    ]
                }
            }),
            401: openapi.Response('Unauthorized', examples={
                'application/json': {'detail': 'Authentication credentials were not provided.'}
            })
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        current_user = self.request.user
        
        # Get IDs of users that the current user is already following
        following_ids = Follower.objects.filter(follower=current_user).values_list('user_id', flat=True)
        
        # Exclude current user and already followed users
        queryset = User.objects.exclude(
            id=current_user.id
        ).exclude(
            id__in=following_ids
        ).order_by('username')
        
        return queryset
