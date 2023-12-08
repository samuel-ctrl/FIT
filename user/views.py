import random

from django.utils import timezone
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import get_object_or_404

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from drf_spectacular.utils import extend_schema

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from .models import User

from .serializers import (
    LoginSerializer,
    UserSerializer,
    VerifyOTPSerializer,
)


def twilio_client():
    return Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)


def generate_otp():
    return str(random.randint(1000, 9999))


@extend_schema(tags=["AUTH"])
class LoginView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def parse_validation(self, data):
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer

    @staticmethod
    def send_otp(phone, otp):
        # Send otp with twilio account.
        try:
            my_otp = f"Your OTP is {otp}."
            client = twilio_client()
            message = client.messages.create(
                body=my_otp,
                to=phone,
                from_=settings.TWILIO_PHONE_NUMBER,
            )
        except TwilioRestException as e:
            error_dict = {"send": False, "message": str(e)}
            error_message = ""
            if e.code == 21211:
                error_message = "Invalid phone number"
            elif e.code == 21608:
                error_message = "The number is unverified."

            if error_message:
                error_dict["message"] = error_message
            return error_dict
        return {"send": True, "message": message}

    def post(self, request):
        seriaizer = self.parse_validation(data=request.data)
        phone = seriaizer.validated_data["phone"]
        otp = generate_otp()
        cache.set(phone, otp, timeout=300)
        response = self.send_otp(phone, otp)
        if response["send"]:
            return Response({"message": "OTP sent successfully."})
        return Response(
            {"message": response["message"]}, status=status.HTTP_400_BAD_REQUEST
        )


@extend_schema(tags=["AUTH"])
class VerifyOTPView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyOTPSerializer

    def parse_validation(self, data):
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer

    def post(self, request) -> Response:
        serializer = self.parse_validation(data=request.data)
        req_data = serializer.validated_data
        cache_otp = 0000
        # cache_otp = cache.get(phone)

        if cache_otp is not None and cache_otp != int(req_data["otp"]):
            raise Exception(details="Invalid Code")

        user, _ = User.objects.get_or_create(phone=req_data["phone"])
        user.is_phone_verified = True
        user.last_login = timezone.now()
        user.save()

        token = RefreshToken.for_user(user)
        response_data = {
            "refresh_token": str(token),
            "access_token": str(token.access_token),
            "expiry_at": "1d",
        }

        cache.delete(req_data["phone"])

        return Response(response_data, status=status.HTTP_200_OK)


@extend_schema(tags=["AUTH"])
class TokenRefreshView(TokenRefreshView):
    pass


@extend_schema(tags=["USER"])
class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def parse_validation(self, data, instance=None, partial=False):
        serializer = self.serializer_class(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        return serializer

    def get(self, request):
        data = self.queryset.filter(pk=request.user.id).first()
        serializer = UserSerializer(data)
        return Response(
            data={"details": serializer.data},
            status=status.HTTP_200_OK,
        )

    def patch(self, request):
        instance = get_object_or_404(User, pk=request.user.id)
        user_serilizer = self.parse_validation(instance=instance, data=request.data, partial=True)
        user_serilizer.update(instance, user_serilizer.validated_data)
        return Response(data={"details": "Updated success."}, status=status.HTTP_200_OK)

    def put(self, request):
        instance = get_object_or_404(User, pk=request.user.id)
        user_serilizer = self.parse_validation(data=request.data)
        user_serilizer.update(instance, user_serilizer.validated_data)
        return Response(data={"details": "Updated success."}, status=status.HTTP_200_OK)

    def delete(self, request):
        instance = get_object_or_404(User, pk=request.user.id)
        instance.delete()
        return Response(status=status.HTTP_200_OK, data={"details": "deleted success."})
