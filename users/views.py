from django_filters import CharFilter, ChoiceFilter, FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import Payments, User
from users.serializers import EmailTokenObtainPairSerializer, PaymentsSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class PaymentsFilter(FilterSet):
    payment_course = CharFilter(field_name="payment_course__id")
    payment_type = ChoiceFilter(choices=Payments.PAYMENTS_CHOICES)

    class Meta:
        model = Payments
        fields = ["payment_course", "payment_type"]


class PaymentsViewSet(ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentsFilter
    ordering_fields = ["payment_date"]
    ordering = ["-payment_date"]
    filterset_fields = ["payment_course", "payment_type"]
    search_fields = ["payment_course", "payment_type"]

    def get_queryset(self):
        queryset = super().get_queryset()
        ordering = self.request.query_params.get("ordering", None)
        if ordering:
            if ordering.lstrip("-") == "payment_date":
                queryset = queryset.order_by(ordering)

        return queryset


class PaymentsCreateAPIView(CreateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer


class PaymentsListAPIView(ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer


class PaymentsRetrieveAPIView(RetrieveAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer


class PaymentsUpdateAPIView(UpdateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer


class PaymentsDestroyAPIView(DestroyAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
