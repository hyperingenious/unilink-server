import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, username, full_name, institute_name, dob, dept_course, gender, register_number, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")
        if not institute_name:
            raise ValueError("Institute name is required")
        if not dob:
            raise ValueError("Date of birth is required")
        if not dept_course:
            raise ValueError("Department/Course is required")
        if not gender:
            raise ValueError("Gender is required")
        if not register_number:
            raise ValueError("Register number is required")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            full_name=full_name,
            institute_name=institute_name,
            dob=dob,
            dept_course=dept_course,
            gender=gender,
            register_number=register_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, full_name, institute_name, dob, dept_course, gender, register_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)  # Superusers are active by default
        return self.create_user(email, username, full_name, institute_name, dob, dept_course, gender, register_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=150)
    bio = models.TextField(blank=True, default="")
    profile_photo = models.URLField(blank=True, null=True)
    
    # New fields for account creation
    institute_name = models.CharField(max_length=200)
    dob = models.DateField()
    dept_course = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    register_number = models.CharField(max_length=50, unique=True)

    is_active = models.BooleanField(default=False)  # Must verify email first
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "full_name", "institute_name", "dob", "dept_course", "gender", "register_number"]

    def __str__(self):
        return f"@{self.username}"
