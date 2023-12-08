from django.urls import path
from .views import (
    BeverageView,
    BulkBeverageView,
    BulkWaterIntakeView,
    CreateBeverageView,
    WaterIntakeView,
    CreateWaterIntakeView,
)


urlpatterns = [
    path("beverages/<str:pk>", BeverageView.as_view(), name="beverages"),
    path("beverages", CreateBeverageView.as_view(), name="create beverages"),
    path("beverages_bulk", BulkBeverageView.as_view(), name="bulk beverages"),
    path("water_intake/<str:pk>", WaterIntakeView.as_view(), name="water intake"),
    path("water_intake", CreateWaterIntakeView.as_view(), name="water intake"),
    path("water_intake_bulk", BulkWaterIntakeView.as_view(), name="bulk water intake"),
]
