from datetime import datetime
from django.utils import timezone
from django.forms import ValidationError
from django.db.models import Q
from rest_framework import serializers

from core.constants import ALREADY_EXIST_MESSAGE, INVALID_VALUE_MESSAGE

from .models import Beverage, WaterIntake


class BulkBeverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beverage
        exclude = ["user"]


class BulkWaterIntakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterIntake
        exclude = ["user"]


class BeverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beverage
        exclude = ["id", "user"]

    def update(self, instance, validated_data, user):
        name = validated_data.get("name")
        if (
            name
            and Beverage.objects.filter(Q(is_admin=True) | Q(user=user))
            .filter(name=name)
            .exists()
        ):
            raise serializers.ValidationError(
                {"error": f"{ALREADY_EXIST_MESSAGE} - {name}"}
            )
        for key in validated_data.keys():
            setattr(instance, key, validated_data[key])
        instance.save()
        return instance


class CreateBeverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beverage
        fields = ["name", "description", "water_content", "icon"]

    def validate_water_content(self, value):
        if value == 0 or value > 100:
            raise ValidationError(f"{INVALID_VALUE_MESSAGE} - {value}")
        return value

    def create(self, validated_data, user):
        validated_data["user_id"] = str(user.id)
        name = validated_data.get("name")
        if (
            name
            and Beverage.objects.filter(Q(is_admin=True) | Q(user=user))
            .filter(name=name)
            .exists()
        ):
            raise serializers.ValidationError(
                {"error": f"{ALREADY_EXIST_MESSAGE} - {name}"}
            )
        if user.is_admin:
            validated_data["is_admin"] = True
        else:
            validated_data["is_admin"] = False

        user_data = Beverage.objects.create(**validated_data)
        serializer_data = BulkBeverageSerializer(user_data)
        return serializer_data


class WaterIntakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterIntake
        exclude = ["user"]


class CreateWaterIntakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterIntake
        exclude = ["id", "user"]

    def create(self, validated_data, user):
        validated_data["user_id"] = str(user.id)
        user_data = WaterIntake.objects.create(**validated_data)
        serializer_data = WaterIntakeSerializer(user_data)
        return serializer_data
