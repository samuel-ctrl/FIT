from django.db.models import Q

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from drf_spectacular.utils import extend_schema

from core.decorators import request_user_only

from .models import Beverage, WaterIntake
from .serializers import (
    BeverageSerializer,
    BulkWaterIntakeSerializer,
    CreateBeverageSerializer,
    WaterIntakeSerializer,
    BulkBeverageSerializer,
    CreateWaterIntakeSerializer,
)


@extend_schema(tags=["BEVERAGES"])
class BeverageView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Beverage.objects.all()
    serializer_class = BeverageSerializer
    model = Beverage

    def parse_validation(self, data, instance=None, partial=False):
        serializer = self.serializer_class(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        return serializer

    @request_user_only
    def get(self, request, pk):
        instance = self.get_object()
        serializer = self.serializer_class(instance, context=request)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @request_user_only
    def patch(self, request, pk):
        instance = self.get_object()
        user_serilizer = self.parse_validation(
            instance=instance, data=request.data, partial=True
        )
        user_serilizer.update(
            instance=instance,
            validated_data=user_serilizer.validated_data,
            user=request.user,
        )
        return Response(data={"details": "Updated success."}, status=status.HTTP_200_OK)

    @request_user_only
    def put(self, request, pk):
        instance = self.get_object()
        serializer = self.parse_validation(data=request.data)
        serializer.update(
            instance=instance,
            validated_data=serializer.validated_data,
            user=request.user,
        )
        return Response(status=status.HTTP_200_OK, data={"details": "updated success"})

    @request_user_only
    def delete(self, request, pk):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_200_OK, data={"details": "deleted success."})


@extend_schema(tags=["BEVERAGES"])
class CreateBeverageView(generics.CreateAPIView):
    queryset = Beverage.objects.all()
    serializer_class = CreateBeverageSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.create(
            validated_data=serializer.validated_data, user=request.user
        )
        return Response(
            data={"details": serializer_data.data},
            status=status.HTTP_201_CREATED,
        )


@extend_schema(tags=["BEVERAGES"])
class BulkBeverageView(generics.RetrieveAPIView):
    queryset = Beverage.objects.all()
    serializer_class = BulkBeverageSerializer
    pagination_class = LimitOffsetPagination

    def parse_validation(self, data):
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer

    def get(self, request):
        data = self.queryset.filter(Q(user=request.user) | Q(is_admin=True))
        serializer = self.serializer_class(data, many=True)
        paginate_date = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(paginate_date)


@extend_schema(tags=["WATERINTAKE"])
class CreateWaterIntakeView(generics.CreateAPIView):
    queryset = WaterIntake.objects.all()
    serializer_class = CreateWaterIntakeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.create(validated_data=serializer.validated_data, user=request.user)
        return Response(
            data={"details": serializer_data.data},
            status=status.HTTP_201_CREATED,
        )


@extend_schema(tags=["WATERINTAKE"])
class WaterIntakeView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WaterIntake.objects.all()
    serializer_class = WaterIntakeSerializer
    model = WaterIntake

    def parse_validation(self, data, instance=None, partial=False):
        serializer = self.serializer_class(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        return serializer

    @request_user_only
    def get(self, request, pk):
        instance = self.get_object()
        serializer = self.serializer_class(instance, context=request)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @request_user_only
    def patch(self, request, pk):
        instance = self.get_object()
        user_serilizer = self.parse_validation(
            instance=instance, data=request.data, partial=True
        )
        user_serilizer.update(
            instance=instance,
            validated_data=user_serilizer.validated_data,
            user=request.user,
        )
        return Response(data={"details": "Updated success."}, status=status.HTTP_200_OK)

    @request_user_only
    def put(self, request, pk):
        instance = self.get_object()
        serializer = self.parse_validation(data=request.data)
        serializer.update(
            instance=instance,
            validated_data=serializer.validated_data,
            user=request.user,
        )
        return Response(status=status.HTTP_200_OK, data={"details": "updated success"})

    @request_user_only
    def delete(self, request, pk):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_200_OK, data={"details": "deleted success."})


@extend_schema(tags=["WATERINTAKE"])
class BulkWaterIntakeView(generics.ListAPIView):
    queryset = WaterIntake.objects.all()
    serializer_class = BulkWaterIntakeSerializer
    pagination_class = LimitOffsetPagination

    def get(self, request):
        qs_data = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(qs_data, many=True)
        paginate_date = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(paginate_date)
