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

from .models import User
from .serializers import UserSerializer, RegisterSerializer

# ------------------- Register -------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

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
    permission_classes = [AllowAny]  # <-- Add this line

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
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"status": "account deleted"})


# ------------------- Verify Email -------------------
class VerifyEmailView(APIView):
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
