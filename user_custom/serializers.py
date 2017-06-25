from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserRegistrationSerializer

User = get_user_model()


class CustomUserRegistrationSerializer(UserRegistrationSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            User.USERNAME_FIELD, User._meta.pk.name, 'password',
        ) + ('first_name', 're_password', 'phone_number')

    re_password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
    )

    def validate(self, data):
        password = data.get('password')
        re_password = data.get('re_password')
        if password != re_password:
            raise serializers.ValidationError("Both passwords should match")
        data.pop('re_password')
        return data
