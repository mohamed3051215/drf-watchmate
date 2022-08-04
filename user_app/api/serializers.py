from rest_framework import serializers as s
from django.contrib.auth.models import User


class RegistrationSerializer(s.ModelSerializer):
    password2 = s.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]
        extra_kwargs = {'password': {"write_only": True}}

    def save(self):
        data = self.validated_data
        username = data['username']
        email = data['email']
        password1 = data["password"]
        password2 = data['password2']
        if password1 != password2:
            raise s.ValidationError(
                {"error": "confirm password doesn't match"})

        if User.objects.filter(email=email).exists():
            raise s.ValidationError(
                {"error", "Email already exists, try another one"})
        user = User(email=email, username=username)
        user.set_password(password1)
        user.save()
        return user
