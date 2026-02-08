from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (EmailTokenObtainPairView, PaymentsCreateAPIView, PaymentsDestroyAPIView, PaymentsListAPIView,
                         PaymentsRetrieveAPIView, PaymentsUpdateAPIView, PaymentsViewSet, TransactionCreateAPIView,
                         UserCreateAPIView, UserViewSet)

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
    path("token/", EmailTokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="token_obtain_pair"),
    path("login/", EmailTokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("transaction/", TransactionCreateAPIView.as_view(), name="transaction"),
]

urlpatterns += router.urls
