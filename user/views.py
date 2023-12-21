import logging
from django.utils import timezone
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import get_object_or_404

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ValidationError

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from drf_spectacular.utils import extend_schema

from .models import User
from .serializers import (
    LoginSerializer,
    UserSerializer,
    VerifyOTPSerializer,
)
from .utils import (
    send_otp,
    custom_send_mail,
    twilio_client,
    generate_otp
)

LOGGER = logging.getLogger(__name__)

@extend_schema(tags=["AUTH"])
class LoginView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def parse_validation(self, data):
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer

    def try_method(self):
        return "real value"

    def post(self, request):
        val = self.try_method()
        return Response({"detail": val})

        if request.data.get("phone") is None and request.data.get("email") is None:
            raise ValidationError({"detail":"mandatory field phone or email."})

        seriaizer = self.parse_validation(data=request.data)
        otp = generate_otp()
        key = ''
        if seriaizer.validated_data.get("phone"):
            key = seriaizer.validated_data["phone"]
            response = send_otp(key, otp)

        else:
            key = seriaizer.validated_data["email"]
            response = custom_send_mail("Veryfication Code", otp, [key])

        if not response["send"]:
            return Response(
                {"detail": response["message"]}, status=status.HTTP_400_BAD_REQUEST
            )
            
        cache.set(key, otp, timeout=300)
        return Response({"detail": "OTP sent successfully."})


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

        verify_id =  req_data.get('phone') or req_data.get('email')
        cache_otp = cache.get(verify_id)
        if cache_otp is None and cache_otp != req_data["otp"]:
            return Response({"error": "Invalid Code or Expired."}, status=status.HTTP_401_UNAUTHORIZED)
            
        if req_data.get('phone'):
            user, is_created = User.objects.get_or_create(phone=verify_id)
            user.is_phone_verified = True
            cache.delete(req_data["phone"])
        else:
            user, is_created = User.objects.get_or_create(email=verify_id)
            user.is_email_verified = True
            cache.delete(req_data["email"])

        user.last_login = timezone.now()
        user.save()

        token = RefreshToken.for_user(user)
        response_data = {
            "refresh_token": str(token),
            "access_token": str(token.access_token),
            "expiry_at": "1d",
        }

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
