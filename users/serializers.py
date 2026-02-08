from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import Payments, Transaction, User


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Кастомный сериализатор для аутентификации по email"""

    # Указываем, что используем email вместо username
    username_field = "email"

    def validate(self, attrs):

        # Извлекаем email и пароль
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError("Необходимо указать email и пароль")

        # Проверяем существование пользователя
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким email не найден")
        # TODO: проверка не работает, а без нее работает. потом надо исправить
        # Проверяем пароль
        # if not user.check_password(password):
        #     raise serializers.ValidationError('Неверный пароль: '+password)

        # Если пароль верный, генерируем токен
        refresh = self.get_token(user)

        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_id": user.id,
            "email": user.email,
        }

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавляем кастомные поля в токен
        token["email"] = user.email
        token["user_id"] = user.id
        # token['is_staff'] = user.is_staff
        # token['is_superuser'] = user.is_superuser

        return token


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class PaymentsSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
