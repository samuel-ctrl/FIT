import uuid
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from multiselectfield import MultiSelectField


class User(AbstractBaseUser):
    class Gender(models.TextChoices):
        OTHER = "Other"
        MALE = "Male"
        FEMALE = "Female"

    class ActivityLevel(models.TextChoices):
        SEDENTARY = "Sedentary"
        MODERATE = "Moderate"
        ACTIVE = "Active"

    class HealthConditions(models.TextChoices):
        NORMAL = "Normal"
        DIABETES = "Diabetes"
        KIDNEY_DISEASE = "Kidney Disease"
        HEART_DISEASE = "Heart Disease"
        DIARRHEA_OR_VOMITING = "Diarrhea OR Vomiting"

    class Settings(models.TextChoices):
        EMAIL = "Email"
        SMS = "SMS"
        APP = "App", "App Notification"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    is_phone_verified = models.BooleanField(default=False)
    remainder_settings = MultiSelectField(choices=Settings.choices, max_length=10)
    is_email_verified = models.BooleanField(default=False)
    age = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    sex = models.CharField(max_length=10, choices=Gender.choices, default=Gender.MALE)
    health_condition = models.CharField(
        max_length=20,
        choices=HealthConditions.choices,
        default=HealthConditions.NORMAL,
    )
    activity_level = models.CharField(
        max_length=20,
        choices=ActivityLevel.choices,
        default=ActivityLevel.SEDENTARY,
    )
    wake_up_time = models.DateTimeField(blank=True, null=True)
    sleeping_time = models.DateTimeField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone
