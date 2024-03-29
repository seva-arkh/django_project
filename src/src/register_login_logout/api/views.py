# from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response

# from knox.models import AuthToken
from register_login_logout.api.serializer \
    import UserSerializer, RegisterSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView

# from rest_framework.decorators import api_view
from rest_framework.authtoken.views import ObtainAuthToken


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"user":
             UserSerializer(user, context=self.get_serializer_context()).data}
        )


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class TokenRetrieveView(ObtainAuthToken):
    pass
