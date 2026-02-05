from django.urls import path
from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from users.views import (
    UserViewSet,
    PaymentsViewSet,
    PaymentsCreateAPIView,
    PaymentsDestroyAPIView,
    PaymentsListAPIView,
    PaymentsRetrieveAPIView,
    PaymentsUpdateAPIView,
)

app_name = UsersConfig.name


router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"payments", PaymentsViewSet, basename="payments")

urlpatterns = [
    path("payments/list/", PaymentsListAPIView.as_view(), name="payments_list"),
    path("payments/<int:pk>/", PaymentsRetrieveAPIView.as_view(), name="payments_retrieve"),
    path("payments/create/", PaymentsCreateAPIView.as_view(), name="payments_create"),
    path("payments/<int:pk>/delete", PaymentsDestroyAPIView.as_view(), name="payments_delete"),
    path("payments/<int:pk>/update", PaymentsUpdateAPIView.as_view(), name="payments_update"),
]

urlpatterns += router.urls
