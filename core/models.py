import uuid
from django.db import models
from user.models import User


class Beverage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    water_content = models.SmallIntegerField()
    description = models.CharField(max_length=300)
    icon = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class WaterIntake(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    beverage_type = models.ForeignKey(Beverage, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name


class NotificationSetting(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255)
    reminder_type = models.CharField(max_length=255)
    frequency = models.DateField()
    activate = models.BooleanField(default=False)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Remainder(models.Model):
    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_setting = models.ForeignKey(
        NotificationSetting, on_delete=models.CASCADE
    )
    message = models.CharField(max_length=255)

    def __str__(self):
        return self.coach
