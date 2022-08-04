from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from user_app.api.serializers import RegistrationSerializer


@api_view(["POST", ])
def register(req):
    if req.method == 'POST':
        serializer = RegistrationSerializer(data=req.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            data = serializer.data
            data["token"] = token.key
            data['state'] = "registraion successful"
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST", ])
def logout_view(req):
    if req.method == 'POST':
        req.user.auth_token.delete()
        return Response({"state": "logged out successfuly"}, status.HTTP_200_OK)
