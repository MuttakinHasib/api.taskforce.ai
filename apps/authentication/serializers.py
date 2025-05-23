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
