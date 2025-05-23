from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        email = validated_data["email"]
        username_base = email.split("@")[0]
        username = username_base
        counter = 1

        # Check if username exists and append _n if it does
        while User.objects.filter(username=username).exists():
            username = f"{username_base}_{counter}"
            counter += 1

        validated_data["username"] = username
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), username=email, password=password
            )

            if not user:
                raise serializers.ValidationError(
                    "Unable to log in with provided credentials."
                )

            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")

            attrs["user"] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include "email" and "password".')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value


class TokenSerializer(serializers.Serializer):
    """Serializer for token response"""

    access = serializers.CharField()
    refresh = serializers.CharField()

    def to_representation(self, instance):
        from apps.users.serializers import UserProfileSerializer

        data = super().to_representation(instance)
        if hasattr(instance, "user"):
            data["user"] = UserProfileSerializer(instance.user).data
        return data
