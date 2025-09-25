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

from .models import User
from .serializers import UserSerializer, RegisterSerializer

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
        user = serializer.save(is_active=False)  # Inactive until email verified

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
