from django.forms import ValidationError
from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["email", "is_active", "staff", "admin", "created_at", "modified_at"]


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    password2 = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Confirm Password'}
    )

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user

    def validate(self, attrs):
        if attrs.get("password2") != attrs.get("password"):
            raise ValidationError({'password': 'Password and confirm password must match.'})
        return attrs

    class Meta:
        model = User
        fields = ("id", "email", "password", "password2")
        write_only_fields = ("password","password2")
        read_only_fields = ("id",)
