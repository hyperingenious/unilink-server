from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "full_name", "bio", "profile_photo", 
                 "institute_name", "dob", "dept_course", "gender", "register_number"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "full_name", "password", 
                 "institute_name", "dob", "dept_course", "gender", "register_number", "profile_photo"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "full_name"]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["full_name", "bio", "profile_photo", "institute_name", "dept_course"]
        extra_kwargs = {
            'full_name': {'required': False},
            'bio': {'required': False},
            'profile_photo': {'required': False},
            'institute_name': {'required': False},
            'dept_course': {'required': False},
        }
