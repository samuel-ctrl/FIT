import re
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.constent import CustomRegex

from .models import User


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "phone",
            "email",
            "age",
            "weight",
            "height",
            "sex",
            "health_condition",
            "wake_up_time",
            "sleeping_time"
        ]

    def validate_first_name(self, value):
        if not value.isalnum():
            raise ValidationError(f"first name is only contain alphabetic: {value}")
        return value

    def validate_last_name(self, value):
        if not value.isalpha():
            raise ValidationError(f"last name is only contain alphabetic: {value}")
        return value

    def validate_age(self, value):
        if value > 120 or value < 0.6:
            raise ValidationError(f"Invalid age: {value}")
        return value

    def validate_phone(self, value):
        if not re.match(CustomRegex.PHONE_NUMBER.value, value):
            raise ValidationError(f"Invalid phone number: {value}")
        return value

    def update(self, instance, validated_data):
        for key in validated_data.keys():
            setattr(instance, key, validated_data[key])
        instance.save()
        return instance


class LoginSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()

    class Meta:
        model = User
        fields = [
            "phone",
        ]

    def validate_phone(self, value):
        if not re.match(CustomRegex.PHONE_NUMBER.value, value):
            raise ValidationError(f"Invalid phone number: {value}")
        return value


class VerifyOTPSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()
    otp = serializers.IntegerField()

    class Meta:
        model = User
        fields = ["phone", "otp"]

    def validate_phone(self, value):
        if not re.match(CustomRegex.PHONE_NUMBER.value, value):
            raise ValidationError(f"Invalid phone number: {value}")
        return value


class TokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, coach):
        token = super().get_token(coach)
        token["name"] = coach.name
        return token
